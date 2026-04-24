using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace QQPilot4
{
    public class TinyLangJaccardCS
    {
        private readonly Dictionary<string, string> _qaPairs;
        private readonly List<string> _questions;

        public TinyLangJaccardCS(string jsonFilePath)
        {
            if (!File.Exists(jsonFilePath))
                throw new FileNotFoundException($"Dataset file not found: {jsonFilePath}");

            string jsonContent = File.ReadAllText(jsonFilePath);
            _qaPairs = System.Text.Json.JsonSerializer.Deserialize<Dictionary<string, string>>(jsonContent) ??
                       throw new InvalidOperationException("Failed to parse JSON.");

            _questions = new List<string>(_qaPairs.Keys);
        }

        /// <summary>
        /// 计算两个字符串的 Jaccard 相似度（基于字符集合）
        /// </summary>
        private static double JaccardSimilarity(string s1, string s2)
        {
            if (string.IsNullOrEmpty(s1) && string.IsNullOrEmpty(s2)) return 1.0;
            if (string.IsNullOrEmpty(s1) || string.IsNullOrEmpty(s2)) return 0.0;

            var set1 = s1.ToHashSet();
            var set2 = s2.ToHashSet();

            var intersection = set1.Intersect(set2).Count();
            var union = set1.Union(set2).Count();

            return union == 0 ? 0.0 : (double)intersection / union;
        }

        /// <summary>
        /// 根据输入问题，返回最相似问题对应的答案
        /// </summary>
        public string Answer(string question)
        {
            if (_questions.Count == 0)
                throw new InvalidOperationException("No questions loaded.");

            string bestMatch = _questions[0];
            double maxSimilarity = -1.0;

            foreach (string q in _questions)
            {
                double similarity = JaccardSimilarity(question, q);
                if (similarity > maxSimilarity)
                {
                    maxSimilarity = similarity;
                    bestMatch = q;
                }
            }

            string answer = _qaPairs[bestMatch];
            Console.WriteLine(answer); // 模拟 print
            return answer;
        }
    }
}