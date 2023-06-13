from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello, World!"


@app.route('/form', methods=['POST'])
def process_form():
    data = request.get_json()
    name = data.get('name', None)
    # 在这里执行对表单数据的处理逻辑'
    print("name:", name)
    data = {
        'name': "name",
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run()
