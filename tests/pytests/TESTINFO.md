# Test Info

## Coverage Synopsis

| format      | model               | NTL | NTD | PTL | PTD | DONE |
|-------------|---------------------|-----|-----|-----|-----|------|
| pytorch     | bert (weights-only) | XXX | XXX | XXX | XXX | XXXX |
| pytorch     | bert (architecture) | XXX | XXX | XXX | XXX | XXXX |
| safetensors | bert                | XXX | XXX | XXX | XXX | XXXX |
| onnx        | yolo                | XXX | XXX | XXX | XXX | XXXX |
| mnn         | yolo                |     |     |     |     |      |
| om          | yolo                |     |     |     |     |      |
| tflite      | yolo (float32)      |     |     |     |     | BAD  |
| zip         | NA                  | NA  | NA  | NA  | NA  | BAD  |
| json        | NA                  | NA  | NA  | NA  | NA  | XXXX |
| protobuf    | NA                  | NA  | NA  | NA  | NA  |      |
| flatbuffers | NA                  | NA  | NA  | NA  | NA  |      |
| pickle      | NA                  | NA  | NA  | NA  | NA  | XXXX |


## No Plan To Test

- pparse ident
- hft graph
- yannt sysscan

## Test Impl Deferred

- graph extraction

## Planned To Test

- (DONE) pparse pytorch == naive pytorch, weights_only tensor data
- (DONE) pparse pytorch == naive pytorch, architecture tensor data
- pparse safetensors == naive safetensors, tensor data
- pparse zip == naive zip, files
- pparse json == naive json, canonical-data
- pparse protobuf == expected data
- pparse flatbuffers == expected data
- pparse pickle == expected data
- pparse onnx == naive onnx, tensor data
- pparse mnn == naive mnn, tensor data
- pparse om == expected data, tensor data
- pparse tflite == naive tflite, tensor data

Notes:

- When we're confident there is no "naive" approach, we'll can only compare to expected data based on source data.
- Generic types (protobuf, flatbuffers, zip, pickle) will be tested based on known inputs.
- Tests that focus on tensor data remain ignorant of source data and pass if naive approach matches pparse approach.
