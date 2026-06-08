using System;
using System.Collections.Generic;
using System.Text;

namespace QQPilot4
{
    internal class Log
    {
        public enum Stat
        {
            NORMAL,WARN,ERROR
        }
        public static void Print(string target,Stat stat=Stat.NORMAL)
        {
            DateTime dt = DateTime.Now;
            string output = $"[{dt:t}]{target}";
            switch(stat)
            {
                case Stat.NORMAL:
                    break;
                case Stat.WARN:
                    output = "[WARN]"+output;
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    break;
                case Stat.ERROR:
                    output = "[ERR]"+output;
                    Console.ForegroundColor = ConsoleColor.Red;
                    break;
                default:
                    break;
            }
            Console.WriteLine(output);
            File.AppendAllText("log.txt", output+"\n");
            Console.ResetColor();
        }

    }
}
