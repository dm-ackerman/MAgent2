""" some utility for call C++ code"""


import ctypes
import multiprocessing
import os
import platform


def _load_lib():
    """Load library in local."""
    cur_path = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
    lib_path = cur_path
    if platform.system() == "Darwin":
        import sysconfig

        filename = f"libmagent.{sysconfig.get_config_var('SOABI')}.dylib"
        path_to_so_file = os.path.join(lib_path, filename)
    elif platform.system() == "Linux":
        import sysconfig

        filename = f"libmagent.{sysconfig.get_config_var('SOABI')}.so"
        path_to_so_file = os.path.join(lib_path, filename)
    elif platform.system() == "Windows":
        path_to_so_file = os.path.join(lib_path, "magent.dll")
    else:
        raise BaseException("unsupported system: " + platform.system())

    if not os.path.exists(path_to_so_file):
        raise FileNotFoundError(f"Could not find the DLL file at: {path_to_so_file}")

    lib = ctypes.CDLL(path_to_so_file, ctypes.RTLD_GLOBAL)
    return lib


def as_float_c_array(buf):
    """numpy to ctypes array"""
    return buf.ctypes.data_as(ctypes.POINTER(ctypes.c_float))


def as_int32_c_array(buf):
    """numpy to ctypes array"""
    return buf.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))


def as_bool_c_array(buf):
    """numpy to ctypes array"""
    return buf.ctypes.data_as(ctypes.POINTER(ctypes.c_bool))


if "OMP_NUM_THREADS" not in os.environ:
    os.environ["OMP_NUM_THREADS"] = str(multiprocessing.cpu_count() // 2)
_LIB = _load_lib()
