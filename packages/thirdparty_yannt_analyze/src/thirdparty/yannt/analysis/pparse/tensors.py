
'''
Thoughts on terminology:
- metrics - collection of measurements (good for characterizing across dimensions)
- fingerprint - single derived value used for identify
- identifier - which one is this? (ideally distinct)
- qualifier - what is this like? (metrics, stats, characteristics)
- characteristics - properties of the tensor itself
- characterization - interpretation or description of the tensor
'''

import hashlib
import struct
import numpy as np
from dataclasses import dataclass, field, asdict
from typing import Any, Optional, Tuple

from thirdparty.yannt.analysis.lib import AnalysisFactor


@dataclass
class TensorMetrics:
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
    def _safe_kurtosis(flat: np.ndarray) -> float:
        # Fisher kurtosis (excess kurtosis, normal=0).
        if flat.std() < 1e-10:
            return 0.0
        z = (flat - flat.mean()) / flat.std()
        return float(np.mean(z ** 4) - 3.0)

    def _safe_skewness(flat: np.ndarray) -> float:
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


def calc_tensor_sha256(numpy_arr) -> str:
    # sha256 over serialized contiguous numpy array.
    return hashlib.sha256(np.ascontiguousarray(numpy_arr).tobytes()).hexdigest()


def calc_arch_sha256(st_entries, keep_lm_head=False):
    # Architectural hash calculated as canonical safetensors without data.
    # Hash will survive across training with same training framework.
    import json
    sane_json = json.dumps(st_entries, indent=None, separators=(",", ":"))
    return hashlib.sha256(sane_json.encode("utf-8")).hexdigest()


def calc_shape_seq_sha256(shapes) -> str:
    # Shape sequence hash ignores names. Serialized as all shape lists (sorted).
    # Hash will survive training across training frameworks.
    hasher = hashlib.sha256()
    for shape in sorted(shapes):
        hasher.update(struct.pack(f"I{len(shape)}Q", len(shape), *shape))
    return hasher.hexdigest()


class TensorsCharacter(AnalysisFactor):
    def __init__(self, name = "_init", dependencies = []):
        # Setup base class
        super().__init__(name=name, dependencies=dependencies)
        # Grab config from enclosed class object
        self.factor_config = self.__class__.factor_config
        #breakpoint()


    def run(self):
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
            spectral_metrics = calc_spectral_metrics(numpy_arr)

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
                top_sv_ratio=spectral_metrics["top_sv_ratio"],
                sv_entropy=spectral_metrics["sv_entropy"],
                effective_rank=spectral_metrics["effective_rank"],
            )

        return ModelTensorMetrics(
            # dtype distribution
            dtype_dist=dtype_dist,
            value_count=value_count,
            tensors=tensor_dict,
            arch_sha256=calc_arch_sha256(st_entries),
            shape_seq_sha256=calc_shape_seq_sha256(shapes_list),
        )
