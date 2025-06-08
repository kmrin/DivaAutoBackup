import os
import sys
import traceback


def format_exception(e: Exception) -> str:
    path, line, _, _ = traceback.extract_tb(e.__traceback__)[-1]
    path = os.path.basename(path)
    
    return f"{type(e).__name__} [{path} | {line}] -> {str(e)}"


def get_base_path(external: bool = False) -> str:
    if hasattr(sys, '_MEIPASS'):
        if external:
            return os.path.dirname(sys.executable)
        else:
            return sys._MEIPASS
    
    return os.path.join(os.path.dirname(__file__), "..")