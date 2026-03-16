import os

def get_distro():
    """Detects the Linux distribution."""
    if not os.path.exists("/etc/os-release"):
        return "unknown"
    
    distro_info = {}
    with open("/etc/os-release", "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.rstrip().split("=", 1)
                distro_info[key] = value.strip('"')
    
    return distro_info.get("ID", "unknown").lower()

def get_package_manager(distro=None):
    """Returns the package manager for the given distro."""
    if distro is None:
        distro = get_distro()
    
    pm_map = {
        "ubuntu": "apt",
        "debian": "apt",
        "fedora": "dnf",
        "centos": "dnf",
        "rhel": "dnf",
        "arch": "pacman",
        "manjaro": "pacman",
    }
    
    return pm_map.get(distro, "apt") # Default to apt if unknown
