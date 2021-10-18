import sys

if sys.platform == "win32":
    from .netsh import cli_config_check, get_signal, parse_signal
elif sys.platform == "linux":
    from .netman import cli_config_check, get_signal, parse_signal
elif sys.platform == "darwin":
    from .airport import cli_config_check, get_signal, parse_signal
else:
    raise ImportError(f"MozLoc doesn't work with platform {sys.platform}")
