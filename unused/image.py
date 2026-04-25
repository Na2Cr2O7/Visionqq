import sysDetect
if not sysDetect.isLinux():
    from imageWin import *
else:
    from imageLinux import *
