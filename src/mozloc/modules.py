import sys
import platform


if sys.platform == "win32":
    from .netsh import config_check, get_signal, scan_signal
elif sys.platform == "linux":
    from .netman import config_check, get_signal, scan_signal
elif sys.platform == "darwin":
    if tuple(map(int, platform.mac_ver()[0].split("."))) < (14, 4):
        from .airport import config_check, get_signal, scan_signal
    else:
        from .macos_corelocation import config_check, get_signal, scan_signal
else:
    raise ImportError(f"MozLoc doesn't work with platform {sys.platform}")


__all__ = ["config_check", "get_signal", "scan_signal"]
