import sysDetect
if not sysDetect.isLinux():
    from messageBoxWindows import *
else:
    from messageBoxLinux import *