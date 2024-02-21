// TodoList.js
import React, { useState, useEffect } from 'react';

function TodoList() {
    const [todos, setTodos] = useState([]);

    useEffect(() => {
        // Fetch todos from the Flask API
        fetch('http://localhost:5000/todos')
            .then(response => response.json())
            .then(data => setTodos(data))
            .catch(error => console.error('Error fetching todos:', error));
    }, []); // Empty array means this effect runs once on component mount

    return (
        <ul>
            {todos.map(todo => (
                <li key={todo.id}>{todo.task}</li>
            ))}
        </ul>
    );
}

export default TodoList;
