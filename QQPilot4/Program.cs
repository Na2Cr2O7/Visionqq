using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace QQPilot4
{
    internal class Program
    {
        static void Main(string[] args)
        {
            //GUIOperation.Init();
            //GUIOperation.Click(3, 3);
            Console.OutputEncoding = Encoding.UTF8;


            //Console.WriteLine(AppDomain.CurrentDomain.BaseDirectory);

            //Focus.focus(false);
            Answer answer = new Answer();
            answer.Test();
        }
    }
}
