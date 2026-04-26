namespace Download
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
            FZ = new GroupBox();
            buttonShadow1 = new AntdUI.ButtonShadow();
            SBar = new VScrollBar();
            FZ.SuspendLayout();
            SuspendLayout();
            // 
            // FZ
            // 
            FZ.Controls.Add(buttonShadow1);
            FZ.Location = new Point(0, 0);
            FZ.Name = "FZ";
            FZ.Size = new Size(881, 785);
            FZ.TabIndex = 0;
            FZ.TabStop = false;
            FZ.Enter += groupBox1_Enter;
            // 
            // buttonShadow1
            // 
            buttonShadow1.Location = new Point(6, 12);
            buttonShadow1.Name = "buttonShadow1";
            buttonShadow1.Size = new Size(171, 56);
            buttonShadow1.TabIndex = 0;
            buttonShadow1.Text = "关闭";
            buttonShadow1.Click += buttonShadow1_Click;
            // 
            // SBar
            // 
            SBar.Dock = DockStyle.Right;
            SBar.Location = new Point(884, 0);
            SBar.Name = "SBar";
            SBar.Size = new Size(37, 483);
            SBar.TabIndex = 0;
            SBar.Scroll += SBar_Scroll;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(10F, 25F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(921, 483);
            Controls.Add(SBar);
            Controls.Add(FZ);
            Icon = (Icon)resources.GetObject("$this.Icon");
            Name = "Form1";
            Text = "下载助手";
            Load += Form1_Load;
            FZ.ResumeLayout(false);
            ResumeLayout(false);
        }

        #endregion

        private GroupBox FZ;
        private VScrollBar SBar;
        private AntdUI.ButtonShadow buttonShadow1;
    }
}
