
import os

def find_files(root):
    seen_inodes = set()

    def _walk(path):
        if any(path.startswith(v) for v in ("/proc", "/sys", "/dev")):
            return

        try:
            for entry in os.scandir(path):
                try:
                    stat = entry.stat(follow_symlinks=True)
                except FileNotFoundError:
                    # Happens when links are broken
                    continue

                inode = (stat.st_ino, stat.st_dev)
                if inode in seen_inodes:
                    continue
                seen_inodes.add(inode)

                yield entry.path

                if entry.is_dir(follow_symlinks=True):
                    yield from _walk(entry.path)

        except PermissionError:
            # TODO: Account for skipped paths?
            pass
        except OSError:
            # Happens when: "[Errno 40] Too many levels of symbolic links"
            pass

    yield from _walk(os.path.abspath(root))
