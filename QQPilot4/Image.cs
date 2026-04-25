using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;
using IniParser;

namespace QQPilot4
{
    // === 结构体定义 ===
    [StructLayout(LayoutKind.Sequential)]
    public struct Point
    {
        public uint x;
        public uint y;

        public override string ToString() => $"Point(x={x}, y={y})";

        public bool IsNull() => x == 0 && y == 0;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct RECT
    {
        public uint left;
        public uint top;
        public uint right;
        public uint bottom;

        public override string ToString() =>
            $"RECT(left={left}, top={top}, right={right}, bottom={bottom})";
    }

    // === DLL 导入 ===
    internal static class NativeMethods
    {
        private const string VisionDll = "Vision.dll";
        private const string ScreenCaptureDll = "ScreenCapture.dll";

        // ScreenCapture.dll 函数
        [DllImport(ScreenCaptureDll, CallingConvention = CallingConvention.Cdecl)]
        public static extern int screenshot(int x, int y, int width, int height);

        [DllImport(ScreenCaptureDll, CallingConvention = CallingConvention.Cdecl)]
        public static extern int fullScreenshot();

        // Vision.dll 函数
        [DllImport(VisionDll, CallingConvention = CallingConvention.Cdecl)]
        public static extern Point containsRedDot(RECT rect, byte[] imagePath);

        [DllImport(VisionDll, CallingConvention = CallingConvention.Cdecl)]
        public static extern Point containsBlue(byte[] imagePath);

        [DllImport(VisionDll, CallingConvention = CallingConvention.Cdecl)]
        public static extern Point point(uint x, uint y);

        [DllImport(VisionDll, CallingConvention = CallingConvention.Cdecl)]
        public static extern RECT rect(uint x, uint y, uint width, uint height);

        [DllImport(VisionDll, CallingConvention = CallingConvention.Cdecl)]
        public static extern int matchTemplatesMultiScaleBegin(
            byte[] imageBytes,
            byte[] templateBytes,
            int tolerance,
            int maxCount);

        [DllImport(VisionDll, CallingConvention = CallingConvention.Cdecl)]
        public static extern Point matchTemplateNext(int index);

        [DllImport(VisionDll, CallingConvention = CallingConvention.Cdecl)]
        public static extern void matchTemplateEnd();
    }

    // === 主逻辑类 ===
    internal class Image
    {
        private static readonly float Width;
        private static readonly float Height;
        private static readonly float Scale;

        static Image()
        {
            var parser = new FileIniDataParser();
            var data = parser.ReadFile("config.ini", Encoding.UTF8);
            Width = int.Parse(data["general"]["width"]);
            Height = int.Parse(data["general"]["height"]);
            Scale = float.Parse(data["general"]["scale"]);
        }

        // 封装函数
        public static RECT Rect(uint x, uint y, uint width, uint height)
            => NativeMethods.rect(x, y, width, height);

        public static Point Point(uint x, uint y)
            => NativeMethods.point(x, y);

        public static bool Screenshot(int x, int y, int width, int height)
        {
            int result = NativeMethods.screenshot(x, y, width, height);
            return result != 1; // 返回 1 表示失败
        }
        public static bool Screenshot((int,int,int,int) area)
        {
            return Screenshot(area.Item1,area.Item2,area.Item3,area.Item4);
        }
        public static bool FullScreenShot()
        {
            int result = NativeMethods.fullScreenshot();
            return result != 1;
        }

        public static (uint x, uint y) ContainsRedDot(RECT rect)
        {
            var pt = NativeMethods.containsRedDot(rect, Encoding.UTF8.GetBytes("screenshot.png"));
            return (pt.x, pt.y);
        }

        public static (uint x, uint y) ContainsBlue()
        {
            var pt = NativeMethods.containsBlue(Encoding.UTF8.GetBytes("screenshot.png"));
            return (pt.x, pt.y);
        }

        public static List<(uint x, uint y)> FindTemplates(
            string imagePath,
            string templatePath,
            int tolerance = 30,
            int maxCount = 1)
        {
            byte[] imgBytes = Encoding.UTF8.GetBytes(imagePath);
            byte[] tplBytes = Encoding.UTF8.GetBytes(templatePath);

            int count = NativeMethods.matchTemplatesMultiScaleBegin(imgBytes, tplBytes, tolerance, maxCount);

            if (count < 0)
            {
                NativeMethods.matchTemplateEnd();
                string msg = count switch
                {
                    -1 => "大图尺寸小于模板图尺寸",
                    -2 => $"无法加载大图: {imagePath}",
                    -3 => $"无法加载模板图: {templatePath}",
                    _ => $"未知错误代码: {count}"
                };
                throw new InvalidOperationException(msg);
            }

            var results = new List<(uint x, uint y)>();
            for (int i = 0; i < count; i++)
            {
                Point pt = NativeMethods.matchTemplateNext(i);
                results.Add((pt.x, pt.y));
            }

            NativeMethods.matchTemplateEnd();
            return results;
        }

        internal static RECT Rect(int item1, int item2, int item3, int item4)
        {
            return Rect((uint)item1, (uint)item2, (uint)item3, (uint)item4);
        }
        internal static RECT Rect((int,int,int,int) Pos)
        {
            return Rect((uint)Pos.Item1, (uint)Pos.Item2, (uint)Pos.Item3, (uint)Pos.Item4);
        }
    }
}