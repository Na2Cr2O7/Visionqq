using System;
using System.Collections.Generic;
using System.Text;

namespace QQPilot4
{
    internal class UploadContent
    {
        public string? Text { get; set; }
        public List<string> Images { get; set; }
        public static implicit operator UploadContent(string? text)
        {
            return new UploadContent(text);
        }
        public UploadContent(string? text, List<string> images)
        {
            Text = text;
            Images = images;
        }
        public UploadContent(string? text)
        {
            Text = text;
            Images = [];
        }
        public List<string> Absolute()
        {
             List<string> result = [];
            foreach (var image in Images)
            {
                result.Add(Path.GetFullPath(image));
            }
            return result;
        }
        public override string? ToString() => Text;
    }
}
