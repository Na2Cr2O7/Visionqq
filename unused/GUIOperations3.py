import sysDetect
if not sysDetect.isLinux():
    from GUIOperations2 import * #Windows
else:
    from GUIOperationLinux import *
