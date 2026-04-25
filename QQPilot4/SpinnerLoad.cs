using System;
using System.Threading;
using System.Threading.Tasks;

namespace QQPilot4
{
    internal class SpinnerLoad
    {
        private static readonly string[] _spinner = { "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏" };
        private static volatile bool _loading = false;
        private static DateTime _startTime;

        /// <summary>
        /// 开始旋转加载动画
        /// </summary>
        /// <param name="ansiColorCode">ANSI 颜色代码，如 "\x1b[36m"（青色），可为空</param>
        /// <param name="text">要显示的提示文本</param>
        public static void Start(ConsoleColor c, string text = "加载中...")
        {
            _loading = true;
            _startTime = DateTime.Now;

            _ = Task.Run(() =>
            {
                int index = 0;
                while (_loading)
                {
                    string spinnerChar = _spinner[index % _spinner.Length];
                    Console.ForegroundColor = c;
                    string line = $"{spinnerChar} {text}\x1b[0m";
                    Console.ResetColor();

                    // 清除当前行并重写
                    Console.Write("\r" + new string(' ', Console.BufferWidth - 1) + "\r");
                    Console.Write(line);

                    index++;
                    Thread.Sleep(100); // 每 0.1 秒切换一帧
                }
            });
        }

        /// <summary>
        /// 停止加载动画，并输出耗时
        /// </summary>
        public static void Stop()
        {
            _loading = false;
            Thread.Sleep(50); // 确保动画线程退出

            var elapsed = (DateTime.Now - _startTime).TotalSeconds;
            Console.WriteLine($"\n✅ 完成！用时: {elapsed:F2} 秒\n");
        }

    }
}