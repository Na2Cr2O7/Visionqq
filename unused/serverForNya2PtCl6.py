from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

url = 'http://127.0.0.1:5000'
def getAnswer(question:str,)->str:
    posturl=url+f'/anyModel/{question}'
    try:
        response = requests.post(posturl)
        if response.status_code == 200:
            result = json.loads(response.text)
            answer=result['answer']
            return answer
        else:
            return ''
    except:
        return ''
    
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "缺少字段 'text'"}), 400

    question = data['text']
    try:
        answer = getAnswer(question)
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8800, debug=False)