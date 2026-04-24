using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace QQPilot
{
    public class ChatContent
    {
        // 属性定义
        public string Username { get; set; } = string.Empty;
        public List<string> ImagePaths { get; set; } = new List<string>();
        public string Text { get; set; } = string.Empty;
        public string Time { get; set; } = string.Empty;
        public bool OwnByMyself { get; set; } = false;

        // 构造函数
        public ChatContent(string username, List<string> imagePaths, string text, string time, bool ownByMyself)
        {
            Username = username;
            ImagePaths = imagePaths;
            Text = text;
            Time = time;
            OwnByMyself = ownByMyself;
        }

        // 生成报告的方法
        // 逻辑：检查文件是否存在，格式化输出
        public string Report()
        {
            // 1. 前缀标记
            string prefix = OwnByMyself ? "[你]" : "";

            // 2. 文本处理 (空内容显示为【空】)
            string content = string.IsNullOrEmpty(Text) ? "【空】" : Text;

            // 3. 图片有效性检查 (核心逻辑移植)
            // 筛选出真实存在于硬盘上的图片路径
            var validImages = ImagePaths.Where(path => File.Exists(path)).ToList();

            string imagePart;
            if (validImages.Any())
            {
                // 将路径列表转换为字符串表示形式，例如 ["path1", "path2"]
                imagePart = "[ " + string.Join(", ", validImages.Select(p => $"\"{p}\"")) + " ]";
            }
            else
            {
                imagePart = "无";
            }

            return $"{prefix}{Username}: {content}\n{Time}\n 图片：{imagePart}";
        }

        // 重写 ToString 方法
        public override string ToString()
        {
            string content = string.IsNullOrEmpty(Text) ? "【空】" : Text;

            if (!OwnByMyself)
            {
                return $"{Username}:{content}";
            }
            else
            {
                return content;
            }
        }
    }
}