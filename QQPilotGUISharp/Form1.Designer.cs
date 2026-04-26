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
            SuspendLayout();
            // 
            // winHeight
            // 
            winHeight.Location = new Point(350, 54);
            winHeight.Name = "winHeight";
            winHeight.Size = new Size(120, 56);
            winHeight.TabIndex = 11;
            winHeight.Text = "0";
            // 
            // label3
            // 
            label3.Location = new Point(244, 65);
            label3.Name = "label3";
            label3.Size = new Size(100, 36);
            label3.TabIndex = 10;
            label3.Text = "窗口高度";
            // 
            // winWidth
            // 
            winWidth.Location = new Point(118, 54);
            winWidth.Name = "winWidth";
            winWidth.Size = new Size(120, 56);
            winWidth.TabIndex = 9;
            winWidth.Text = "0";
            // 
            // label2
            // 
            label2.Location = new Point(12, 65);
            label2.Name = "label2";
            label2.Size = new Size(100, 36);
            label2.TabIndex = 8;
            label2.Text = "窗口宽度";
            // 
            // vname
            // 
            vname.Location = new Point(84, 12);
            vname.Name = "vname";
            vname.Size = new Size(642, 36);
            vname.TabIndex = 7;
            vname.Text = "版本";
            // 
            // label1
            // 
            label1.Location = new Point(12, 12);
            label1.Name = "label1";
            label1.Size = new Size(66, 36);
            label1.TabIndex = 6;
            label1.Text = "版本";
            // 
            // label4
            // 
            label4.Location = new Point(12, 126);
            label4.Name = "label4";
            label4.Size = new Size(100, 36);
            label4.TabIndex = 12;
            label4.Text = "解析图片数";
            // 
            // MaxImageCount
            // 
            MaxImageCount.Location = new Point(118, 116);
            MaxImageCount.Name = "MaxImageCount";
            MaxImageCount.Size = new Size(120, 56);
            MaxImageCount.TabIndex = 13;
            MaxImageCount.Text = "0";
            MaxImageCount.ValueChanged += MaxImageCount_ValueChanged;
            // 
            // tooltip1
            // 
            tooltip1.Back = SystemColors.ActiveCaptionText;
            tooltip1.BackColor = SystemColors.ButtonFace;
            tooltip1.ForeColor = SystemColors.AppWorkspace;
            tooltip1.Location = new Point(244, 116);
            tooltip1.MaximumSize = new Size(340, 57);
            tooltip1.MinimumSize = new Size(340, 57);
            tooltip1.Name = "tooltip1";
            tooltip1.Size = new Size(340, 57);
            tooltip1.TabIndex = 15;
            tooltip1.Text = "(本地模型解析>1张图片时速度极慢)";
            tooltip1.Click += tooltip1_Click;
            // 
            // label5
            // 
            label5.Location = new Point(12, 187);
            label5.Name = "label5";
            label5.Size = new Size(100, 36);
            label5.TabIndex = 16;
            label5.Text = "模型名称";
            // 
            // ModelName
            // 
            ModelName.Location = new Point(118, 173);
            ModelName.Name = "ModelName";
            ModelName.Size = new Size(654, 60);
            ModelName.TabIndex = 17;
            // 
            // label6
            // 
            label6.Location = new Point(12, 249);
            label6.Name = "label6";
            label6.Size = new Size(100, 36);
            label6.TabIndex = 18;
            label6.Text = "视觉模型";
            // 
            // IsVisionModel
            // 
            IsVisionModel.Location = new Point(118, 239);
            IsVisionModel.Name = "IsVisionModel";
            IsVisionModel.Size = new Size(112, 55);
            IsVisionModel.TabIndex = 19;
            // 
            // label7
            // 
            label7.Location = new Point(12, 314);
            label7.Name = "label7";
            label7.Size = new Size(100, 36);
            label7.TabIndex = 20;
            label7.Text = "API Key";
            // 
            // APIKey
            // 
            APIKey.Location = new Point(116, 300);
            APIKey.Name = "APIKey";
            APIKey.PasswordChar = '·';
            APIKey.Size = new Size(656, 60);
            APIKey.TabIndex = 21;
            // 
            // label8
            // 
            label8.Location = new Point(12, 392);
            label8.Name = "label8";
            label8.Size = new Size(100, 36);
            label8.TabIndex = 22;
            label8.Text = "服务器";
            // 
            // ServerName
            // 
            ServerName.Location = new Point(118, 379);
            ServerName.Name = "ServerName";
            ServerName.Size = new Size(158, 60);
            ServerName.TabIndex = 23;
            ServerName.Text = "select1";
            ServerName.SelectedIndexChanged += ServerName_SelectedIndexChanged;
            // 
            // ServerUrl
            // 
            ServerUrl.Location = new Point(282, 379);
            ServerUrl.Name = "ServerUrl";
            ServerUrl.Size = new Size(490, 60);
            ServerUrl.TabIndex = 24;
            // 
            // Scroll
            // 
            Scroll.Location = new Point(146, 445);
            Scroll.Name = "Scroll";
            Scroll.Size = new Size(120, 56);
            Scroll.TabIndex = 26;
            Scroll.Text = "0";
            Scroll.ValueChanged += Scroll_ValueChanged;
            // 
            // label9
            // 
            label9.Location = new Point(12, 458);
            label9.Name = "label9";
            label9.Size = new Size(128, 36);
            label9.TabIndex = 25;
            label9.Text = "框选消息时长";
            // 
            // label10
            // 
            label10.Location = new Point(12, 524);
            label10.Name = "label10";
            label10.Size = new Size(100, 36);
            label10.TabIndex = 27;
            label10.Text = "包含图片";
            // 
            // WithImage
            // 
            WithImage.Location = new Point(118, 515);
            WithImage.Name = "WithImage";
            WithImage.Size = new Size(112, 55);
            WithImage.TabIndex = 28;
            // 
            // label11
            // 
            label11.Location = new Point(244, 524);
            label11.Name = "label11";
            label11.Size = new Size(128, 36);
            label11.TabIndex = 29;
            label11.Text = "自动点击登录";
            // 
            // label12
            // 
            label12.Location = new Point(476, 524);
            label12.Name = "label12";
            label12.Size = new Size(194, 36);
            label12.TabIndex = 29;
            label12.Text = "持续将窗口置于最前";
            // 
            // AutoLogin
            // 
            AutoLogin.Location = new Point(358, 515);
            AutoLogin.Name = "AutoLogin";
            AutoLogin.Size = new Size(112, 55);
            AutoLogin.TabIndex = 30;
            // 
            // AutoFocusing
            // 
            AutoFocusing.Location = new Point(660, 515);
            AutoFocusing.Name = "AutoFocusing";
            AutoFocusing.Size = new Size(112, 55);
            AutoFocusing.TabIndex = 31;
            // 
            // label13
            // 
            label13.Location = new Point(9, 585);
            label13.Name = "label13";
            label13.Size = new Size(168, 36);
            label13.TabIndex = 32;
            label13.Text = "发送图片概率 (%)";
            // 
            // SendImagePossibility
            // 
            SendImagePossibility.Location = new Point(167, 576);
            SendImagePossibility.Name = "SendImagePossibility";
            SendImagePossibility.Size = new Size(605, 55);
            SendImagePossibility.TabIndex = 34;
            SendImagePossibility.Text = "slider1";
            // 
            // ATDetect
            // 
            ATDetect.Location = new Point(118, 635);
            ATDetect.Name = "ATDetect";
            ATDetect.Size = new Size(112, 55);
            ATDetect.TabIndex = 36;
            ATDetect.CheckedChanged += ATDetect_CheckedChanged;
            // 
            // label14
            // 
            label14.Location = new Point(12, 644);
            label14.Name = "label14";
            label14.Size = new Size(100, 36);
            label14.TabIndex = 35;
            label14.Text = "只检查 @";
            // 
            // label15
            // 
            label15.Location = new Point(12, 698);
            label15.Name = "label15";
            label15.Size = new Size(192, 36);
            label15.TabIndex = 35;
            label15.Text = "远程服务器超时 (秒):";
            // 
            // RemoteServerTimeout
            // 
            RemoteServerTimeout.Location = new Point(244, 687);
            RemoteServerTimeout.Name = "RemoteServerTimeout";
            RemoteServerTimeout.Size = new Size(120, 56);
            RemoteServerTimeout.TabIndex = 37;
            RemoteServerTimeout.Text = "0";
            RemoteServerTimeout.ValueChanged += RemoteServerTimeout_ValueChanged;
            // 
            // label16
            // 
            label16.Location = new Point(411, 698);
            label16.Name = "label16";
            label16.Size = new Size(192, 36);
            label16.TabIndex = 38;
            label16.Text = "tab按下次数";
            // 
            // TabTimes
            // 
            TabTimes.Location = new Point(614, 683);
            TabTimes.Name = "TabTimes";
            TabTimes.Size = new Size(158, 60);
            TabTimes.TabIndex = 39;
            TabTimes.Text = "select1";
            // 
            // SystemText
            // 
            SystemText.Location = new Point(789, 65);
            SystemText.Multiline = true;
            SystemText.Name = "SystemText";
            SystemText.Size = new Size(735, 678);
            SystemText.TabIndex = 40;
            SystemText.Text = "input1";
            // 
            // label17
            // 
            label17.Location = new Point(789, 12);
            label17.Name = "label17";
            label17.Size = new Size(117, 36);
            label17.TabIndex = 41;
            label17.Text = "提示文本";
            // 
            // buttonShadow1
            // 
            buttonShadow1.Location = new Point(1308, 12);
            buttonShadow1.Name = "buttonShadow1";
            buttonShadow1.Size = new Size(207, 56);
            buttonShadow1.TabIndex = 42;
            buttonShadow1.Text = "保存设置";
            buttonShadow1.Click += buttonShadow1_Click;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(10F, 25F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = SystemColors.ButtonFace;
            ClientSize = new Size(1536, 773);
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
    }
}
