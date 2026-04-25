import os
import sqlite3
from time import time
from collections import defaultdict

start = time()

# === 第一步：确保 dataset.db 存在（可选：自动转换逻辑可放 compressDatasetSqlite）===
if not os.path.exists('dataset.db'):
    import compressDatasetSqlite
# === 第二步：从 SQLite 加载全量问答对 ===
import dbconnect
questions, answers = dbconnect.questions, dbconnect.answers
question_sets = [set(q) for q in questions]

print(f"共加载 {len(questions)} 条问答对")

# === 第三步：构建字符倒排索引（和原来一样）===
char_to_questions = defaultdict(set)
for idx, q in enumerate(questions):
    for char in q:
        char_to_questions[char].add(idx)

# === 第四步：保留你的 Jaccard 匹配函数 ===
def answer_fast(question):
    q_set = set(question)
    candidate_indices = set()
    
    # 收集所有包含任一字符的问题索引
    for char in q_set:
        candidate_indices |= char_to_questions.get(char, set())
    
    if not candidate_indices:
        candidate_indices = range(len(questions))
    
    max_sim = -1
    best_idx = 0
    q_len = len(q_set)
    
    for idx in candidate_indices:
        q_set_i = question_sets[idx]
        inter = len(q_set & q_set_i)
        union = q_len + len(q_set_i) - inter
        sim = inter / union if union > 0 else 0.0
        
        if sim > max_sim:
            max_sim = sim
            best_idx = idx
    
    ans = answers[best_idx] 
    print(ans)
    return ans

print(f'准备完成: {time() - start:.2f}s')

if __name__ == '__main__':
    print('TinyLangJaccard-Swiftness-Sqlite 测试')
    print('数据集:https://modelscope.cn/datasets/qiaojiedongfeng/qiaojiedongfeng')
    while True:
        try:
            question = input('请输入问题: ')
            if not question.strip():
                continue
            start_time = time()
            answer_fast(question)
            print(f'耗时: {time() - start_time:.2f}s')
        except (KeyboardInterrupt, EOFError):
            print("\n再见！")
            break








#