from flask import Flask, jsonify, request, make_response, abort
from models import todos

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/api/v1/todos/", methods=["GET"])
def todos_list_api_v1():
    return jsonify(todos.all())


@app.route("/api/v1/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    return jsonify({"todo": todo})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.route("/api/v1/todos/", methods=["POST"])
def create_todo():
    if not request.json or not 'title' in request.json:
        abort(400)
    todo = {
        'id': todos.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'year': request.json.get('year',),
        'genre': request.json.get('genre', ""),
        'description': request.json.get('description', ""),
        'watched': False
    }
    todos.create(todo)
    return jsonify({'todo': todo}), 201

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.route("/api/v1/todos/<int:todo_id>", methods=['DELETE'])
def delete_todo(todo_id):
    result = todos.delete(todo_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'year' in data and not isinstance(data.get('year'), int),
        'genre' in data and not isinstance(data.get('genre'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'watched' in data and not isinstance(data.get('watched'), bool)
    ]):
        abort(400)
    todo = {
        'title': data.get('title', todo['title']),
        'year': data.get('year', todo['year']),
        'genre': data.get('genre', todo['genre']),
        'description': data.get('description', todo['description']),
        'watched': data.get('watched', todo['watched'])
    }
    todos.update(todo_id, todo)
    return jsonify({'todo': todo})

if __name__ == "__main__":
    app.run(debug=True)

