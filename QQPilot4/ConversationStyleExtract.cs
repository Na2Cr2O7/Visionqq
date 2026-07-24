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
            string[] lines = chatStr.Split(new[] { "\r\n", "\r", "\n" }, StringSplitOptions.None);
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
        //public static Func<string, List<ChatContent>> Extract = ParseChatLog;
    }
}