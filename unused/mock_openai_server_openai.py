# mock_openai_server_flask.py
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/v1/chat/completions', methods=['POST'])
def mock_chat_completions():
    # 获取请求头
    headers = dict(request.headers)
    
    # 获取并解析请求体
    try:
        body = request.get_json(force=True)
    except Exception as e:
        return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400

    # 调试输出
    print("\n" + "="*70)
    print("🟢 收到 OpenAI API 请求")
    print("="*70)
    print("Headers:")
    for k, v in headers.items():
        print(f"  {k}: {v}")
    print("\nRequest Body (JSON):")
    print(json.dumps(body, indent=2, ensure_ascii=False))
    print("="*70)

    # 检查必要字段
    if not body or 'model' not in body:
        return jsonify({"error": "Missing 'model' in request body"}), 400

    # 构造模拟响应（符合 OpenAI 官方格式）
    response = {
        "id": "chatcmpl-mock123",
        "object": "chat.completion",
        "created": 1700000000,
        "model": body["model"],
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "✅ 这是来自 Flask Mock OpenAI 服务器的测试回复。你的请求结构正确！"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 15,
            "completion_tokens": 25,
            "total_tokens": 40
        }
    }

    return jsonify(response)


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Mock OpenAI Server is running!",
        "endpoint": "/v1/chat/completions"
    })


if __name__ == '__main__':
    print("🚀 启动 Flask Mock OpenAI 服务器...")
    print("监听地址: http://localhost:8000/v1/chat/completions")
    print("请在 config.ini 中设置:")
    print("  server_url = http://localhost:8000/v1")
    print("  API_KEY = 任意值（如 test-key）")
    print("\n等待请求中...（按 Ctrl+C 停止）\n")
    app.run(host='127.0.0.1', port=8000, debug=False)