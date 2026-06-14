
'''
Thoughts on terminology:
- metrics - collection of measurements (good for characterizing across dimensions)
- fingerprint - single derived value used for identify
- identifier - which one is this? (ideally distinct)
- qualifier - what is this like? (metrics, stats, characteristics)
- characteristics - properties of the tensor itself
- characterization - interpretation or description of the tensor

Factor Use Cases:
- Tensor Sha256 - Identical parameter (e.g. weight) detection.
- Architectural Sha256 - Compare structure across models within framework.
- Shape Sequence Sha256 - Compare structure across models and frameworks.
- Statistical Metrics - Indication of fine tuning / similarity.
- Data type Distribution - Indication of similarity / complexity.
- Value count - Count of all values in all observed tensors (ATM, includes non-learnable values.)
- Singular Value Decomposition (SVD) Metrics
  - Detect low rank adapters (LoRA has very low effective_rank).
  - Identify over-parameterized tensors.
  - Detect architectural familiar across retraining.
'''

import hashlib
import struct
import numpy as np
from dataclasses import dataclass, field, asdict
from typing import Any, Optional, Tuple

from thirdparty.yannt.analysis.lib import AnalysisFactor


@dataclass
class TensorMetrics:
    """Per-tensor statistical and structural metrics.

    Attributes:
        name: Tensor name as it appears in the model file.
        shape: Tensor shape tuple.
        dtype: Data type string (e.g. `'F32'`).
        sha256: Hex digest of the raw contiguous tensor bytes.
        mean: Mean of all tensor values.
        std: Standard deviation of all tensor values.
        min: Minimum tensor value.
        max: Maximum tensor value.
        sparsity: Fraction of values with absolute magnitude below 1e-6.
        kurtosis: Fisher (excess) kurtosis of tensor values.
        skewness: Skewness of tensor values.
        top_sv_ratio: Ratio of the largest to second-largest singular value,
            or `None` if SVD could not be computed.
        sv_entropy: Spectral entropy of the normalised singular values,
            or `None` if SVD could not be computed.
        effective_rank: Effective rank via squared-SV distribution entropy,
            or `None` if SVD could not be computed.
    """

    # standard fields
    name: str
    shape: tuple
    dtype: str

    # digest of contiguous values
    sha256: str

    # statistical metrics
    mean: float
    std: float
    min: float
    max: float
    sparsity: float
    kurtosis: float
    skewness: float

    # singular value decomposition (SVD) metrics
    top_sv_ratio: Optional[float]
    sv_entropy: Optional[float]
    effective_rank: Optional[float]


@dataclass
class ModelTensorMetrics:
    """Aggregate tensor metrics for an entire model.

    Attributes:
        dtype_dist: Mapping of dtype string to count of tensors with that dtype.
        value_count: Total number of scalar values across all tensors
            (pseudo-parameter count).
        tensors: Dict mapping tensor name to its :class:`TensorMetrics`.
        arch_sha256: Architectural hash computed from tensor names, dtypes, and
            shapes in canonical JSON form.
        shape_seq_sha256: Shape-sequence hash computed from sorted shape tuples,
            independent of tensor names.
    """

    # dtype distribution
    dtype_dist: dict[str, int]

    # pseudo-parameter count
    value_count: int

    # tensor metrics dictionary
    tensors: list[TensorMetrics]

    # arch sha256
    arch_sha256: str

    # shape seq sha256
    shape_seq_sha256: str


def calc_stat_metrics(arr: np.ndarray) -> dict[str, float]:
    """Compute descriptive statistics for a numpy array.

    Args:
        arr: Input tensor as a numpy array of any shape.

    Returns:
        A dict with keys `'mean'`, `'std'`, `'min'`, `'max'`,
        `'sparsity'`, `'kurtosis'`, and `'skewness'`.
    """
    def _safe_kurtosis(flat: np.ndarray) -> float:
        """Compute Fisher (excess) kurtosis, returning 0.0 for near-constant arrays.

        Args:
            flat: 1-D numpy array of float values.

        Returns:
            Excess kurtosis as a float.
        """
        if flat.std() < 1e-10:
            return 0.0
        z = (flat - flat.mean()) / flat.std()
        return float(np.mean(z ** 4) - 3.0)

    def _safe_skewness(flat: np.ndarray) -> float:
        """Compute skewness, returning 0.0 for near-constant arrays.

        Args:
            flat: 1-D numpy array of float values.

        Returns:
            Skewness as a float.
        """
        if flat.std() < 1e-10:
            return 0.0
        z = (flat - flat.mean()) / flat.std()
        return float(np.mean(z ** 3))

    flat = arr.flatten()
    return {
        "mean": float(np.mean(flat)),
        "std": float(np.std(flat)),
        "min": float(np.min(flat)),
        "max": float(np.max(flat)),
        "sparsity": float(np.mean(np.abs(flat) < 1e-6)),
        "kurtosis": _safe_kurtosis(flat),
        "skewness": _safe_skewness(flat),
    }


def calc_svd_metrics(arr: np.ndarray, max_sv: int = 64) -> dict[str, Optional[float]]:
    """Compute singular value decomposition metrics for a tensor.

    Only meaningful for arrays with at least two dimensions and a minimum inner
    dimension of 4.  Returns `None` values for all metrics when SVD cannot
    be performed.

    Args:
        arr: Input tensor as a numpy array.
        max_sv: Maximum number of singular values to retain.

    Returns:
        A dict with keys `'top_sv_ratio'`, `'sv_entropy'`, and
        `'effective_rank'`, each a float or `None`.
    """
    # Perform singular value decomposition. Note: Only useful for 2D matrices.
    # i.e. spectral analysis of the matrix's eigenvalues

    # Bail out if not enough data.
    if arr.ndim < 2 or min(arr.shape[-2:]) < 4:
        return {"top_sv_ratio": None, "sv_entropy": None, "effective_rank": None}

    # Reshape to 2D: (rows, cols) using last two dims
    mat = arr.reshape(-1, arr.shape[-1]).astype(np.float32)
    k = min(max_sv, min(mat.shape) - 1, 64)
    if k < 2:
        # Bail out if not enough data.
        return {"top_sv_ratio": None, "sv_entropy": None, "effective_rank": None}

    try:
        # The actual SVD computation via numpy.
        _, sv, _ = np.linalg.svd(mat, full_matrices=False)
        sv = sv[:k]
    except np.linalg.LinAlgError:
        # Bail if non-convergense, NaN/Inf values, numerical Instability
        return {"top_sv_ratio": None, "sv_entropy": None, "effective_rank": None}

    sv = sv[sv > 1e-10]
    if len(sv) < 2:
        # Bail out if not enough data.
        return {"top_sv_ratio": None, "sv_entropy": None, "effective_rank": None}

    top_sv_ratio = float(sv[0] / sv[1]) if sv[1] > 1e-10 else None

    # spectral entropy (of normalized singular values)
    sv_norm = sv / sv.sum()
    sv_entropy = float(-np.sum(sv_norm * np.log(sv_norm + 1e-12)))

    # effective rank via squared-SV distribution
    sv2 = sv ** 2
    sv2_norm = sv2 / sv2.sum()
    effective_rank = float(np.exp(-np.sum(sv2_norm * np.log(sv2_norm + 1e-12))))

    return {
        "top_sv_ratio": top_sv_ratio,
        "sv_entropy": sv_entropy,
        "effective_rank": effective_rank,
    }


def calc_tensor_sha256(numpy_arr: np.ndarray) -> str:
    """Compute a SHA-256 digest over the contiguous bytes of a numpy array.

    Args:
        numpy_arr: Input numpy array of any dtype and shape.

    Returns:
        Hex-encoded SHA-256 digest string.
    """
    # sha256 over serialized contiguous numpy array.
    return hashlib.sha256(np.ascontiguousarray(numpy_arr).tobytes()).hexdigest()


def calc_arch_sha256(st_entries: dict, keep_lm_head: bool = False) -> str:
    """Compute an architectural SHA-256 hash from tensor metadata.

    Hashes the canonical JSON representation of tensor names, dtypes, and
    shapes — without tensor data — so the digest is stable across training
    runs that use the same architecture.

    Args:
        st_entries: Dict mapping tensor name to `{'dtype': ..., 'shape': ...}`.
        keep_lm_head: Reserved for future use; currently unused.

    Returns:
        Hex-encoded SHA-256 digest string.
    """
    # Architectural hash calculated as canonical safetensors without data.
    # Hash will survive across training with same training framework.
    import json
    sane_json = json.dumps(st_entries, indent=None, separators=(",", ":"))
    return hashlib.sha256(sane_json.encode("utf-8")).hexdigest()


def calc_shape_seq_sha256(shapes: list) -> str:
    """Compute a SHA-256 hash from a sorted sequence of tensor shapes.

    Ignores tensor names so the digest is stable across training frameworks
    that use different naming conventions for the same architecture.

    Args:
        shapes: Iterable of shape tuples.

    Returns:
        Hex-encoded SHA-256 digest string.
    """
    # Shape sequence hash ignores names. Serialized as all shape lists (sorted).
    # Hash will survive training across training frameworks.
    hasher = hashlib.sha256()
    for shape in sorted(shapes):
        hasher.update(struct.pack(f"I{len(shape)}Q", len(shape), *shape))
    return hasher.hexdigest()


class TensorsCharacter(AnalysisFactor):
    """Analysis factor that computes per-tensor and model-level metrics.

    Reads a pparse viewer object from its last declared dependency and
    iterates over all tensors to produce a :class:`ModelTensorMetrics` result.
    The factor config may carry additional options via `factor_config`.
    """

    def __init__(self, name: str = "_init", dependencies: list = []) -> None:
        """Initialize TensorsCharacter.

        Args:
            name: Factor instance name.
            dependencies: List of upstream factor names; the last entry is
                expected to provide a pparse viewer object.
        """
        # Setup base class
        super().__init__(name=name, dependencies=dependencies)
        # Grab config from enclosed class object
        self.factor_config = self.__class__.factor_config
        #breakpoint()


    def run(self) -> ModelTensorMetrics:
        """Compute tensor metrics for the model provided by the upstream pparse viewer.

        Iterates over all tensors in sorted name order, computing statistical
        metrics, SVD metrics, and per-tensor SHA-256 digests, then assembles
        model-level aggregates.

        Returns:
            A :class:`ModelTensorMetrics` instance containing per-tensor
            metrics and model-level summaries.
        """
        print(f"Running in {type(self)}:{self.name}")
        print(f"  Dependencies: {self.dependencies}")

        '''
            Only accepts last dependency as a pparse view object with
            `obj.tensor_names()` and `obj.tensor(name) -> Tensor` API.
        '''

        obj = self.get_result(self.dependencies[-1])
        dtype_dist = {}
        shapes_list = []
        st_entries = {}
        tensor_dict = {}

        # TODO: Only include weights, bias, norm params, and embedding tables
        # TODO: Exclude buffers, non-learnable constants, and optimizer state
        value_count = 0
        
        # list sorted for arch_sha256 (via st_entries)
        for tensor_name in sorted(obj.tensor_names()):
            tensor = obj.tensor(tensor_name)
            dtype = tensor.get_type()
            shape = tensor.get_shape()
            numpy_arr = tensor.as_numpy()
            stat_metrics = calc_stat_metrics(numpy_arr)
            svd_metrics = calc_svd_metrics(numpy_arr)

            # Increment model dtype count.
            dtype_dist[dtype] = dtype_dist.setdefault(dtype, 0) + 1

            # Required for shape_seq_sha256
            shapes_list.append(shape)

            # Calculate pseudo-parameter count.
            value_count += numpy_arr.size

            # arch sha256 entries
            st_entries.setdefault(tensor_name, {'dtype': dtype, 'shape': shape})

            # TODO: Consider global mean, std, sparsity. (Performance challenges for large models.)

            tensor_dict[tensor_name] = TensorMetrics(
                name=tensor_name,
                shape=shape,
                dtype=tensor.get_type(),
                sha256=calc_tensor_sha256(numpy_arr),
                mean=stat_metrics["mean"],
                std=stat_metrics["std"],
                min=stat_metrics["min"],
                max=stat_metrics["max"],
                sparsity=stat_metrics["sparsity"],
                kurtosis=stat_metrics["kurtosis"],
                skewness=stat_metrics["skewness"],
                top_sv_ratio=svd_metrics["top_sv_ratio"],
                sv_entropy=svd_metrics["sv_entropy"],
                effective_rank=svd_metrics["effective_rank"],
            )

        return ModelTensorMetrics(
            # dtype distribution
            dtype_dist=dtype_dist,
            value_count=value_count,
            tensors=tensor_dict,
            arch_sha256=calc_arch_sha256(st_entries),
            shape_seq_sha256=calc_shape_seq_sha256(shapes_list),
        )
