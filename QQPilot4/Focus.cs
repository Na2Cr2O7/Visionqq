using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;

namespace QQPilot4
{
    internal class Focus
    {
        [DllImport("FocusQQWindow2.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern int focus(bool flag);
    }
}
