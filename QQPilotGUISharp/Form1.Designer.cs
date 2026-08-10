namespace QQPilotGUISharp
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            winHeight = new AntdUI.InputNumber();
            label3 = new AntdUI.Label();
            winWidth = new AntdUI.InputNumber();
            label2 = new AntdUI.Label();
            vname = new AntdUI.Label();
            label1 = new AntdUI.Label();
            label4 = new AntdUI.Label();
            MaxImageCount = new AntdUI.InputNumber();
            tooltip1 = new AntdUI.Tooltip();
            label5 = new AntdUI.Label();
            ModelName = new AntdUI.Input();
            label6 = new AntdUI.Label();
            IsVisionModel = new AntdUI.Switch();
            label7 = new AntdUI.Label();
            APIKey = new AntdUI.Input();
            label8 = new AntdUI.Label();
            ServerName = new AntdUI.Select();
            ServerUrl = new AntdUI.Input();
            Scroll = new AntdUI.InputNumber();
            label9 = new AntdUI.Label();
            label10 = new AntdUI.Label();
            WithImage = new AntdUI.Switch();
            label11 = new AntdUI.Label();
            label12 = new AntdUI.Label();
            AutoLogin = new AntdUI.Switch();
            AutoFocusing = new AntdUI.Switch();
            label13 = new AntdUI.Label();
            SendImagePossibility = new AntdUI.Slider();
            ATDetect = new AntdUI.Switch();
            label14 = new AntdUI.Label();
            label15 = new AntdUI.Label();
            RemoteServerTimeout = new AntdUI.InputNumber();
            label16 = new AntdUI.Label();
            TabTimes = new AntdUI.Select();
            SystemText = new AntdUI.Input();
            label17 = new AntdUI.Label();
            buttonShadow1 = new AntdUI.ButtonShadow();
            buttonShadow2 = new AntdUI.ButtonShadow();
            TokenCount = new AntdUI.Label();
            label19 = new AntdUI.Label();
            UserName = new AntdUI.Input();
            label18 = new AntdUI.Label();
            tooltip2 = new AntdUI.Tooltip();
            forceOllamaAPI = new AntdUI.Switch();
            label20 = new AntdUI.Label();
            buttonShadow3 = new AntdUI.ButtonShadow();
            SuspendLayout();
            // 
            // winHeight
            // 
            winHeight.Location = new Point(248, 59);
            winHeight.Margin = new Padding(2);
            winHeight.Maximum = new decimal(new int[] { 720, 0, 0, 0 });
            winHeight.Name = "winHeight";
            winHeight.Radius = 72;
            winHeight.Size = new Size(84, 34);
            winHeight.TabIndex = 11;
            winHeight.Text = "0";
            // 
            // label3
            // 
            label3.Location = new Point(174, 66);
            label3.Margin = new Padding(2);
            label3.Name = "label3";
            label3.Size = new Size(70, 22);
            label3.TabIndex = 10;
            label3.Text = "窗口高度";
            // 
            // winWidth
            // 
            winWidth.Location = new Point(86, 59);
            winWidth.Margin = new Padding(2);
            winWidth.Minimum = new decimal(new int[] { 1280, 0, 0, 0 });
            winWidth.Name = "winWidth";
            winWidth.Radius = 72;
            winWidth.Size = new Size(84, 34);
            winWidth.TabIndex = 9;
            winWidth.Text = "1280";
            winWidth.Value = new decimal(new int[] { 1280, 0, 0, 0 });
            winWidth.ValueChanged += winWidth_ValueChanged;
            // 
            // label2
            // 
            label2.Location = new Point(11, 66);
            label2.Margin = new Padding(2);
            label2.Name = "label2";
            label2.Size = new Size(70, 22);
            label2.TabIndex = 8;
            label2.Text = "窗口宽度";
            // 
            // vname
            // 
            vname.Location = new Point(86, 7);
            vname.Margin = new Padding(2);
            vname.Name = "vname";
            vname.Size = new Size(449, 22);
            vname.TabIndex = 7;
            vname.Text = "版本";
            // 
            // label1
            // 
            label1.Location = new Point(11, 7);
            label1.Margin = new Padding(2);
            label1.Name = "label1";
            label1.Size = new Size(46, 22);
            label1.TabIndex = 6;
            label1.Text = "版本";
            label1.Click += label1_Click;
            // 
            // label4
            // 
            label4.Location = new Point(11, 103);
            label4.Margin = new Padding(2);
            label4.Name = "label4";
            label4.Size = new Size(70, 22);
            label4.TabIndex = 12;
            label4.Text = "解析图片数";
            // 
            // MaxImageCount
            // 
            MaxImageCount.Location = new Point(86, 97);
            MaxImageCount.Margin = new Padding(2);
            MaxImageCount.Minimum = new decimal(new int[] { 0, 0, 0, 0 });
            MaxImageCount.Name = "MaxImageCount";
            MaxImageCount.Size = new Size(84, 34);
            MaxImageCount.TabIndex = 13;
            MaxImageCount.Text = "0";
            MaxImageCount.ValueChanged += MaxImageCount_ValueChanged;
            // 
            // tooltip1
            // 
            tooltip1.Back = SystemColors.ActiveCaptionText;
            tooltip1.BackColor = SystemColors.ButtonFace;
            tooltip1.ForeColor = SystemColors.AppWorkspace;
            tooltip1.Location = new Point(174, 93);
            tooltip1.Margin = new Padding(2);
            tooltip1.MaximumSize = new Size(227, 38);
            tooltip1.MinimumSize = new Size(227, 38);
            tooltip1.Name = "tooltip1";
            tooltip1.Size = new Size(227, 38);
            tooltip1.TabIndex = 15;
            tooltip1.Text = "(本地模型解析>1张图片时速度极慢)";
            tooltip1.Click += tooltip1_Click;
            // 
            // label5
            // 
            label5.Location = new Point(11, 139);
            label5.Margin = new Padding(2);
            label5.Name = "label5";
            label5.Size = new Size(70, 22);
            label5.TabIndex = 16;
            label5.Text = "模型名称";
            // 
            // ModelName
            // 
            ModelName.Location = new Point(86, 131);
            ModelName.Margin = new Padding(2);
            ModelName.Name = "ModelName";
            ModelName.Size = new Size(458, 36);
            ModelName.TabIndex = 17;
            ModelName.TextChanged += ModelName_TextChanged;
            // 
            // label6
            // 
            label6.Location = new Point(11, 176);
            label6.Margin = new Padding(2);
            label6.Name = "label6";
            label6.Size = new Size(70, 22);
            label6.TabIndex = 18;
            label6.Text = "视觉模型";
            // 
            // IsVisionModel
            // 
            IsVisionModel.Location = new Point(86, 170);
            IsVisionModel.Margin = new Padding(2);
            IsVisionModel.Name = "IsVisionModel";
            IsVisionModel.Size = new Size(78, 33);
            IsVisionModel.TabIndex = 19;
            IsVisionModel.CheckedChanged += IsVisionModel_CheckedChanged;
            // 
            // label7
            // 
            label7.Location = new Point(11, 215);
            label7.Margin = new Padding(2);
            label7.Name = "label7";
            label7.Size = new Size(70, 22);
            label7.TabIndex = 20;
            label7.Text = "API Key";
            // 
            // APIKey
            // 
            APIKey.Location = new Point(84, 207);
            APIKey.Margin = new Padding(2);
            APIKey.Name = "APIKey";
            APIKey.PasswordChar = '·';
            APIKey.Size = new Size(459, 36);
            APIKey.TabIndex = 21;
            APIKey.TextChanged += APIKey_TextChanged;
            // 
            // label8
            // 
            label8.Location = new Point(11, 262);
            label8.Margin = new Padding(2);
            label8.Name = "label8";
            label8.Size = new Size(70, 22);
            label8.TabIndex = 22;
            label8.Text = "服务器";
            // 
            // ServerName
            // 
            ServerName.Location = new Point(86, 254);
            ServerName.Margin = new Padding(2);
            ServerName.Name = "ServerName";
            ServerName.Size = new Size(111, 36);
            ServerName.TabIndex = 23;
            ServerName.Text = "select1";
            ServerName.SelectedIndexChanged += ServerName_SelectedIndexChanged;
            // 
            // ServerUrl
            // 
            ServerUrl.Location = new Point(200, 254);
            ServerUrl.Margin = new Padding(2);
            ServerUrl.Name = "ServerUrl";
            ServerUrl.Size = new Size(343, 36);
            ServerUrl.TabIndex = 24;
            // 
            // Scroll
            // 
            Scroll.Location = new Point(105, 294);
            Scroll.Margin = new Padding(2);
            Scroll.Name = "Scroll";
            Scroll.Size = new Size(84, 34);
            Scroll.TabIndex = 26;
            Scroll.Text = "0";
            Scroll.ValueChanged += Scroll_ValueChanged;
            // 
            // label9
            // 
            label9.Location = new Point(11, 302);
            label9.Margin = new Padding(2);
            label9.Name = "label9";
            label9.Size = new Size(90, 22);
            label9.TabIndex = 25;
            label9.Text = "框选消息时长";
            // 
            // label10
            // 
            label10.Location = new Point(11, 341);
            label10.Margin = new Padding(2);
            label10.Name = "label10";
            label10.Size = new Size(70, 22);
            label10.TabIndex = 27;
            label10.Text = "包含图片";
            // 
            // WithImage
            // 
            WithImage.Location = new Point(86, 336);
            WithImage.Margin = new Padding(2);
            WithImage.Name = "WithImage";
            WithImage.Size = new Size(78, 33);
            WithImage.TabIndex = 28;
            // 
            // label11
            // 
            label11.Location = new Point(174, 341);
            label11.Margin = new Padding(2);
            label11.Name = "label11";
            label11.Size = new Size(90, 22);
            label11.TabIndex = 29;
            label11.Text = "自动点击登录";
            // 
            // label12
            // 
            label12.Location = new Point(336, 341);
            label12.Margin = new Padding(2);
            label12.Name = "label12";
            label12.Size = new Size(136, 22);
            label12.TabIndex = 29;
            label12.Text = "持续将窗口置于最前";
            // 
            // AutoLogin
            // 
            AutoLogin.Location = new Point(254, 336);
            AutoLogin.Margin = new Padding(2);
            AutoLogin.Name = "AutoLogin";
            AutoLogin.Size = new Size(78, 33);
            AutoLogin.TabIndex = 30;
            // 
            // AutoFocusing
            // 
            AutoFocusing.Location = new Point(465, 336);
            AutoFocusing.Margin = new Padding(2);
            AutoFocusing.Name = "AutoFocusing";
            AutoFocusing.Size = new Size(78, 33);
            AutoFocusing.TabIndex = 31;
            // 
            // label13
            // 
            label13.Location = new Point(9, 378);
            label13.Margin = new Padding(2);
            label13.Name = "label13";
            label13.Size = new Size(118, 22);
            label13.TabIndex = 32;
            label13.Text = "发送图片概率 (%)";
            // 
            // SendImagePossibility
            // 
            SendImagePossibility.Location = new Point(120, 373);
            SendImagePossibility.Margin = new Padding(2);
            SendImagePossibility.Name = "SendImagePossibility";
            SendImagePossibility.Size = new Size(424, 33);
            SendImagePossibility.TabIndex = 34;
            SendImagePossibility.Text = "slider1";
            // 
            // ATDetect
            // 
            ATDetect.Location = new Point(86, 408);
            ATDetect.Margin = new Padding(2);
            ATDetect.Name = "ATDetect";
            ATDetect.Size = new Size(78, 33);
            ATDetect.TabIndex = 36;
            ATDetect.CheckedChanged += ATDetect_CheckedChanged;
            // 
            // label14
            // 
            label14.Location = new Point(11, 413);
            label14.Margin = new Padding(2);
            label14.Name = "label14";
            label14.Size = new Size(70, 22);
            label14.TabIndex = 35;
            label14.Text = "只检查 @";
            // 
            // label15
            // 
            label15.Location = new Point(11, 446);
            label15.Margin = new Padding(2);
            label15.Name = "label15";
            label15.Size = new Size(134, 22);
            label15.TabIndex = 35;
            label15.Text = "远程服务器超时 (秒):";
            // 
            // RemoteServerTimeout
            // 
            RemoteServerTimeout.Location = new Point(174, 439);
            RemoteServerTimeout.Margin = new Padding(2);
            RemoteServerTimeout.Minimum = new decimal(new int[] { 60, 0, 0, 0 });
            RemoteServerTimeout.Name = "RemoteServerTimeout";
            RemoteServerTimeout.Size = new Size(84, 34);
            RemoteServerTimeout.TabIndex = 37;
            RemoteServerTimeout.Text = "60";
            RemoteServerTimeout.Value = new decimal(new int[] { 60, 0, 0, 0 });
            RemoteServerTimeout.ValueChanged += RemoteServerTimeout_ValueChanged;
            // 
            // label16
            // 
            label16.Location = new Point(291, 446);
            label16.Margin = new Padding(2);
            label16.Name = "label16";
            label16.Size = new Size(134, 22);
            label16.TabIndex = 38;
            label16.Text = "tab按下次数";
            // 
            // TabTimes
            // 
            TabTimes.Location = new Point(433, 437);
            TabTimes.Margin = new Padding(2);
            TabTimes.Name = "TabTimes";
            TabTimes.Size = new Size(111, 36);
            TabTimes.TabIndex = 39;
            TabTimes.Text = "select1";
            // 
            // SystemText
            // 
            SystemText.Location = new Point(552, 39);
            SystemText.Margin = new Padding(2);
            SystemText.Multiline = true;
            SystemText.Name = "SystemText";
            SystemText.Size = new Size(514, 439);
            SystemText.TabIndex = 40;
            SystemText.Text = "input1";
            // 
            // label17
            // 
            label17.Location = new Point(552, 7);
            label17.Margin = new Padding(2);
            label17.Name = "label17";
            label17.Size = new Size(82, 22);
            label17.TabIndex = 41;
            label17.Text = "提示文本";
            // 
            // buttonShadow1
            // 
            buttonShadow1.Location = new Point(916, 7);
            buttonShadow1.Margin = new Padding(2);
            buttonShadow1.Name = "buttonShadow1";
            buttonShadow1.Size = new Size(145, 34);
            buttonShadow1.TabIndex = 42;
            buttonShadow1.Text = "保存设置";
            buttonShadow1.Click += buttonShadow1_Click;
            // 
            // buttonShadow2
            // 
            buttonShadow2.Location = new Point(416, 93);
            buttonShadow2.Name = "buttonShadow2";
            buttonShadow2.Size = new Size(111, 32);
            buttonShadow2.TabIndex = 43;
            buttonShadow2.Text = "重置计数器";
            buttonShadow2.Click += buttonShadow2_Click;
            // 
            // TokenCount
            // 
            TokenCount.Location = new Point(432, 66);
            TokenCount.Margin = new Padding(2);
            TokenCount.Name = "TokenCount";
            TokenCount.Size = new Size(59, 22);
            TokenCount.TabIndex = 45;
            TokenCount.Text = "版本";
            TokenCount.Click += TokenCount_Click;
            // 
            // label19
            // 
            label19.Location = new Point(355, 66);
            label19.Margin = new Padding(2);
            label19.Name = "label19";
            label19.Size = new Size(70, 22);
            label19.TabIndex = 44;
            label19.Text = "Token用量";
            label19.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // UserName
            // 
            UserName.Location = new Point(83, 26);
            UserName.Margin = new Padding(2);
            UserName.Name = "UserName";
            UserName.Size = new Size(218, 36);
            UserName.TabIndex = 46;
            UserName.TextChanged += UserName_TextChanged;
            // 
            // label18
            // 
            label18.Location = new Point(9, 33);
            label18.Margin = new Padding(2);
            label18.Name = "label18";
            label18.Size = new Size(70, 22);
            label18.TabIndex = 47;
            label18.Text = "用户名";
            // 
            // tooltip2
            // 
            tooltip2.Back = SystemColors.ActiveCaptionText;
            tooltip2.BackColor = SystemColors.ButtonFace;
            tooltip2.ForeColor = SystemColors.AppWorkspace;
            tooltip2.Location = new Point(304, 24);
            tooltip2.Margin = new Padding(2);
            tooltip2.MaximumSize = new Size(168, 38);
            tooltip2.MinimumSize = new Size(168, 38);
            tooltip2.Name = "tooltip2";
            tooltip2.Size = new Size(168, 38);
            tooltip2.TabIndex = 48;
            tooltip2.Text = "用于判断是否是自身消息";
            // 
            // forceOllamaAPI
            // 
            forceOllamaAPI.Location = new Point(465, 297);
            forceOllamaAPI.Margin = new Padding(2);
            forceOllamaAPI.Name = "forceOllamaAPI";
            forceOllamaAPI.Size = new Size(78, 33);
            forceOllamaAPI.TabIndex = 50;
            forceOllamaAPI.CheckedChanged += forceOllamaAPI_CheckedChanged;
            // 
            // label20
            // 
            label20.Location = new Point(336, 302);
            label20.Margin = new Padding(2);
            label20.Name = "label20";
            label20.Size = new Size(136, 22);
            label20.TabIndex = 49;
            label20.Text = "强制使用OllamaAPI";
            // 
            // buttonShadow3
            // 
            buttonShadow3.Location = new Point(200, 297);
            buttonShadow3.Name = "buttonShadow3";
            buttonShadow3.Size = new Size(111, 32);
            buttonShadow3.TabIndex = 51;
            buttonShadow3.Text = "请求的额外参数";
            buttonShadow3.Click += buttonShadow3_Click;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = SystemColors.ButtonFace;
            ClientSize = new Size(1075, 489);
            Controls.Add(buttonShadow3);
            Controls.Add(forceOllamaAPI);
            Controls.Add(label20);
            Controls.Add(tooltip2);
            Controls.Add(label18);
            Controls.Add(UserName);
            Controls.Add(TokenCount);
            Controls.Add(label19);
            Controls.Add(buttonShadow2);
            Controls.Add(buttonShadow1);
            Controls.Add(label17);
            Controls.Add(SystemText);
            Controls.Add(TabTimes);
            Controls.Add(label16);
            Controls.Add(RemoteServerTimeout);
            Controls.Add(ATDetect);
            Controls.Add(label15);
            Controls.Add(label14);
            Controls.Add(SendImagePossibility);
            Controls.Add(label13);
            Controls.Add(AutoFocusing);
            Controls.Add(AutoLogin);
            Controls.Add(label12);
            Controls.Add(label11);
            Controls.Add(WithImage);
            Controls.Add(label10);
            Controls.Add(Scroll);
            Controls.Add(label9);
            Controls.Add(ServerUrl);
            Controls.Add(ServerName);
            Controls.Add(label8);
            Controls.Add(APIKey);
            Controls.Add(label7);
            Controls.Add(IsVisionModel);
            Controls.Add(label6);
            Controls.Add(ModelName);
            Controls.Add(label5);
            Controls.Add(tooltip1);
            Controls.Add(MaxImageCount);
            Controls.Add(label4);
            Controls.Add(winHeight);
            Controls.Add(label3);
            Controls.Add(winWidth);
            Controls.Add(label2);
            Controls.Add(vname);
            Controls.Add(label1);
            FormBorderStyle = FormBorderStyle.FixedDialog;
            Icon = (Icon)resources.GetObject("$this.Icon");
            Margin = new Padding(2);
            MaximizeBox = false;
            Name = "Form1";
            Text = "设置";
            Load += Form1_Load;
            ResumeLayout(false);
        }

        #endregion

        private AntdUI.InputNumber winHeight;
        private AntdUI.Label label3;
        private AntdUI.InputNumber winWidth;
        private AntdUI.Label label2;
        private AntdUI.Label vname;
        private AntdUI.Label label1;
        private AntdUI.Label label4;
        private AntdUI.InputNumber MaxImageCount;
        private AntdUI.Tooltip tooltip1;
        private AntdUI.Label label5;
        private AntdUI.Input ModelName;
        private AntdUI.Label label6;
        private AntdUI.Switch IsVisionModel;
        private AntdUI.Label label7;
        private AntdUI.Input APIKey;
        private AntdUI.Label label8;
        private AntdUI.Select ServerName;
        private AntdUI.Input ServerUrl;
        private AntdUI.InputNumber Scroll;
        private AntdUI.Label label9;
        private AntdUI.Label label10;
        private AntdUI.Switch WithImage;
        private AntdUI.Label label11;
        private AntdUI.Label label12;
        private AntdUI.Switch AutoLogin;
        private AntdUI.Switch AutoFocusing;
        private AntdUI.Label label13;
        private AntdUI.Slider SendImagePossibility;
        private AntdUI.Switch ATDetect;
        private AntdUI.Label label14;
        private AntdUI.Label label15;
        private AntdUI.InputNumber RemoteServerTimeout;
        private AntdUI.Label label16;
        private AntdUI.Select TabTimes;
        private AntdUI.Input SystemText;
        private AntdUI.Label label17;
        private AntdUI.ButtonShadow buttonShadow1;
        private AntdUI.ButtonShadow buttonShadow2;
        private AntdUI.Label TokenCount;
        private AntdUI.Label label19;
        private AntdUI.Input UserName;
        private AntdUI.Label label18;
        private AntdUI.Tooltip tooltip2;
        private AntdUI.Switch forceOllamaAPI;
        private AntdUI.Label label20;
        private AntdUI.ButtonShadow buttonShadow3;
    }
}
