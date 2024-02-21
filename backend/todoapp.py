from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

# Handle CORS in the Flask app to allow requests from your React app's origin.
CORS(app)

# In-memory list of todos
todos = []

# Add a todo the list of todos
@app.route('/todos', methods=['POST'])
def add_todo():

    app.logger.debug("Adding todos")

    # Get the task and add a corresponding ID
    todo = request.json.get('task', '')

    if not todo:
        return jsonify({'error': 'The task field is required.'}), 400
    
    new_id = len(todos)+1
    todos.append({'id': new_id, 'task': todo, 'completed': False})

    return jsonify(get_todo(new_id)), 201

# Delete a todo
@app.route('/todos/<int:task_id>', methods=['DELETE'])
def delete_todo_route(task_id):

    app.logger.debug("Deleting todos")

    if delete_todo(task_id):
        return jsonify({'message': 'Todo removed successfully'}), 200
    else:
        return jsonify({'error': 'Todo not found'}), 404
    
@app.route('/todos/<int:task_id>', methods=['PUT'])
def update_todo_route(task_id):

    app.logger.debug("Updating todos")

    data = request.json
    success = update_todo(task_id, new_task=data.get('task'), new_completed=data.get('completed'))
    if success:
        return jsonify({'message': 'Todo updated successfully'}), 200
    else:
        return jsonify({'error': 'Todo not found'}), 404


# Get all todos
@app.route('/todos', methods=['GET'])
def get_todos():

    app.logger.debug("Getting todos")
    
    return jsonify({'todos': todos})

# Get a todo by id
def get_todo(task_id):
    return next((todo for todo in todos if todo['id'] == task_id), None)

# Remove a todo by id
def delete_todo(task_id):

    todo_to_remove = next((todo for todo in todos if todo['id'] == task_id), None)

    if todo_to_remove is not None:
        todos.remove(todo_to_remove)
        print(f"Todo with id {task_id} was removed successfully.")
        return True
    else:
        print(f"Todo with id {task_id} was not found.")
        return False
    
# Look for and update the todo if found in the list
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