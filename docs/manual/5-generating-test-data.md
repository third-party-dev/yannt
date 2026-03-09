# Generating Test Data

yannt comes with several configurations to assist with the setup of environments for the generation and conversion of test data. At the moment, this is primarily build around Ultralytic's `yolo` command and Huggingface's `transformers` library. From these two command, we can generate a great many ML artifacts to perform analysis on.

## Ultralytics

Ultralytics combines capabilities from many different ML environments. These different libraries rarely place nice together and therefore it can be a frustrating time getting them all into a single environment. I've personally run through a bit of a gambit to get things to the working state that they are and its "good enough" for me at the moment.

- `yolo-conda` - Process that will build a conda environment with ultralytics installed and will install every yolo export dependencies known to me (except tensorflow). 
- `yolo-tf-conda` - A special environment for handling Tensorflow based models (tflite, saved_model).
- `yolo-docker` - An `docker.io/ultralytics/ultralytics:8.4.8-python-export` docker based container install. It has all the things ready to go, but locked in at verion 8.4.8 and several years old. (Looked at source and while the `python-export` is still in code, appears to not be regularly tested?)
- `yolo-podman` - An `docker.io/ultralytics/ultralytics:8.4.8-python-export` podman based container install for those without docker access.

Note: None of these have been tested with GPU exports yet. In theory, the docker setup would work with GPU exports if you volume mounted the correct paths from host. This is on my things "to do", but hasn't happened yet.

## Huggingface

**Not Yet Implemented**