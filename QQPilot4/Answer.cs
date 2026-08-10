using IniParser;
using IniParser.Model;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace QQPilot4
{
    internal class Answer
    {
        private readonly HttpClient _httpClient;
        private FileIniDataParser parser = new();
        private IniData? config;
        private string ModelName { get; set; } = "";
        private string ServerUrl { get; set; } = "";
        private bool IsVisionModel { get; set; }
        private int MaxImageCount { get; set; }
        private int RemoteServerTimeout { get; set; }
        private string ApiKey { get; set; } = "";
        private bool Builtin { get; set; } = false;
        private string SysPmpt { get; set; } = "";
        private TinyLangJaccardCS? TinyLangJaccard;
        private bool ForceOllamaAPI { get; set; }

        private
            readonly
            bool UseOllama=false;

        // 常量
        private const int MAX_LENGTH = 2048;

        public long TotalTokens
        {
            get; private set; }
        public Answer()
        {
            config = parser.ReadFile("config.ini", Encoding.UTF8);
            ModelName = config["general"]["modelname"];
            ServerUrl = config["general"]["server_url"];
            IsVisionModel = config["general"]["isvisionmodel"].Equals("true", StringComparison.OrdinalIgnoreCase);
            MaxImageCount = int.Parse(config["general"]["maximagecount"]);
            RemoteServerTimeout = int.Parse(config["general"]["remote_server_timeout"]);
            ForceOllamaAPI = bool.Parse(config["general"]["forceollamaapi"]);
            ApiKey = config["general"]["api_key"];
            SysPmpt = File.Exists("system.txt") ? File.ReadAllText("system.txt") : "";

            // 配置 HttpClient
            _httpClient = new HttpClient();
            _httpClient.Timeout = TimeSpan.FromSeconds(RemoteServerTimeout);
            if (ForceOllamaAPI)
            {
                UseOllama = true;
            }
            else if (ServerUrl.Equals("ollama", StringComparison.OrdinalIgnoreCase))
                {
                    ServerUrl = "http://localhost:11434/api/chat";
                    UseOllama = true;
                    //UseOllama = false;
            }
                else if (ServerUrl.Equals("builtin", StringComparison.OrdinalIgnoreCase))
                {
                    Builtin = true;
                }
            // 否则 ServerUrl 就是用户自定义的 base URL（如 http://192.168.1.100:8000/v1）
        }

        // --- 工具方法 ---

        private static string ImageToBase64(string path)
        {
            byte[] bytes = File.ReadAllBytes(path);
            return Convert.ToBase64String(bytes);
        }

        private static (bool hasTime, List<string> validTimes) IsTime(string text)
        {
            var pattern1 = @"\(?([0-2]?[0-9]):([0-5][0-9])\)?";
            var pattern2 = @"\(?([0-2]?[0-9])\.([0-5][0-9])\)?";

            var matches1 = Regex.Matches(text, pattern1);
            var matches2 = Regex.Matches(text, pattern2);

            var allMatches = matches1.Cast<Match>().Concat(matches2.Cast<Match>());
            var validTimes = new List<string>();

            foreach (var m in allMatches)
            {
                if (int.TryParse(m.Groups[1].Value, out int h) &&
                    int.TryParse(m.Groups[2].Value, out int min) &&
                    h >= 0 && h <= 23 && min >= 0 && min <= 59)
                {
                    validTimes.Add($"{h:D2}:{min:D2}");
                }
            }

            return (validTimes.Count > 0, validTimes);
        }

        private List<Dictionary<string, object>> ConcatenateText(List<ChatContent> textList, List<string> images)
        {
            var messages = new List<Dictionary<string, object>>();

            foreach (var t in textList)
            {
                // 只收集同时出现在全局 images 列表（已按 MaxImageCount 截断）中的图片
                var imageB64 = new List<string>();       // 纯 base64 —— Ollama 使用
                var imageDataUrls = new List<string>();  // data: URI  —— OpenAI 兼容 API 使用
                foreach (var img in t.ImagePaths)
                {
                    if (images.IndexOf(img) < 0) continue;

                    string b64 = ImageToBase64(img);
                    string mime = img.ToLower().EndsWith(".png") ? "image/png" : "image/jpeg";
                    imageB64.Add(b64);
                    imageDataUrls.Add($"data:{mime};base64,{b64}");
                }

                // 只有用户消息携带图片；assistant 消息只带文本
                bool hasText = !string.IsNullOrEmpty(t.Text);
                bool attachImages = !t.OwnByMyself && imageB64.Count > 0;

                // 既没有文本、也没有可发送的图片 → 整条消息跳过。
                // 注意：纯图片消息（Text 为空但有图片）必须保留，否则图片永远不会发出去。
                if (!hasText && !attachImages) continue;

                string text = hasText ? $"{t}" : "";

                var message = new Dictionary<string, object>
                {
                    ["role"] = t.OwnByMyself ? "assistant" : "user",
                };

                if (UseOllama)
                {
                    // Ollama /api/chat 格式：images 是与 content 平级的【纯 base64】数组（不带 data: 前缀）
                    message["content"] = text;
                    if (attachImages)
                    {
                        message["images"] = imageB64.ToArray();
                    }
                }
                else
                {
                    // OpenAI 兼容格式：content 可以是字符串，也可以是分段数组
                    if (!attachImages)
                    {
                        message["content"] = text;
                    }
                    else
                    {
                        var parts = new List<object>
                        {
                            new Dictionary<string, object>
                            {
                                ["type"] = "text",
                                ["text"] = text
                            }
                        };
                        foreach (var url in imageDataUrls)
                        {
                            parts.Add(new Dictionary<string, object>
                            {
                                ["type"] = "image_url",
                                ["image_url"] = new Dictionary<string, string>
                                {
                                    ["url"] = url
                                }
                            });
                        }
                        message["content"] = parts;
                    }
                }

                messages.Add(message);
            }

            return messages;
        }

        // --- 主逻辑：直接 POST 调用 API ---
        JsonSerializerOptions? jsonSerializerOptionsForPosting;
        JsonSerializerOptions? jsonSerializerOptionsForPrinting;
        public async Task<string?> GetAnswerAsync(List<ChatContent> text, string systemPrompt = "auto")
        {

            if (text == null || text.Count == 0) return "";

            // 内置模型
            if (Builtin)
            {
                foreach (var t in text.AsEnumerable().Reverse())
                {
                    if (string.IsNullOrEmpty(t.Text) || t.OwnByMyself) continue;
                    TinyLangJaccard ??= new TinyLangJaccardCS("datasetTiny.json");
                    return TinyLangJaccard.Answer(t.Text);
                }
                return "";
            }
            string extra = "{}";
            try
            {

                extra=File.ReadAllText("extra.json", new UTF8Encoding(false));
            }
            catch
            {

            }
           JsonDocument? extraJson;
            try
            {
             extraJson = JsonSerializer.Deserialize<JsonDocument>(extra);

            }
            catch
            {
                  extraJson=JsonSerializer.Deserialize<JsonDocument>("{}");
            }
            var mergedData = new Dictionary<string, object>();
            if (extraJson != null)
            {
                
                foreach (JsonProperty property in extraJson.RootElement.EnumerateObject())
                {
                    // property.Name 是键
                    // property.Value 是 JsonElement

                    // 注意：JsonElement 需要转换为具体类型才能存入 object
                    // 这里简单处理，根据类型转换
                    if (property.Value.ValueKind == JsonValueKind.String)
                        mergedData[property.Name] = property.Value.GetString()!;
                    else if (property.Value.ValueKind == JsonValueKind.Number)
                        mergedData[property.Name] = property.Value.GetDouble();
                    else if (property.Value.ValueKind == JsonValueKind.True || property.Value.ValueKind == JsonValueKind.False)
                        mergedData[property.Name] = property.Value.GetBoolean();
                    else if (property.Value.ValueKind == JsonValueKind.Null)
                        mergedData[property.Name] = "null";
                    else if (property.Value.ValueKind == JsonValueKind.Object)
                        // 嵌套对象可以递归处理，或者直接用 Utf8JsonWriter 写入
                        mergedData[property.Name] = JsonSerializer.Deserialize<object>(property.Value.GetRawText())!;
                    else if (property.Value.ValueKind == JsonValueKind.Array)
                        mergedData[property.Name] = JsonSerializer.Deserialize<object[]>(property.Value.GetRawText()!)!;
                }
            }
            string finalJson = JsonSerializer.Serialize(mergedData);
            Log.Print(finalJson);

            //foreach(var (k,v) in extraJson )
            // 系统提示
            string finalSystemPrompt = systemPrompt switch
            {
                "auto" => SysPmpt,
                "" or "None" => "",
                _ => systemPrompt
            };

            // 收集图片
            var imageList = new List<string>();
            var reversedText = new List<ChatContent>(text.ToArray());
            reversedText.Reverse();
            foreach (var t in reversedText)
            {
                if (!t.OwnByMyself)
                {
                    foreach (var img in t.ImagePaths)
                    {
                        if (File.Exists(img))
                        {
                            imageList.Add(img);
                            if (imageList.Count >= MaxImageCount) break;
                        }
                        else
                        {
                            Log.Print($"× 没有找到图片 {img}",Log.Stat.WARN);
                        }
                    }
                    if (imageList.Count >= MaxImageCount) break;
                }
            }

            // 构建 messages
            var messages = new List<Dictionary<string, object>>();
            if (!string.IsNullOrEmpty(finalSystemPrompt))
            {
                messages.Add(new Dictionary<string, object>
                {
                    ["role"] = "system",
                    ["content"] = finalSystemPrompt
                });
            }

            messages.AddRange(ConcatenateText(text, imageList));

            // 构造请求体
            var requestBody = new Dictionary<string, object>
            {
                ["model"] = ModelName,
                ["messages"] = messages,
                ["stream"] = false,
            };

            foreach(KeyValuePair<string, object> k in mergedData)
            {
                requestBody[k.Key]= k.Value;
            }

            jsonSerializerOptionsForPosting ??= new JsonSerializerOptions { WriteIndented = false };
            string json = JsonSerializer.Serialize(requestBody,jsonSerializerOptionsForPosting! );


            var content = new StringContent(json, Encoding.UTF8, "application/json");


            // 设置 Headers
            if (!string.IsNullOrEmpty(ApiKey) && !ServerUrl.Contains("localhost") && !ServerUrl.Contains("127.0.0.1"))
            {
                _httpClient.DefaultRequestHeaders.Authorization =
                    new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", ApiKey);
            }
            else
            {
                _httpClient.DefaultRequestHeaders.Authorization = null;
            }   

            try
            {
                var startTime = DateTime.UtcNow;
                HttpResponseMessage response;
                jsonSerializerOptionsForPrinting ??= new JsonSerializerOptions
                {
                    Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
                    WriteIndented = true // 可选：美化输出
                };
                try
                {

                File.WriteAllText("dest.json", JsonSerializer.Serialize(requestBody, jsonSerializerOptionsForPrinting!));
                }catch
                {

                }

                if (! UseOllama)
                {

           
                    Log.Print($"Sending request to: {ServerUrl}/chat/completions");


                    response = await _httpClient.PostAsync($"{ServerUrl}/chat/completions", content);
                }
                else
                {
                    Log.Print($"Sending request to: {ServerUrl}");

                    response = await _httpClient.PostAsync(ServerUrl, content);

                }
                string responseBody = await response.Content.ReadAsStringAsync();

                if (!response.IsSuccessStatusCode)
                {
                    Log.Print($"API Error: {response.StatusCode} - {responseBody}",Log.Stat.ERROR);
                    return null;
                }
                

                Log.Print($"\n\nResponse:\n");
                Log.Print(responseBody.ToString());

                using JsonDocument doc = JsonDocument.Parse(responseBody);
                string? answer = null;
                if (UseOllama)
                {
                    answer = doc.RootElement
                        .GetProperty("message")
                        .GetProperty("content")
                        .GetString();
                }
                else
                {
                    answer = doc.RootElement
                        .GetProperty("choices")[0]
                        .GetProperty("message")
                        .GetProperty("content")
                        .GetString();
                }
                try
                {
                    if (doc.RootElement.TryGetProperty("usage", out JsonElement usage))
                    {
                        int promptTokens = usage.TryGetProperty("prompt_tokens", out var pt) ? pt.GetInt32() : 0;
                        int completionTokens = usage.TryGetProperty("completion_tokens", out var ct) ? ct.GetInt32() : 0;
                        int totalTokens = usage.TryGetProperty("total_tokens", out var tt) ? tt.GetInt32() : 0;

                        Log.Print($"Token 用量: 输入 {promptTokens} | 输出 {completionTokens} | 总计 {totalTokens}");
                        TotalTokens += totalTokens;
                    }
                    string? reason = doc.RootElement //Deepseek
                        .GetProperty("choices")[0]
                        .GetProperty("message")
                        .GetProperty("reasoning_content")
                        .GetString();  
                    reason ??= doc.RootElement  //Ollama
                        .GetProperty("message")
                        .GetProperty("thinking")
                        .GetString();

                    if (reason is not null)
                    {
                        Log.SetColor(ConsoleColor.Gray);
                        Log.Print($"<think>\n{reason}\n</think>");
                        
                    }
                } catch (Exception ex)
                {
                    //Log.Print(ex.ToString(),Log.Stat.ERROR);
                }

                var elapsed = (DateTime.UtcNow - startTime).TotalSeconds;
                Log.Print($"用时 {elapsed:F2}s");
                Log.Print(answer?.Trim()??"");

                return answer?.Trim();
            }
            catch (Exception ex)
            {
                Log.Print($"HTTP request failed: {ex.Message}",Log.Stat.ERROR);
                return null;
            }
        }

        // 同步版本
        public string? GetAnswer(List<ChatContent> text, string systemPrompt = "auto")
        {
            return GetAnswerAsync(text, systemPrompt).GetAwaiter().GetResult();
        }

        public void Test()
        {
            try
            {
                //UseOllama = true;
                ServerUrl = "http://localhost:8080/api/chat";
                ForceOllamaAPI= true;
                //ChatContent c = ;
                Log.Print($"[ASSISTANT]: {GetAnswer([
                    new("Username1", [], "你好", DateTime.Now.ToShortDateString(), false),
                    //new("Username3", [], "1",DateTime.Now.ToShortDateString(), false),
                    //new("Username2", [], "1", DateTime.Now.ToShortDateString(), false),
                    //new("Username4", [], "1", DateTime.Now.ToShortDateString(), false),
                    //new("Username5", ["C:\\Users\\Develop\\Downloads\\juniorcuisine-template-26.2\\src\\main\\resources\\assets\\juniorcuisine\\textures\\item\\slime_podding.png"], "这是什么图片 /no_think", "", false),
                    //new("Username5", ["C:\\Users\\Develop\\Downloads\\juniorcuisine-template-26.2\\src\\main\\resources\\assets\\juniorcuisine\\textures\\item\\magma_cream_podding.png"], "这是什么图片 /no_think", "", false),
                    //new("Username5", ["C:\\Users\\Develop\\Downloads\\juniorcuisine-template-26.2\\src\\main\\resources\\assets\\juniorcuisine\\textures\\item\\nether_stew.png"], "这是什么图片 /no_think", "", false),
                    ])}");
            }
            catch (Exception ex)
            {
                Log.Print($"Test failed: {ex.Message}"  , Log.Stat.ERROR);
            }
        }
    }
}