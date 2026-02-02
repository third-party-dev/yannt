Tensorflow versions are tightly bound to Python version. Combined with broad contraints of Ultralytics causes pip to have to download all of the Tensorflow versions from newest to one that matches dependencies in pip. I can't express my awe of how stupid this process is. Could Ultralytics OR Tensorflow provide constraints? Yes! Could Tensorflow provide a lightweight meta package to prevent having to download all the things? Yes! Do they give a crap? Nope! ... so here I am installing `ultralytics[export]` with pip, waiting for it to download >10GB of Tensorflow versions so I can capture the constraints for the next install.

GPT says (early 2026):

```
Python     Tensorflow     Comment
------     ----------     -------
3.9	       2.12.x	        Least backtracking
3.10       2.13–2.15      Best overall
3.11       2.15+          Some export paths flaky
3.12       limited TF     lagging
3.13/3.14	 experimental	  Expect breakage
```

```
wurlitzer-3.1.1-py3-none-any.whl
ydf-0.14.0-cp39-cp39-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl
wrapt-1.14.2-cp39-cp39-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl
tensorflow_estimator-2.14.0-py2.py3-none-any.whl
tensorflow_io_gcs_filesystem-0.37.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
tensorflow_decision_forests-1.5.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
tensorflow-2.13.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
six-1.16.0-py2.py3-none-any.whl
pytz-2020.1-py2.py3-none-any.whl
python_dateutil-2.8.2-py2.py3-none-any.whl
pyparsing-2.3.1-py2.py3-none-any.whl
?? protobuf-6.33.2-cp39-abi3-manylinux2014_x86_64.whl
protobuf-5.29.1-cp38-abi3-manylinux2014_x86_64.whl



ultralytics[export] <- tensorflow[export] <- tensorflowjs <- flax <- tensorstore
                                                          <- tensorflow

```




requirements: Ultralytics requirements ['onnx2tf>=1.15.4,<=1.17.5', 'sng4onnx>=1
.0.1', 'onnxsim>=0.4.33', 'onnx_graphsurgeon>=0.3.26', 'tflite_support', 'onnxru
ntime'] not found
