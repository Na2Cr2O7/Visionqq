using System.Text;

namespace QQPilot
{
    public class QQPilot
    {
        public static int Main(string[] args)
        {
            Console.OutputEncoding = Encoding.UTF8;


            Console.WriteLine(AppDomain.CurrentDomain.BaseDirectory);
    
            Focus.focus(false);
            return 0;
        }
    }
}