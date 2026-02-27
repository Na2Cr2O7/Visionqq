import sysDetect
if not sysDetect.isLinux():
    import ctypes
    import os
    dll=ctypes.CDLL(os.path.abspath('uploadFile.dll'))
    def upload():
        return dll.upload()
