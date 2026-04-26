import ctypes
awareness = ctypes.c_int()
errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
# print(awareness.value)
errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(1)
if errorCode!= 0:
    print("SetProcessDpiAwareness failed with error code %d" % errorCode)