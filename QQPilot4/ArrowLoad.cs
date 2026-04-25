using System;
using System.Threading;
using System.Threading.Tasks;

namespace QQPilot4
{
    internal class ArrowLoad
    {
        private static bool _loading = false;
        private static DateTime _startTime;
        private static readonly string[] _spinner = { "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏" };
        private static readonly string[] _progressBar;

        // 静态构造器：初始化进度条动画帧
        static ArrowLoad()
        {
            var forward = new[]
            {
                "[->                         ]",
                "[-->                        ]",
                "[ <-->                      ]",
                "[  <-->                     ]",
                "[    <-->                   ]",
                "[      <-->                 ]",
                "[        <-->               ]",
                "[          <-->             ]",
                "[            <-->           ]",
                "[              <-->         ]",
                "[                <-->       ]",
                "[                  <-->     ]",
                "[                    <-->   ]",
                "[                      <--> ]",
                "[                        <--]",
                "[                         <-]"
            };

            var backward = new string[forward.Length - 2]; // 去掉首尾避免重复
            for (int i = forward.Length - 2; i >= 1; i--)
            {
                backward[forward.Length - 2 - i] = forward[i];
            }

            _progressBar = new string[forward.Length + backward.Length];
            Array.Copy(forward, _progressBar, forward.Length);
            Array.Copy(backward, 0, _progressBar, forward.Length, backward.Length);
        }

        /// <summary>
        /// 开始加载动画
        /// </summary>
        /// <param name="ansiColorCode">ANSI 颜色代码，例如 "\x1b[32m"（绿色），留空则无色</param>
        /// <param name="text">显示的文本</param>
        public static void StartLoading(ConsoleColor color, string text)
        {
            _loading = true;
            _startTime = DateTime.Now;

            // 启动后台线程运行动画
            _ = Task.Run(() =>
            {
                int spinnerIndex = 0;
                int barIndex = 0;
                while (_loading)
                {
                    string bar = _progressBar[barIndex % _progressBar.Length];
                    string spinnerChar = _spinner[spinnerIndex % _spinner.Length];

                    // 构造带颜色的行（\r 回车覆盖当前行）
                    Console.BackgroundColor = color;
                    string line = $"{spinnerChar}{bar}\t{text}";
                    Console.ResetColor();

                    Console.Write("\r" + new string(' ', Console.BufferWidth - 1) + "\r"); // 清除当前行
                    Console.Write(line);

                    spinnerIndex++;
                    barIndex++;
                    Thread.Sleep(100); // 0.1 秒
                }
            });
        }

        /// <summary>
        /// 停止加载动画并输出耗时
        /// </summary>
        public static void StopLoading()
        {
            _loading = false;
            Thread.Sleep(100); // 等待动画线程退出（可选）

            var elapsed = (DateTime.Now - _startTime).TotalSeconds;
            Console.WriteLine($"\n用时: {elapsed:F2}s");
            Console.WriteLine();
        }

    }
}