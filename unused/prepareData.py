import json
pair={}
with open('train.jsonl', 'r', encoding='utf8') as f:
    questions=[]
    answers=[]
    for line in f:

        data = json.loads(line)
        questions.append(data['conversation'][0]['human'])
        answers.append(data['conversation'][0]['assistant'])
        pair[data['conversation'][0]['human']]=data['conversation'][0]['assistant']

char_to_idx={char:idx for idx,char in enumerate(set(''.join(questions+answers)))}
with open('tokenizer.json','w',encoding='utf8') as f:
    json.dump(char_to_idx,f,ensure_ascii=False)
with open('datasetTiny.jsonl', 'w', encoding='utf8') as f:
    json.dump(pair,f,ensure_ascii=False)

print("√ 数据处理完成")