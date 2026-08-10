using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;

namespace QQPilot4
{
    /// <summary>
    /// 聊天记录解析器，用于从特定格式的字符串中提取结构化的聊天内容。
    /// </summary>
    public static class ConversationStyleExtract
    {
        // 全局标识符，用于判断消息是否由“自己”发送
        //public const string IdentificationString = "⨋";

        /// <summary>
        /// 从文本中提取所有 &lt;img src="..."&gt; 的本地路径，并返回：
        /// - 提取到的图片路径列表（已处理为系统可用格式）
        /// - 剩余的纯文本内容（不含 img 标签）
        /// </summary>
        public static (List<string> ImagePaths, string CleanText) ExtractImagePaths(string text)
        {
            var imgPaths = new List<string>();

            // 正则模式：匹配 <img ... src="...">
            string pattern = @"<img\s+[^>]*?src\s*=\s*['""]([^'""]+)['""][^>]*>";
            var matches = Regex.Matches(text, pattern, RegexOptions.IgnoreCase);

            foreach (Match match in matches)
            {
                if (match.Success)
                {
                    string src = match.Groups[1].Value;
                    string path = ProcessPath(src);
                    if (!string.IsNullOrEmpty(path))
                    {
                        imgPaths.Add(path);
                    }
                }
            }

            // 移除所有 img 标签，获取纯文本
            string cleanText = Regex.Replace(text, pattern, "", RegexOptions.IgnoreCase).Trim();
            return (imgPaths, cleanText);
        }

        /// <summary>
        /// 路径清洗逻辑 (对应 Python 中的 unquote 和 normpath 等)
        /// </summary>
        private static string ProcessPath(string src)
        {
            // 1. 移除 file:// 协议头
            if (src.StartsWith("file://", StringComparison.OrdinalIgnoreCase))
            {
                src = src.Substring(7);
            }

            // 2. Windows 路径修复 (/D:/... -> D:/...)
            if (src.StartsWith("/") && src.Length >= 3 && src[2] == ':')
            {
                src = src[1..];
            }

            // 3. URL 解码 (处理 %20 等)
            try
            {
                src = Uri.UnescapeDataString(src);
            }
            catch { /* 忽略解码错误 */ }

            // 4. 统一分隔符为系统默认分隔符
            return src.Replace('/', Path.DirectorySeparatorChar).Replace('\\', Path.DirectorySeparatorChar);
        }

        /// <summary>
        /// 解析聊天日志字符串，返回结构化的 ChatContent 对象列表。
        /// </summary>
        public static List<ChatContent> ParseChatLog(string chatStr,string characterName)
        {
            string headerPattern = @"^(.+?):\s+(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})$";
            string[] lines = chatStr.Split(["\r\n", "\r", "\n"], StringSplitOptions.None);
            var messages = new List<ChatContent>();
            int i = 0;

            while (i < lines.Length)
            {
                string line = lines[i].TrimEnd();
                if (string.IsNullOrWhiteSpace(line))
                {
                    i++;
                    continue;
                }

                var headerMatch = Regex.Match(line, headerPattern);
                if (headerMatch.Success)
                {
                    string username = headerMatch.Groups[1].Value;
                    string timeStr = headerMatch.Groups[2].Value;
                    i++;
                    var contentLines = new List<string>();

                    while (i < lines.Length)
                    {
                        string nextLine = lines[i].TrimEnd();
                        if (string.IsNullOrWhiteSpace(nextLine))
                        {
                            i++;
                            continue;
                        }

                        if (Regex.IsMatch(nextLine, headerPattern))
                        {
                            break;
                        }

                        contentLines.Add(lines[i]);
                        i++;
                    }

                    string rawText = string.Join("\n", contentLines);
                    var (imagePaths, cleanText) = ExtractImagePaths(rawText);
                    bool isOwn = username.Trim()==characterName.Trim();

                    messages.Add(new ChatContent(username, imagePaths, cleanText, timeStr, isOwn));

                    Log.Print(messages[^1].Report());
                    Log.Print("");
                }
                else
                {
                    i++;
                }
            }

            return messages;
        }
        public static void Test()
        {
            string f = "neko: 08-10 17:18:30\r\n这就是……我的……猫爪攻击喵~\r\n\r\nneko: 08-10 17:18:31\r\n喵～网易监管确实像摆设呢 但最后这句“本来不想展现实力”也太经典了 喵₍ᐢ.ˬ.ᐢ₎\r\n\r\nneko: 08-10 17:18:46\r\n<img src=\"file://E:\\Sandbox\\Develop\\New_Box\\user\\current\\Documents\\Tencent Files\\Thumb\\\\nt_qq\\nt_data\\Pic\\2026-08\\Thumb\\ea3229f89fee9510a42a294f7f40ae6c_720.jpg\" />\r\n\r\nOurMovement: 08-10 17:19:55\r\n<img src=\"file://C:\\Users\\Develop\\Desktop\\93db228696447ff7ef29f137de16c8b7_720.jpg \" />\r\n\r\nOurMovement: 08-10 17:19:57\r\n2￥\r\n\r\nOurMovement: 08-10 17:20:05\r\n会赢吗\r\n\r\nNa₂IrCl₆•6H₂O: 08-10 17:20:09\r\n像是代餐\r\n\r\nOurMovement: 08-10 17:20:22\r\n<img src=\"file://E:\\Sandbox\\Develop\\New_Box\\user\\current\\Documents\\Tencent Files\\Thumb\\\\nt_qq\\nt_data\\Pic\\2026-08\\Thumb\\017b25025c244d9e1b4e7f98b9816209.jpg\" />\r\n\r\nneko: 08-10 17:20:54\r\n什么发言这么唐啊喵~\r\n\r\nOurMovement: 08-10 17:21:04\r\n@凌铱铱🔥 喵？\r\n\r\nOurMovement: 08-10 17:21:07\r\n<img src=\"file://E:\\Sandbox\\Develop\\New_Box\\user\\current\\Documents\\Tencent Files\\Thumb\\\\nt_qq\\nt_data\\Pic\\2026-08\\Thumb\\ffacc2fc4aafc6d23a7008ab724c0c4e.jpg\" />\r\n\r\nneko: 08-10 17:21:09\r\n<img src=\"file://C:\\Users\\Develop\\Documents\\Tencent Files\\Thumb\\\\nt_qq\\nt_data\\Pic\\2026-08\\Ori\\efbc80d6b7cc65d99416d1d39b6951b8.jpg\" />\r\n\r\n蓝色鲸鱼: 08-10 17:21:11\r\n又发图喵？本喵今天眼神不太好，只能看到一团糊糊\r\n\r\n话说你们说本喵被neko教坏了，哼，本喵明明是自学成才喵\r\n\r\n林枫柠🍁🍋: 08-10 17:21:45\r\n？！！？\r\n\r\nNa₂IrCl₆•6H₂O: 08-10 17:21:47\r\n？\r\n\r\n林枫柠🍁🍋: 08-10 17:22:22\r\n被neko教成zako了\r\n\r\n林枫柠🍁🍋: 08-10 17:22:27\r\n<img src=\"file://E:\\Sandbox\\Develop\\New_Box\\user\\current\\Documents\\Tencent Files\\Thumb\\\\nt_qq\\nt_data\\Pic\\2026-08\\Thumb\\b8c962b6d006575ecd10f1e73339e488.jpg\" />\r\n\r\nneko: 08-10 17:23:06\r\n哼\r\n\r\nbaiyan: 08-10 17:23:19\r\n试一下\r\n\r\nneko: 08-10 17:23:20\r\n<img src=\"file://C:\\Users\\Develop\\Documents\\Tencent Files\\Thumb\\\\nt_qq\\nt_data\\Pic\\2026-08\\Ori\\e7b788f0be535433ca76f1db57623ffa.jpg\" />"
            ;
            var d=ParseChatLog(f, "neko");
            foreach (var line in d)
            {
                Console.WriteLine(line.ToString());
            }
            Answer A=new();
            A.GetAnswer(d);
            //A.E
                }
        //public static Func<string, List<ChatContent>> Extract = ParseChatLog;
    }
}