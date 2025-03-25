import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttb
from ttkbootstrap.constants import *
from datetime import datetime
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo App")
        self.root.geometry("600x500")
        
        # Initialize data
        self.tasks = []
        self.tasks_file = "tasks.json"
        self.load_tasks()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=BOTH, expand=YES)
        
        # Create input area
        self.create_input_area()
        
        # Create task list
        self.create_task_list()
        
        # Create buttons
        self.create_buttons()
        
        # Load tasks
        self.refresh_task_list()
        
        # Set up auto-save
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_input_area(self):
        # Input frame
        input_frame = ttk.LabelFrame(self.main_frame, text="Add New Task", padding="10")
        input_frame.pack(fill=X, pady=5)
        
        # Task entry
        self.task_var = tk.StringVar()
        ttk.Label(input_frame, text="Task:").grid(row=0, column=0, padx=5)
        ttk.Entry(input_frame, textvariable=self.task_var, width=40).grid(row=0, column=1, padx=5)
        
        # Priority selection
        self.priority_var = tk.StringVar(value="Medium")
        ttk.Label(input_frame, text="Priority:").grid(row=0, column=2, padx=5)
        ttk.Combobox(input_frame, textvariable=self.priority_var, 
                    values=["High", "Medium", "Low"], width=10, state="readonly").grid(row=0, column=3, padx=5)
        
        # Add button
        ttk.Button(input_frame, text="Add Task", command=self.add_task).grid(row=0, column=4, padx=5)

    def create_task_list(self):
        # Create Treeview
        columns = ("Task", "Priority", "Status")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.tree.heading("Task", text="Task")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("Task", width=300)
        self.tree.column("Priority", width=100)
        self.tree.column("Status", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES, pady=5)
        scrollbar.pack(side=RIGHT, fill=Y, pady=5)

    def create_buttons(self):
        # Button frame
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=X, pady=5)
        
        # Buttons
        ttk.Button(btn_frame, text="Complete", command=self.complete_task).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_task).pack(side=LEFT, padx=5)

    def add_task(self):
        task = self.task_var.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Please enter a task!")
            return
            
        priority = self.priority_var.get()
        
        new_task = {
            "task": task,
            "priority": priority,
            "status": "Pending",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.tasks.append(new_task)
        self.save_tasks()
        self.refresh_task_list()
        
        # Clear input
        self.task_var.set("")
        self.priority_var.set("Medium")

    def complete_task(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a task to mark as complete!")
            return
            
        for item_id in selected_items:
            task_idx = self.get_task_index(item_id)
            if task_idx is not None:
                if self.tasks[task_idx]["status"] == "Completed":
                    self.tasks[task_idx]["status"] = "Pending"
                else:
                    self.tasks[task_idx]["status"] = "Completed"
            
        self.save_tasks()
        self.refresh_task_list()

    def delete_task(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
            
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete {len(selected_items)} task(s)?"):
            for item_id in selected_items:
                task_idx = self.get_task_index(item_id)
                if task_idx is not None:
                    del self.tasks[task_idx]
            self.save_tasks()
            self.refresh_task_list()

    def get_task_index(self, item_id):
        try:
            task_values = self.tree.item(item_id)['values']
            return next(i for i, task in enumerate(self.tasks) 
                       if task["task"] == task_values[0] and 
                       task["priority"] == task_values[1])
        except (StopIteration, IndexError):
            return None

    def refresh_task_list(self):
        self.tree.delete(*self.tree.get_children())
        
        for task in self.tasks:
            values = (
                task["task"],
                task["priority"],
                task["status"]
            )
            tags = ("completed",) if task["status"] == "Completed" else ()
            self.tree.insert("", END, values=values, tags=tags)
        
        # Configure tag colors
        self.tree.tag_configure("completed", foreground="gray")

    def save_tasks(self):
        try:
            with open(self.tasks_file, "w") as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")

    def load_tasks(self):
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, "r") as f:
                    self.tasks = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
            self.tasks = []
            
    def on_closing(self):
        """Handle application closing"""
        self.save_tasks()
        self.root.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = TodoApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
