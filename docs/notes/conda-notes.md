# ~~docker pull conda/miniconda3~~

docker pull continuumio/miniconda3:23.5.2-0

# Create home folder
mkdir -p conda-data/home

# Start container
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -e HOME=/opt/conda/home \
  -v $(pwd)/conda-data:/opt/conda \
  continuumio/miniconda3

# Update $HOME/.bashrc
conda init bash

# Restart shell (or container) to get .bashrc updates.

# Create yolo conda env
conda create -c conda-forge -n yolo python=3.11.10 -y
# Activate yolo env
conda activate yolo
# Install reqs in ultralytics/ultralytics:8.4.8-python-export



# Optional: Wipe environment
conda deactivate
conda env remove -n yolo
