import os
from pathlib import Path
from importlib import resources

PCI_SYSFS = Path("/sys/bus/pci/devices")


def read_hex(path: Path) -> int:
    return int(path.read_text().strip(), 16)


def load_pci_ids():
    vendors = {}
    current_vendor = None

    # The following files are local copies of:
    # - /usr/share/misc/pci.ids
    # - /usr/share/hwdata/pci.ids
    # TODO: Access these as package resources
    for path in ["misc-pci.ids", "hwdata-pci.ids"]:
        #if not path.exists():
        #    continue

        with resources.open_text('thirdparty.yannt.sysscan.data', path) as f:
            for line in f:
                if not line.strip() or line.startswith("#"):
                    continue

                if not line.startswith("\t"):
                    vid, name = line.strip().split(None, 1)
                    vendors[vid.lower()] = {
                        "name": name,
                        "devices": {},
                    }
                    current_vendor = vid.lower()
                elif current_vendor:
                    did, name = line.strip().split(None, 1)
                    vendors[current_vendor]["devices"][did.lower()] = name

        # Consider using both ids files?
        break

    return vendors


def pci_class_is_gpu(cls: int) -> bool:
    base = cls >> 16
    return base == 0x03  # Display controller (VGA, 3D, etc)


def kernel_driver(dev: Path):
    driver = dev / "driver"
    if driver.is_symlink():
        return driver.resolve().name
    return None


def scan_gpus():
    pci_ids = load_pci_ids()
    gpus = []

    for dev in PCI_SYSFS.iterdir():
        try:
            cls = read_hex(dev / "class")
        except FileNotFoundError as e:
            print(f"Failed to read class: {e}")
            continue

        if not pci_class_is_gpu(cls):
            continue

        try:
            vendor = read_hex(dev / "vendor")
            device = read_hex(dev / "device")

            vendor_hex = f"{vendor:04x}"
            device_hex = f"{device:04x}"

            vendor_name = pci_ids.get(vendor_hex, {}).get("name", "Unknown Vendor")
            device_name = pci_ids.get(vendor_hex, {}).get("devices", {}).get(
                device_hex, "Unknown Device"
            )

            gpus.append({
                "pci_address": dev.name,
                "vendor_id": vendor_hex,
                "device_id": device_hex,
                "vendor": vendor_name,
                "device": device_name,
                "class": f"{cls:06x}",
                "kernel_driver": kernel_driver(dev),
            })
        except Exception as e:
            print(f"Failed to get GPU hw data: {e}")
            continue

    return gpus


def is_out_of_tree(modname):
    KMOD_ROOT = Path("/lib/modules") / os.uname().release
    for base in ("updates", "extra", "weak-updates"):
        root = KMOD_ROOT / base
        if root.exists():
            if any(root.rglob(f"{modname}.ko*")):
                return True
    return False

def sus_gpu_driver(modname):
    PREFIXES = (
        "nvidia", "vmw", "vbox",  "wl", "amdgpu", "amdocl",
        "mlx", "r8168", "rtl", "hisi", "npu", "ascend", "davinci",
        "hanguang", "hg_accel", "ali_npu", "xpu", "kunlun", "baidu_npu",
        "cambricon", "mlu", "cn_device", "biren", "brgpu", "br_accel",
        "musa"
    )

    if modname.startswith(PREFIXES):
        return True
    if is_out_of_tree(modname):
        return True


def read_loaded_modules():
    modules = []
    with open("/proc/modules") as f:
        for line in f:
            parts = line.split()
            desc = {
                "name": parts[0],
                "size": int(parts[1]),
                "refcount": int(parts[2]),
                "deps": [] if parts[3] == "-" else parts[3].split(","),
                "state": parts[4],
            }
            modules.append(desc)
    return modules

def kernel_taint_flags():
    taint = int(Path("/proc/sys/kernel/tainted").read_text().strip())
    flags = []
    if taint & 1:
        flags.append("PROPRIETARY_MODULE")
    if taint & 8:
        flags.append("OUT_OF_TREE")
    return flags
