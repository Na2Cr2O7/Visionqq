using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;

namespace QQPilot4
{
    internal class DockLog
    {
        public static void Log2(string s)
        {
            try
            {
                File.WriteAllText("dockLog.txt", s);

            }
            catch (Exception e)
            {
                Log.Print(e.ToString());
            }

        }
        public static void Init()
        {
            try
            {
                var p = Process.Start("DockLog3.exe");
            }
            catch (Exception e)
            {
                {
                    Log.Print(e.ToString(), Log.Stat.ERROR);
                }
            }
        }
        public static void Exit()
        {
            Log2("EXIT");
        }
    }
}
