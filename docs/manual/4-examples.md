Get the arguments for gpt2:
- `yannt transformers list | grep gpt2`

Create pytorch and safetensors transformers:
```sh
yannt transformers create \
  --type AutoModelForCausalLM --model gpt2 \
  --pytorch_state_path output/gpt2-pytorch \
  --safetensors_path output/gpt-safetensors
```

Parse pytorch with viewer and break:
- `yannt pparse --breakpoint pytorch view output/gpt2-pytorch/gpt2-AutoModelForCausalLM.pth`

Some PDB things:

```python
pkl = obj._extraction._extractions[0]._result['pkl']
tensor_dict = pkl.value[0].value[0]
tensor_list = tensor_dict.keys()
print(pparse_repr(tensor_dict['transformer.ln_f.bias']))

reduce_call = tensor_dict['transformer.ln_f.bias']
persid_call = reduce_call.arg[0]
shape = reduce_call.arg[2]
type_tag = persid_call.arg[0]
type_name = persid_call.arg[1]
# torch.FloatStorage => dtype=float32
data_key = persid_call.arg[2]
data_dest = persid_call.arg[3]
elem_cnt = persid_call.arg[4]
```
