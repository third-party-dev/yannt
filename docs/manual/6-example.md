# Example

```sh
cd yannt_transformers
./scripts/init-dev.sh
```

```sh
$ hft --help
$ hft --help
usage: hft [-h] [--breakpoint] {list,create,graph} ...

positional arguments:
  {list,create,graph}
    list               transformers list command
    create             transformers create command
    graph              transformers create command

options:
  -h, --help           show this help message and exit
  --breakpoint
```

```sh
$ hft list | grep " bert "
model: bert type: AutoModel
model: bert type: AutoModelForCausalLM
model: bert type: AutoModelForMaskedLM
model: bert type: AutoModelForMultipleChoice
model: bert type: AutoModelForNextSentencePrediction
model: bert type: AutoModelForPreTraining
model: bert type: AutoModelForQuestionAnswering
model: bert type: AutoModelForSequenceClassification
model: bert type: AutoModelForTextEncoding
model: bert type: AutoModelForTokenClassification
```

```sh
$ hft create --help
usage: hft create [-h] --type MODEL_TYPE --model MODEL_NAME
                  [--pytorch_path PYTORCH_PATH]
                  [--pytorch_params_path PYTORCH_PARAMS_PATH]
                  [--safetensors_path SAFETENSORS_PATH]
                  [--onnx_path ONNX_PATH] [--export_path EXPORT_PATH]
                  [--max_shard MAX_SHARD]

options:
  -h, --help            show this help message and exit
  --type MODEL_TYPE
  --model MODEL_NAME
  --pytorch_path PYTORCH_PATH
  --pytorch_params_path PYTORCH_PARAMS_PATH
  --safetensors_path SAFETENSORS_PATH
  --onnx_path ONNX_PATH
  --export_path EXPORT_PATH
  --max_shard MAX_SHARD
```

```sh
$ hft create --type AutoModel --model bert \
  --pytorch_path ./pt \
  --pytorch_params_path ./pt
Loading PyTorch and Transformers.
Indexing all of the transformer types available. (Takes a moment.)
Exporting everything to pytorch.
Exporting params (state_dict) to pytorch.
```

- `yannt pparse pytorch unpickle` - Only works on already extracted pkl files.

- `yannt pparse pytorch view /work/models/bert/bert-AutoModel.params.pt`
  - `Locals: ['args', 'pparse_repr', 'PyTorch', 'obj']`
  - `obj._extraction._result['zip'].value[0].value['fname']` - Ideally `data.pkl`
  - `obj._extraction._result['zip'].value[0].value['decomp_data'].value` - The raw pkl data.
  - `print(pparse_repr(obj._pkl_extraction._result['pkl'].value[0].value[0]))` - "Pretty" print pickle data.
  - `yannt pparse pytorch hash /work/models/bert/bert-AutoModel.complete.pt` - Generate arch hash
  - `obj._extraction._extractions[0]._result['pkl'].value[0].value[0].state['config']` - Get the model config

```python
topcall = obj._extraction._extractions[0]._result['pkl'].value[0].value[0]

topcall.module_call # -> (b'transformers.models.bert.modeling_bert\n', b'BertModel\n')
topcall.state['_modules']['pooler'].state['_modules']['dense'] # leads to params

layer_keys = topcall.state['_modules']['encoder'].state['_modules']['layer'].state['_modules'].keys()
# results in dict_keys(['11', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0'])

# Note: In the case of bert, this is where most of the data starts. There is not
# flat list (like in the case of state_dict()). It is a tree of modules with the various
# tensor data spread out. In theory, we could recursively traverse the tree and pull out
# all calls that use arg('storage', ...).
layer = topcall.state['_modules']['encoder'].state['_modules']['layer'].state['_modules']

# Based on observations, we could try only recursing into _modules and _parameters through
# the tree to discover tensors.

# An output LayerNorm tensor in layer 11?
layer['11'].state['_modules']['output'].state['_modules']['LayerNorm'].state['_parameters']['weight']
```
