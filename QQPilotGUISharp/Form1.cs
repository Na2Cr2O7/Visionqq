using IniParser;
using IniParser.Model;
using System.Text;

namespace QQPilotGUISharp
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        ~Form1()
        {
            SaveConfig();

        }
        IniParser.FileIniDataParser parser;
        private void button1_Click(object sender, EventArgs e)
        {
            Text = "12314567";
        }
        public void SaveConfig()
        {
            // 创建或加载 INI 文件
            var parser = new FileIniDataParser();
            IniData ini;
            if (File.Exists("config.ini"))
            {
                ini = parser.ReadFile("config.ini", new UTF8Encoding(false));
            }
            else
            {
                ini = new IniData();
            }

            // 获取或创建 [general] 节
            var general = ini["general"];
            if (general == null)
            {
                ini.Sections.AddSection("general");
                general = ini["general"];
            }

            // 保存各个字段
            general["version"] = vname.Text;
            general["width"] = winWidth.Value.ToString();
            general["height"] = winHeight.Value.ToString();
            general["maximagecount"] = MaxImageCount.Value.ToString();
            general["modelname"] = ModelName.Text;
            general["isvisionmodel"] = IsVisionModel.Checked.ToString().ToLower();
            general["api_key"] = APIKey.Text;
            general["server_url"] = ServerUrl.Text; // 注意：这里直接保存文本框内容，而不是下拉框索引
            general["scroll"] = Scroll.Value.ToString();
            general["withimage"] = WithImage.Checked.ToString().ToLower();
            general["autologin"] = AutoLogin.Checked.ToString().ToLower();
            general["autofocusing"] = AutoFocusing.Checked.ToString().ToLower();
            general["sendimagepossibility"] = SendImagePossibility.Value.ToString();
            general["atdetect"] = ATDetect.Checked.ToString().ToLower();
            general["remote_server_timeout"] = RemoteServerTimeout.Value.ToString();

            // tab_times 只允许 7 或 8
            int tabTime = TabTimes.SelectedIndex == 0 ? 7 : 8;
            general["tab_times"] = tabTime.ToString();

            // 写回 config.ini
            parser.WriteFile("config.ini", ini, new UTF8Encoding(false));

            // 保存 system.txt
            File.WriteAllText("system.txt", SystemText.Text, new UTF8Encoding(false));
        }
        private void Form1_Load(object sender, EventArgs e)
        {
            parser = new();
            IniData ini = parser.ReadFile("config.ini", fileEncoding: new UTF8Encoding(false));
            KeyDataCollection general = ini["general"];
            vname.Text = general["version"];
            winWidth.Value = int.Parse(general["width"]);
            winHeight.Value = int.Parse(general["height"]);
            MaxImageCount.Value = int.Parse(general["maximagecount"]);
            ModelName.Text = general["modelname"];
            IsVisionModel.Checked = general["isvisionmodel"].Equals("true", StringComparison.CurrentCultureIgnoreCase);
            APIKey.Text = general["api_key"];
            ServerName.Items = ["ollama", "内置模型", "自定义"];
            ServerName.SelectedIndex = general["server_url"].ToLower() switch
            {
                "ollama" => 0,
                "builtin" => 1,
                _ => 2,
            };
            ServerUrl.Text = general["server_url"];
            Scroll.Value = int.Parse(general["scroll"]);
            WithImage.Checked = general["withimage"].Equals("true", StringComparison.CurrentCultureIgnoreCase);
            AutoLogin.Checked = general["autologin"].Equals("true", StringComparison.CurrentCultureIgnoreCase);
            AutoFocusing.Checked = general["autofocusing"].Equals("true", StringComparison.CurrentCultureIgnoreCase);
            SendImagePossibility.Value = int.Parse(general["sendimagepossibility"]);

            ATDetect.Checked = general["atdetect"].Equals("true", StringComparison.CurrentCultureIgnoreCase);
            RemoteServerTimeout.Value = int.Parse(general["remote_server_timeout"]);
            TabTimes.Items = [7, 8];
            TabTimes.SelectedIndex = int.Parse(general["tab_times"]) switch
            {
                7 => 0,
                8 => 1,
                _ => 1

            };
            SystemText.Text = File.ReadAllText("system.txt", new UTF8Encoding(false));
        }

        private void inputNumber1_ValueChanged(object sender, AntdUI.DecimalEventArgs e)
        {

        }

        private void tooltip1_Click(object sender, EventArgs e)
        {

        }

        private void ServerName_SelectedIndexChanged(object sender, AntdUI.IntEventArgs e)
        {
            if (ServerName.SelectedIndex == 0)
            {
                ServerUrl.Text = ServerName.Text.Trim();
            }
            if (ServerName.SelectedIndex == 1)
            {
                ServerUrl.Text = "builtin";
            }
            //else { ServerUrl.Enabled = false; }
            ServerUrl.Enabled = (ServerName.SelectedIndex == 2);


        }

        private void ATDetect_CheckedChanged(object sender, AntdUI.BoolEventArgs e)
        {

        }

        private void RemoteServerTimeout_ValueChanged(object sender, AntdUI.DecimalEventArgs e)
        {

        }

        private void buttonShadow1_Click(object sender, EventArgs e)
        {
            SaveConfig();
        }

        private void MaxImageCount_ValueChanged(object sender, AntdUI.DecimalEventArgs e)
        {
            MaxImageCount.Value = Math.Clamp(MaxImageCount.Value, 0, 4);
        }

        private void Scroll_ValueChanged(object sender, AntdUI.DecimalEventArgs e)
        {
            Scroll.Value = Math.Clamp(Scroll.Value, 1, 200);

        }
    }
}
