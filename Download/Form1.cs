using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net.Http;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Download
{
    partial class Form1 : AntdUI.Window
    {
        private const string UserAgent = "NULL";
        private readonly List<(AntdUI.Progress progress, AntdUI.Label status, AntdUI.Button startBtn, AntdUI.Button openBtn)> downloadControls = new();
        private readonly HttpClient httpClient = new(new HttpClientHandler { AllowAutoRedirect = true });

        public Form1()
        {
            InitializeComponent();
            httpClient.DefaultRequestHeaders.Add("User-Agent", UserAgent);
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // 设置窗口标题和图标
            this.Text = "下载助手";
            // 创建标题标签
            var title = new AntdUI.Label
            {
                Text = "下载可能需要的文件",
                Font = new System.Drawing.Font("Arial", 16),
                ForeColor = System.Drawing.ColorTranslator.FromHtml("#333333"),
                Location = new System.Drawing.Point(20, 20),
                Size = new System.Drawing.Size(760, 30)
            };
            this.Controls.Add(title);

            // 切换到download目录
            try
            {
                Directory.SetCurrentDirectory(Path.Combine(Directory.GetCurrentDirectory(), "download"));
            }
            catch (Exception ex)
            {
                MessageBox.Show($"无法切换到download目录: {ex.Message}", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // 读取index.json配置文件
            if (!File.Exists("index.json"))
            {
                MessageBox.Show("index.json配置文件不存在！", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            try
            {
                string jsonContent = File.ReadAllText("index.json");
                using JsonDocument doc = JsonDocument.Parse(jsonContent);
                JsonElement root = doc.RootElement;

                if (!root.ValueKind.Equals(JsonValueKind.Array))
                {
                    MessageBox.Show("index.json格式错误：根元素必须是数组！", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                int yPosition = 70;
                foreach (JsonElement downloadElement in root.EnumerateArray())
                {
                    if (!downloadElement.TryGetProperty("description", out JsonElement descriptionElement) ||
                        !downloadElement.TryGetProperty("url", out JsonElement urlElement) ||
                        !downloadElement.TryGetProperty("filename", out JsonElement filenameElement))
                    {
                        continue; // 跳过无效条目
                    }

                    string description = descriptionElement.GetString() ?? "未命名下载项";
                    string url = urlElement.GetString() ?? "";
                    string filename = filenameElement.GetString() ?? Path.GetFileName(url) ?? "download";

                    if (string.IsNullOrEmpty(url))
                        continue;

                    CreateDownloadSection(description, url, filename, ref yPosition);
                    yPosition += 350; // 每个部分的高度
                }

                // 设置窗口大小
                int windowHeight = Math.Max(450, 100 + downloadControls.Count * 130);
                this.ClientSize = new System.Drawing.Size(800, windowHeight);
                SBar.Maximum = yPosition - Height;
                FZ.Height = yPosition;

            }
            catch (Exception ex)
            {
                MessageBox.Show($"解析index.json时出错: {ex.Message}", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void CreateDownloadSection(string name, string url, string filename, ref int yPosition)
        {
            // 创建分组框
            var groupBox = new GroupBox
            {
                Location = new System.Drawing.Point(20, yPosition),
                Size = new System.Drawing.Size(800, 300),
                BackColor = System.Drawing.Color.White,
                Text = ""
            };

            // 创建描述标签
            var nameLabel = new AntdUI.Label
            {
                Text = name,
                Font = new System.Drawing.Font("Arial", 15),
                Location = new System.Drawing.Point(15, 15),
                Size = new System.Drawing.Size(730, 40)
            };
            groupBox.Controls.Add(nameLabel);

            // 创建进度条
            var progress = new AntdUI.Progress
            {
                Location = new System.Drawing.Point(15, 40),
                Size = new System.Drawing.Size(730, 50),
                Value = 0,
                //Maximum = 100

            };
            groupBox.Controls.Add(progress);

            // 创建状态标签
            var status = new AntdUI.Label
            {
                Text = "准备就绪",
                Font = new System.Drawing.Font("Arial", 11),
                Location = new System.Drawing.Point(15, 65),
                Size = new System.Drawing.Size(730, 100)
            };
            groupBox.Controls.Add(status);

            // 创建按钮面板
            var buttonPanel = new GroupBox
            {
                Location = new System.Drawing.Point(15, 170),
                Size = new System.Drawing.Size(730, 120),
            };

            // 开始按钮
            var startBtn = new AntdUI.Button
            {
                Text = "开始",
                BackColor = System.Drawing.ColorTranslator.FromHtml("#4CAF50"),
                ForeColor = System.Drawing.Color.Blue,
                Font = new System.Drawing.Font("Arial", 10),
                Size = new System.Drawing.Size(220, 80),
                Location = new System.Drawing.Point(0, 30)
            };
            startBtn.Click += (s, e) => StartDownload(url, progress, status, filename, startBtn);
            buttonPanel.Controls.Add(startBtn);

            // 在浏览器中打开按钮
            var openInBrowserBtn = new AntdUI.Button
            {
                Text = "🌐 在浏览器中打开",
                BackColor = System.Drawing.ColorTranslator.FromHtml("#424566"),
                //ForeColor = System.Drawing.Color.White,
                ForeColor = System.Drawing.Color.Blue,

                Size = new System.Drawing.Size(220, 80),
                Location = new System.Drawing.Point(240, 30)
            };
            openInBrowserBtn.Click += (s, e) => OpenInBrowser(url);
            buttonPanel.Controls.Add(openInBrowserBtn);

            // 打开文件夹按钮（初始禁用）
            var openBtn = new AntdUI.Button
            {
                Text = "📂 打开文件夹",
                Enabled = false,
                Size = new System.Drawing.Size(220, 80),
                Location = new System.Drawing.Point(500, 30)
            };
            openBtn.Click += (s, e) => OpenFolder(filename);
            buttonPanel.Controls.Add(openBtn);

            groupBox.Controls.Add(buttonPanel);
            FZ.Controls.Add(groupBox);

            // 存储控件引用
            downloadControls.Add((progress, status, startBtn, openBtn));
        }

        private void OpenInBrowser(string url)
        {
            try
            {
                Process.Start(url);
            }
            catch
            {
                // 尝试使用explorer.exe
                try
                {
                    Process.Start("explorer.exe", url);
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"无法在浏览器中打开链接: {ex.Message}", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private void OpenFolder(string filepath)
        {
            string fullPath = Path.GetFullPath(filepath);
            if (!File.Exists(fullPath))
            {
                MessageBox.Show("文件不存在，无法打开文件夹！", "警告", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            try
            {
                Process.Start("explorer.exe", $"/select,\"{fullPath}\"");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"无法打开文件夹: {ex.Message}", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private async void StartDownload(string url, AntdUI.Progress progress, AntdUI.Label status, string filename, AntdUI.Button startBtn)
        {
            if (status.Text.Contains("下载中") || status.Text.Contains("连接中"))
                return;

            // 禁用开始按钮防止重复点击
            startBtn.Enabled = false;

            await Task.Run(async () =>
            {
                try
                {
                    // 更新状态为连接中
                    InvokeIfRequired(() => status.Text = "📥 连接中...");

                    // 获取响应头以确定文件大小
                    using var request = new HttpRequestMessage(HttpMethod.Head, url);
                    using var headResponse = await httpClient.SendAsync(request, HttpCompletionOption.ResponseHeadersRead);

                    if (!headResponse.IsSuccessStatusCode)
                    {
                        throw new HttpRequestException($"HTTP错误: {(int)headResponse.StatusCode} {headResponse.ReasonPhrase}");
                    }

                    long totalSize = headResponse.Content.Headers.ContentLength ?? 10240;
                    if (totalSize == 0)
                        totalSize = 10240;

                    // 开始实际下载
                    using var downloadRequest = new HttpRequestMessage(HttpMethod.Get, url);
                    using var response = await httpClient.SendAsync(downloadRequest, HttpCompletionOption.ResponseHeadersRead);

                    if (!response.IsSuccessStatusCode)
                    {
                        throw new HttpRequestException($"HTTP错误: {(int)response.StatusCode} {response.ReasonPhrase}");
                    }

                    long downloaded = 0;
                    byte[] buffer = new byte[8192];
                    DateTime lastUpdate = DateTime.Now;
                    long lastDownloaded = 0;

                    InvokeIfRequired(() =>
                    {
                        status.Text = "⬇️ 下载中...";
                        //progress.Maximum = 100;
                        progress.Value = 0;
                    });

                    using var fileStream = new FileStream(filename, FileMode.Create, FileAccess.Write, FileShare.None, 8192, true);
                    using var responseStream = await response.Content.ReadAsStreamAsync();

                    while (true)
                    {
                        int bytesRead = await responseStream.ReadAsync(buffer, 0, buffer.Length);
                        if (bytesRead == 0)
                            break;

                        await fileStream.WriteAsync(buffer, 0, bytesRead);
                        downloaded += bytesRead;

                        DateTime now = DateTime.Now;
                        if ((now - lastUpdate).TotalSeconds >= 0.3 || downloaded >= totalSize)
                        {
                            double elapsedSeconds = (now - lastUpdate).TotalSeconds;
                            double speedBps = elapsedSeconds > 0 ? (downloaded - lastDownloaded) / elapsedSeconds : 0;
                            double speedKbps = speedBps / 1024;
                            double percent = Math.Min((double)downloaded / totalSize * 100, 100);

                            string speedStr;
                            if (speedKbps < 1024)
                                speedStr = $"{speedKbps:F2} KB/s";
                            else
                                speedStr = $"{speedKbps / 1024:F2} MB/s";

                            double downloadedMb = downloaded / (1024.0 * 1024.0);
                            double totalMb = totalSize / (1024.0 * 1024.0);

                            InvokeIfRequired(() =>
                            {
                                progress.Value = (float)((downloadedMb / totalMb));
                                status.Text = $"{percent:F1}% 已完成, {speedStr} | {downloadedMb:F2}MB/{totalMb:F2}MB";
                            });

                            lastUpdate = now;
                            lastDownloaded = downloaded;
                        }
                    }

                    // 下载成功
                    InvokeIfRequired(() =>
                    {
                        MessageBox.Show($"{filename} 下载完成！", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        status.Text = "✅ 下载完成！";
                        // 启用"打开文件夹"按钮
                        var openBtn = FindOpenButton(progress);
                        if (openBtn != null)
                            openBtn.Enabled = true;
                    });
                }
                catch (Exception ex)
                {
                    InvokeIfRequired(() =>
                    {
                        MessageBox.Show($"下载失败:\n{ex.Message}", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        status.Text = "❌ 下载失败";
                        progress.Value = 0;
                    });
                }
                finally
                {
                    // 重新启用开始按钮
                    InvokeIfRequired(() => startBtn.Enabled = true);
                }
            });
        }

        private AntdUI.Button FindOpenButton(AntdUI.Progress progress)
        {
            foreach (var (p, _, _, openBtn) in downloadControls)
            {
                if (p == progress)
                    return openBtn;
            }
            return null;
        }

        private void InvokeIfRequired(Action action)
        {
            if (this.InvokeRequired)
                this.Invoke(action);
            else
                action();
        }

        private void groupBox1_Enter(object sender, EventArgs e)
        {

        }

        private void SBar_Scroll(object sender, ScrollEventArgs e)
        {
            FZ.Top = -SBar.Value;
        }

        private void buttonShadow1_Click(object sender, EventArgs e)
        {
            Close();
        }

        //protected override void Dispose(bool disposing)
        //{
        //    if (disposing)
        //    {
        //        httpClient?.Dispose();
        //        components?.Dispose();
        //    }
        //    base.Dispose(disposing);
        //}
    }
}