using System;
using System.Runtime.InteropServices;
using System.Text;

namespace Opt
{
    public class IniFile(string path)
    {
        private string filePath = path;
        [DllImport("kernel32", CharSet = CharSet.Unicode)]
        private static extern long WritePrivateProfileString(string section, string key, string value, string filePath);
        [DllImport("kernel32", CharSet = CharSet.Unicode)]
        private static extern int GetPrivateProfileString(string section, string key, string defaultValue, StringBuilder returnValue, int size, string filePath);

        public void Write(string section, string key, string value)
        {
            WritePrivateProfileString(section, key, value, filePath);
        }
        public string Read(string section, string key)
        {
            var returnValue = new StringBuilder(255);
            GetPrivateProfileString(section, key, "", returnValue, 255, filePath);
            return returnValue.ToString();
        }
    }
}
