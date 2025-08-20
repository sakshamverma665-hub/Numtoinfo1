from flask import Flask, request, send_file, jsonify, after_this_request
import requests
import os

app = Flask(__name__)

API_URL = "https://xploide.site/Api.php?num={}"

@app.route("/")
def home():
    return jsonify({"message": "API is running! Use /get?num=987654321"})

@app.route("/get")
def get_info():
    num = request.args.get("num")

    if not num or not num.isdigit():
        return jsonify({"error": "Please provide a valid number ?num=1234567890"})

    try:
        url = API_URL.format(num)
        response = requests.get(url, timeout=10)

        if response.status_code == 200 and response.text.strip():
            result = response.text.strip()

            file_name = f"{num}.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(result + "\n\nOwner : @Saksham24_11")

            @after_this_request
            def cleanup(response):
                if os.path.exists(file_name):
                    os.remove(file_name)
                return response

            return send_file(file_name, as_attachment=True)

        else:
            return jsonify({"error": "API did not return data"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render ka dynamic port
    app.run(host="0.0.0.0", port=port)