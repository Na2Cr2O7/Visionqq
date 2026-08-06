using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;

namespace QQPilot4
{
    public class ChatContent(string username, List<string> imagePaths, string text, string time, bool ownByMyself)
    {
        // 属性定义
        public string Username { get; set; } = username;
        public List<string> ImagePaths { get; set; } = imagePaths;
        public string Text { get; set; } = text;
        public string Time { get; set; } = time;
        public bool OwnByMyself { get; set; } = ownByMyself;
        public bool Empty { get;
             private set; } = false;

        // 生成报告的方法
        // 逻辑：检查文件是否存在，格式化输出
        public string Report()
        {
            // 1. 前缀标记
            string prefix = OwnByMyself ? "[你]" : "";

            // 2. 文本处理 
            string content = string.IsNullOrEmpty(Text) ? "" : Text;

            
            // 3. 图片有效性检查 (核心逻辑移植)
            // 筛选出真实存在于硬盘上的图片路径
            var validImages = ImagePaths.Where(path => File.Exists(path)).ToList();

            string imagePart;
            if (validImages.Count != 0)
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
            try
            {
                Empty = string.IsNullOrEmpty(Text);
                string content = string.IsNullOrEmpty(Text) ? "" : Text;
                if (string.IsNullOrEmpty(Time))
                {
                    Time = DateTime.Now.ToString("MM-dd HH:mm:ss");
                }
                if (OwnByMyself)
                {
                    // 空文本时直接返回，避免 content[..^1] 因长度 0 产生负数长度异常
                    return content.Length == 0 ? "" : content[..^1];
                }
                else
                {
                    //Unc unc=new();
                    //unc.Username = Username;
                    //unc.Content=content;
                    //string serialized=JsonSerializer.Serialize(unc);
                    //Console.WriteLine(serialized);
                    ;
                    return $"[time]\n{Time} \n\n [username] \n {Username} \n\n [content] \n {content}\n";
                }
            }
            catch (Exception ex)
            {
                Log.Print(ex.ToString(), Log.Stat.ERROR);
                return "";
            }

        }
    }
    //public class Unc()
    //{
    //    public string Username{ get; set; }
    //    public string Content { get; set; }
    //}
}