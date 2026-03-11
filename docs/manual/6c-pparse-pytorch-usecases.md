# PyTorch Use Cases

## Generate Arc Hash of (Weights Only) PyTorch File

Generate pt file for testing (weights only):

```sh
hft create --type AutoModel --model bert --pytorch_params_path ./pt
```

Generate arc hash:

```sh
yannt pparse pytorch hash /work/models/bert/bert-AutoModel.params.pt
```

Example:

```text
$ yannt pparse --breakpoint pytorch hash /work/models/bert/bert-AutoModel.params.pt
Hashing pytorch from: /work/models/bert/bert-AutoModel.params.pt with: arc
Parsing pkl of fpath
Based on 199 tensors seen.
1add2c275863ff5d8f35f2e77739895b2073c1390f6040f653260c127d1fdcc7
```

Inspect results at runtime with:

```sh
yannt pparse --breakpoint pytorch hash /work/models/bert/bert-AutoModel.params.pt
```



## Parse (Weights Only) PyTorch File For Tensor Extraction

Generate pt file for testing (weights only):

```sh
hft create --type AutoModel --model bert --pytorch_params_path ./pt
```

Parse pt file from CLI and inspect from pdb:

```sh
yannt pparse --breakpoint pytorch view /work/models/bert/bert-AutoModel.params.pt
```

Example Tensor List:

```text
$ yannt pparse --breakpoint pytorch view /work/models/bert/bert-AutoModel.params.pt
Parsing pytorch from: /work/models/bert/bert-AutoModel.params.pt
Parsing pkl of fpath
Locals: ['args', 'pparse_repr', 'PyTorch', 'obj']
--Return--
> /work/extern/thirdparty_pparse/src/thirdparty/pparse/cli/pparse_pytorch.py(116)pytorch_view()->None
-> breakpoint()
(Pdb) obj.tensor_names()
['pooler.dense.bias', 'pooler.dense.weight', ... 'embeddings.word_embeddings.weight']
(Pdb) tmp = obj.tensor('embeddings.word_embeddings.weight')
(Pdb) tmp.as_numpy()
len 93763584 np_type <class 'numpy.float32'> elem_cnt 23440896
array([-1.061812  , -0.26294687, -0.42156446, ..., -0.8086512 ,
        1.1152115 , -0.5360393 ], shape=(23440896,), dtype=float32)
(Pdb) tmp.get_shape()
[30522, 768]
(Pdb) tmp.get_type()
'F32'
```

Parse pt file from Python and inspect:

```python
from thirdparty.pparse.view.pytorch import PyTorch

model_data = PyTorch().open_fpath('/work/models/bert/bert-AutoModel.params.pt')
tensor_list = model_data.tensor_names()
a_tensor = model_data.tensor('embeddings.word_embeddings.weight')
tensor_numpy_array = a_tensor.as_numpy()
tensor_shape = a_tensor.get_shape()
tensor_type = a_tensor.get_type()
```

## Parse data.pkl pre-extracted from (any) PyTorch file (no unpickle() used!)

Generate pt file for testing (weights only):

```sh
hft create --type AutoModel --model bert --pytorch_path ./pt
cd pt ; unzip bert-AutoModel.complete.pt
```

Parse the `data.pkl` from command line:

```sh
yannt pparse pytorch unpickle bert-AutoModel.complete/data.pkl
```

Example Output:

```text
Parsing pickle from: bert-AutoModel.complete/data.pkl
transformers.models.bert.modeling_bert.BertModel(
  *(  # ARG
    [
    ]
  )  # End of ARG

  # STATE
  {
    _is_hf_initialized: True

... 57613 more lines of data ...

    _buffers: {
    }
    _parameters: {
    }
    training: False
  }

  # ITEMS
  {
  }
)
```

Parse the pkl from python (using low level lazy paring API):

```python
import thirdparty.pparse.lib as pparse
from thirdparty.pparse.lazy.pickle import Parser as LazyPickleParser

try:
    #'output/gpt2-pytorch/data.pkl'
    parser_reg = {"pkl": LazyPickleParser}
    data_source = pparse.FileData(path=args.path)
    data_range = pparse.Range(data_source.open(), data_source.length)
    root = pparse.BytesExtraction(name=args.path, reader=data_range)
    root.discover_parsers(parser_reg).scan_data()

except pparse.EndOfDataException as e:
    print(e)
    pass
    
top_of_node_tree = root._result["pkl"]
top_of_pkl_data = root._result["pkl"].value[0].value[0]
```

## Transform (Weights Only) PyTorch into Safetensors

Generate pt file for testing (weights only):

```sh
hft create --type AutoModel --model bert --pytorch_params_path ./pt
```

Transform pytorch to safetensors:

```sh
yannt pparse pytorch transform /work/models/bert/bert-AutoModel.params.pt test.safetensors
```

See the data with xxd:

```text
$ xxd -l0x100 -g1 test.safetensors
00000000: 58 57 00 00 00 00 00 00 7b 22 5f 5f 6d 65 74 61  XW......{"__meta
00000010: 64 61 74 61 5f 5f 22 3a 7b 22 66 6f 72 6d 61 74  data__":{"format
00000020: 22 3a 22 70 74 22 7d 2c 22 65 6d 62 65 64 64 69  ":"pt"},"embeddi
00000030: 6e 67 73 2e 4c 61 79 65 72 4e 6f 72 6d 2e 62 69  ngs.LayerNorm.bi
00000040: 61 73 22 3a 7b 22 64 74 79 70 65 22 3a 22 46 33  as":{"dtype":"F3
00000050: 32 22 2c 22 73 68 61 70 65 22 3a 5b 37 36 38 5d  2","shape":[768]
00000060: 2c 22 64 61 74 61 5f 6f 66 66 73 65 74 73 22 3a  ,"data_offsets":
00000070: 5b 30 2c 33 30 37 32 5d 7d 2c 22 65 6d 62 65 64  [0,3072]},"embed
00000080: 64 69 6e 67 73 2e 4c 61 79 65 72 4e 6f 72 6d 2e  dings.LayerNorm.
00000090: 77 65 69 67 68 74 22 3a 7b 22 64 74 79 70 65 22  weight":{"dtype"
000000a0: 3a 22 46 33 32 22 2c 22 73 68 61 70 65 22 3a 5b  :"F32","shape":[
000000b0: 37 36 38 5d 2c 22 64 61 74 61 5f 6f 66 66 73 65  768],"data_offse
000000c0: 74 73 22 3a 5b 33 30 37 32 2c 36 31 34 34 5d 7d  ts":[3072,6144]}
000000d0: 2c 22 65 6d 62 65 64 64 69 6e 67 73 2e 70 6f 73  ,"embeddings.pos
000000e0: 69 74 69 6f 6e 5f 65 6d 62 65 64 64 69 6e 67 73  ition_embeddings
000000f0: 2e 77 65 69 67 68 74 22 3a 7b 22 64 74 79 70 65  .weight":{"dtype
```

Parse out the safe tensors header with yannt:

```sh
yannt pparse safetensors header test.safetensors > test.safetensors.json
```

Transform in python:

```python
from thirdparty.pparse.view.pytorch import PyTorch
obj = PyTorch().open_fpath('/work/models/bert/bert-AutoModel.params.pt')
obj.as_safetensors('test.safetensors', keep_lm_head=False)
```
