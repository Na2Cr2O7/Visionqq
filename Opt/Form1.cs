
using IniParser;
using IniParser.Model;
using System.Text;
namespace Opt
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            FileIniDataParser parser = new();
            IniData data = parser.ReadFile("Config.ini", Encoding.UTF8);
            string width = data["general"]["width"];
            string height = data["general"]["height"];
            string modelName = data["general"]["modelname"];
            string apikey = data["general"]["api_key"];
            string serverURL = data["general"]["server_url"];
            string systemPrompt = data["general"]["system"];
            string scroll= data["general"]["scroll"];
            //parser.WriteFile("Configuration.ini", data);


            //var ini = new IniFile("config.ini");
            // string width = ini.Read("general", "width");


            textBox1.Text = width;
            textBox2.Text = height;
            textBox3.Text = modelName;
            textBox4.Text = apikey;
            textBox5.Text = serverURL;
            textBox6.Text = systemPrompt;
            textBox7.Text = scroll;
            if (textBox5.Text == "Ollama")
            {
                checkBox1.Checked = true;
            }

        }

        private void button2_Click(object sender, EventArgs e)
        {
            Apply();

        }
        private void Apply()
        {
            FileIniDataParser parser = new();
            IniData data = parser.ReadFile("config.ini", new System.Text.UTF8Encoding(false));
            data["general"]["width"] = textBox1.Text;
            data["general"]["height"] = textBox2.Text;
            data["general"]["modelname"] = textBox3.Text;
            data["general"]["api_key"] = textBox4.Text;
            data["general"]["server_url"] = textBox5.Text;
            data["general"]["system"] = textBox6.Text;
            data["general"]["scroll"]=textBox7.Text;
            parser.WriteFile("config.ini", data, new System.Text.UTF8Encoding(false));



        }
        private void button3_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {
            textBox5.Visible = !checkBox1.Checked;
            textBox4.Visible = !checkBox1.Checked;
            if (checkBox1.Checked)
            {
                textBox5.Text = "Ollama";
                textBox4.Text = "None";
            }
        }

        private void textBox6_TextChanged(object sender, EventArgs e)
        {
            textBox6.Text = textBox6.Text.Replace("\n", "");
        }

        private void textBox5_TextChanged(object sender, EventArgs e)
        {

        }
        private bool isnumeric(string s)
        {
            try
            {
                int.Parse(s);
                return true;
            }
            catch { return false; }
        }
        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            if (!isnumeric(textBox1.Text))
            {
                textBox1.Text = 1280.ToString();
            }
        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {
            if (!isnumeric(textBox2.Text))
            {
                textBox2.Text = 720.ToString();

            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Apply();
            Close();
        }

        private void button4_Click(object sender, EventArgs e)
        {
            string currentWorkingDirectory = Directory.GetCurrentDirectory();
            string[] deleteExt = { "*.png", "*.jpg" };
            foreach (string ext in deleteExt)
            {
                string[] files = Directory.GetFiles(currentWorkingDirectory, ext);
                foreach (string file in files)
                {
                    try
                    {
                        File.Delete(file);
                        Console.WriteLine($"deleted{file}");

                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"failed{file}{ex}");
                    }
                }


            }
        }

        private void textBox7_TextChanged(object sender, EventArgs e)
        {
            if(!isnumeric(textBox7.Text))
            {
                textBox7.Text = 4.ToString();
            }
        }
    }
}
