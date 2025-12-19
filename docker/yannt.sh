#!/bin/sh

set -e

HOST_PWD="$(realpath "$(pwd)")"
CONTAINER_PWD="/host${HOST_PWD}"


# Detect absolute paths not starting with /host
abs_paths=""
for arg in "$@"; do
    case "$arg" in
        /*)
            case "$arg" in
                /host/*)
                    ;;
                *)
                    # Missing /host
                    if [ -z "$abs_paths" ]; then
                        abs_paths="$arg"
                    else
                        abs_paths="$abs_paths $arg"
                    fi
                    ;;
            esac
            ;;
    esac
done


# Allow user to continue without prefix.
if [ ! -z "$abs_paths" ]; then
  echo
  echo "The following (presumed) paths are not prefixed with '/host'"
  for path in "$abs_paths"; do
    echo "- $path"
  done
  echo
  echo "Because of the way yannt is packaged in Docker, you must prefix"
  echo "all absolute paths with '/host'."
  echo
  echo "For example, the path '/home/user/mymodel.safetensors' must be"
  echo "given as '/host/home/user/mymodel.safetensors'."
  echo 
  echo "Do you want to continue without changes? [Y/n] \c"
  read ans
  if [ -z "$ans" ] || [ "$ans" = "Y" ] || [ "$ans" = "y" ]; then
      echo "Continuing..."
  else
      echo "Aborting."
      exit 1
  fi
fi


# Run it in docker!
docker run -ti --rm \
  -v /:/host \
  -w "$CONTAINER_PWD" \
  -u $(id -u):$(id -g) \
  yannt "$@"
