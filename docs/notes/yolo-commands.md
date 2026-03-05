```sh
# yolo-conda
yolo export model=yolov5su.pt format=torchscript
# yolo-conda, yolo-tf-conda
yolo export model=yolov5su.pt format=onnx
# yolo-conda
yolo export model=yolov5su.pt format=openvino
# yolo-conda
yolo export model=yolov5su.pt format=coreml
# yolo-tf-conda
yolo export model=yolov5su.pt format=saved_model
# yolo-tf-conda
yolo export model=yolov5su.pt format=tflite
# yolo-conda
yolo export model=yolov5su.pt format=paddle
# yolo-conda
yolo export model=yolov5su.pt format=ncnn
# NOT WORKING (requires running CUDA driver)
yolo export model=yolov5su.pt format=engine
```

```
ImportError: libtorch_cpu.so: cannot enable executable stack as shared object re
quires: Invalid argument
```

I'd like to have a `yolo-pt-cuda-conda` environment, but this is not installable without conda detecting a CUDA driver already on the system (i.e `__cuda`). Ugh.