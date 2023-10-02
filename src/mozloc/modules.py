import sys


match sys.platform:
    case "win32":
        from .netsh import cli_config_check, get_signal, parse_signal
    case "linux":
        from .netman import cli_config_check, get_signal, parse_signal
    case "darwin":
        from .airport import cli_config_check, get_signal, parse_signal
    case _:
        raise ImportError(f"MozLoc doesn't work with platform {sys.platform}")


__all__ = ["cli_config_check", "get_signal", "parse_signal"]
