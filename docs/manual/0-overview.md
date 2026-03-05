# Yet Another Neural Network Tool (yannt)

## Purpose

Yet Another Neural Network Tool (yannt) is a command line tool and suite of libraries for performing analysis and operations on machine learning models and environments. It is highly inspired by the work done by Netron, but in a way that is much less visual. The goal is to be able to parse model formats, convert model formats, and perform various analysis on model formats and the ML environment.

yannt itself is a command line interface wrapper and command line framework. In otherwords, none of the actual work mentioned above is performed by yannt. Instead you must install yannt plugins inside the same python (virtual) environment. The plugins themselves become subcommands of the top-level yannt command with their own arguments and handlers.

From strictly a user perspective, yannt is a single point of entry for discovering and using the plugins installed into the python environment. The most important of these plugins is the `pparse` plugin. The pparse plugin has its own documentation, but for now you should know that when installing `thirdparty.pparse` into a python environment, it enables:

- `import thirdparty.pparse.lib as pparse` - First and foremost, pparse is a python library that is designed to be imported and used by other python code. **Note: No testing in Jupyter Notebooks is performed. All testing is done with test scripts run from within the `env.sh` built virtual environment. Work is planned for supporting Jupyter Environments.**

- `yannt pparse [pparse-command] [options] [args]` - For CLI actions, its recommended to use yannt as the entrypoint. The CLI is primary intended for common task execution, data preparation, and user demonstration purposes. You get all of the power of the tools with your own python scripts, but sometimes you just want to copy paste some commands to get what you need.

- `pparse [pparse-command] [options] [args]` - For systems that are confident they only need pparse, you can install pparse by itself, without yannt. This was an easy addition based on how the argparse component was integrated so its nice to be able to quickly and independently test pparse commands.
