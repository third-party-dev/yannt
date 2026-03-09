# Yet Another Neural Network Tool (yannt)

## Purpose

Yet Another Neural Network Tool (yannt) aims to provide an analysis framework for deeper understanding of the anatomy of AI technologies in use.

yannt itself is a light CLI wrapper and command line framework. In other words, none of the actual work mentioned above is performed by the top level yannt python package. Instead you must install yannt plugins inside the same python (virtual) environment. The plugins themselves become subcommands of the top-level yannt command with their own arguments and handlers.

This fractured design was a deliberate decision to allow a minimal viable install for a user's specific use case. Minimal functionality can often be desired when dealing with very large dependencies (pytorch+cuda) or frustratingly unintelligent dependency management (tensorflow).

## PParse (as in "partial parser")

From strictly a user perspective, yannt is a single point of entry for discovering and using the plugins installed into the python environment. The most important of these plugins is the `pparse` plugin. Pparse is its own python package and has its own dependencies, plugins, and documentation, but its worth noting here that pparse is the heart of a lot of yannt's functionality. `pparse` aims to:

- Enable parsing of very large files (model files) that do not fit on a single machine's memory.
- Parse model files independent of the upstream frameworks. For example, not executing pickle when parsing a PyTorch file.
- Parse model files that have been truncated (corrupted). In this context, pparse aims to parse up to the point where the file becomes invalid and keeps all of the parsed state to that point without crashing. (Quite annoying when you know a piece of software has 90% of the file and dies because it can't verify something I never asked it to verify!)

When installing `thirdparty.pparse` into a python environment, it enables:

- `import thirdparty.pparse.lib as pparse` - First and foremost, pparse is a python library that is designed to be imported and used by other python code.

- `yannt pparse [pparse-command] [options] [args]` - For CLI actions, its recommended to use yannt as the entrypoint. The CLI is primary intended for common task execution, data preparation, and user demonstration purposes. (You get all of the power of the tools with your own python scripts, but sometimes you just want to copy paste some commands to get what you need.)

- `pparse [pparse-command] [options] [args]` - For systems that are confident they only need pparse, you can install pparse by itself, without yannt. This was an easy addition based on how the argparse component was integrated so its nice to be able to quickly and independently test pparse commands.

Note: A primary reason for keeping yannt separate from pparse is because pparse is a more generic parsing philosophy that can be used well beyond the scope of ML artifact parsing. In contrast, yannt keeps the focus to AI/ML related artifacts.









