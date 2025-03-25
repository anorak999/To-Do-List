# 📝 Python To-Do List Manager


A lightweight, command-line to-do list application with persistent storage.

## ✨ Features
- Add, complete, and delete tasks
- Tasks saved automatically to JSON file
- Simple keyboard-driven interface
- Color-coded task status (using Colorama)

## 🛠️ Requirements
- Python 3.8+
- `colorama` package (for colored output)

## ⚡ Quick Start
```bash
git clone https://github.com/yourusername/python-todo-list.git
cd python-todo-list
pip install colorama
python todo.py
```

## ⌨️ Basic Commands
```
+ [task]       Add new task
✓ [number]     Mark task as complete
- [number]     Delete task
l              List all tasks
c              Clear completed tasks
q              Save and quit
```

## 📂 Project Structure
```
todo-list/
├── todo.py          # Main application logic
├── tasks.json       # Auto-generated task storage
├── requirements.txt # Dependencies
└── README.md
```

## 🚀 Future Improvements
- Due dates and reminders
- Priority levels for tasks
- Category tagging system
