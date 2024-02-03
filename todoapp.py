from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory list of todo items
todos = []

@app.route('/todos', methods=['POST'])
def add_todo():

    # Get the task and add a corresponding ID
    todo = request.json.get('task', '')
    new_id = max(todo['id'] for todo in todos) + 1 if todos else 1

    # Add the task and initialize completion as incomplete
    todos.append({'id': new_id, 'task': todo, 'completed': False})

    # Return the result to the user, which is 0-indexed
    return jsonify(get_todo(new_id)), 201

@app.route('/todos/<int:task_id>', methods=['DELETE'])
def delete_todo_route(task_id):
    if delete_todo(task_id):
        return jsonify({'message': 'Todo removed successfully'}), 200
    else:
        return jsonify({'error': 'Todo not found'}), 404
    
@app.route('/todos/<int:task_id>', methods=['PUT'])
def update_todo_route(task_id):
    data = request.json
    success = update_todo(task_id, new_task=data.get('task'), new_completed=data.get('completed'))
    if success:
        return jsonify({'message': 'Todo updated successfully'}), 200
    else:
        return jsonify({'error': 'Todo not found'}), 404


# Route to get all todo items
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify({'todos': todos})

# Get a todo item
def get_todo(task_id):
    return next((todo for todo in todos if todo['id'] == task_id), None)

# Remove a todo
def delete_todo(task_id):
    todo_to_remove = next((todo for todo in todos if todo['id'] == task_id), None)
    if todo_to_remove is not None:
        todos.remove(todo_to_remove)
        print(f"Todo with id {task_id} was removed successfully.")
        return True
    else:
        print(f"Todo with id {task_id} was not found.")
        return False
    
def update_todo(task_id, new_task=None, new_completed=None):
    for todo in todos:
        if todo['id'] == task_id:
            if new_task is not None:
                todo['task'] = new_task
            if new_completed is not None:
                todo['completed'] = new_completed
            return True
    return False

if __name__ == '__main__':
    app.run(debug=True)