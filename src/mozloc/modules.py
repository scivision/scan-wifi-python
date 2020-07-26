import sys

if sys.platform == "win32":
    from .netsh import cli_config_check, get_cli
elif sys.platform == "linux":
    from .netman import cli_config_check, get_cli
else:
    raise ImportError(f"MozLoc doesn't yet know how to work with platform {sys.platform}")
