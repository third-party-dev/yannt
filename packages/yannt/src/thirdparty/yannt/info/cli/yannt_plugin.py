
def register_yannt_info(subparsers):
    info_parser = subparsers.add_parser("info", help="info command")
    info_subparser = info_parser.add_subparsers(dest="info_command", required=True)

    info_yolo5_parser = info_subparser.add_parser("yolo5", help="yolo5 command")
    info_yolo5_parser.set_defaults(func=info_yolo5)

def neat(s, indent=''):
    min_spaces = 1000
    lines = s.splitlines()

    # Drop the first line.
    if len(lines) and len(lines[0].strip()) == 0:
        lines.pop(0)
    # Drop the last line.
    if len(lines) and len(lines[-1].strip()) == 0:
        lines.pop(-1)
    
    # Find initial indent.
    for line in lines:
        space_cnt = len(line) - len(line.lstrip(' '))
        if len(line) > 1 and space_cnt < min_spaces:
            min_spaces = space_cnt

    # Remove indent.
    new_lines = []
    for line in s.splitlines():
        new_lines.append(indent + line[min_spaces:])

    return '\n'.join(new_lines)

def info_yolo5(args):
    print(neat('''
        # ------------------------------------------------------------
        # Ultralytics python dependencies are impressively complicated
        # and therefore it is recommended to keep the library in its
        # own virtual environment when ever possible.
        # 
        # A common use case is to convert a yolo model from a PyTorch
        # checkpoint to a TensorFlow Lite (tflite) format. To
        # accomplish this, pull the docker image, acquire the 
        # checkpoint and the run a yolo command similar to the 
        # following:
        # ------------------------------------------------------------

        docker pull ultralytics/ultralytics:8.4.8-python-export

        docker run -it --rm \\
          -v $(pwd):/workspace \\
          ultralytics/ultralytics:8.4.8-python-export \\
          bash

        cd /workspace
        yolo export model=/workspace/yolov5su.pt format=tflite
        yolo export model=yolov5su.pt format=onnx opset=14

        # ------------------------------------------------------------
        # Ultralytics Checkpoints At:
        #   https://github.com/ultralytics/assets/releases
        #
        # Model Notation:
        # n - nano, s - small, m - medium, l - large, x - XLarge
        # 6 - input dimension scaling doubled
        # u - Ultralytics fork
        #
        # Model Size VRAM Expectations
        # n - 1GB, s - 2GB, m - 4GB, l - 7GB, x - 12GB
        #
    ''', indent='  '))
