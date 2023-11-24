import datetime
import pickle
import PySimpleGUI as sg

sg.theme('DarkGrey5')

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task, due_date=None):
        task_info = {'task': task, 'due_date': due_date}
        self.tasks.append(task_info)

    def remove_task(self, index):
        if 1 <= index <= len(self.tasks):
            del self.tasks[index - 1]
            return True
        return False

    def show_tasks(self):
        task_list = []
        for i, task_info in enumerate(self.tasks, 1):
            task = task_info['task']
            due_date = task_info['due_date']
            if due_date:
                task_list.append(f"{i}. {task} (Due: {due_date})")
            else:
                task_list.append(f"{i}. {task}")
        return task_list


def main():
    to_do_list = ToDoList()

    try:
        with open('tasks.pkl', 'rb') as f:
            to_do_list.tasks = pickle.load(f)
    except FileNotFoundError:
        pass

    layout = [
        [sg.Text("To-Do List")],
        [sg.Button("Add Task"), sg.Button("Remove Task"), sg.Button("Show Tasks")],
        [sg.Listbox(values=to_do_list.show_tasks(), size=(40, 10), key="tasks")],
        [sg.Button("Exit")]
    ]

    window = sg.Window("To-Do List", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            with open('tasks.pkl', 'wb') as f:
                pickle.dump(to_do_list.tasks, f)
            print("Exiting the to-do list program. Goodbye!")
            break
        elif event == "Add Task":
            new_task = sg.popup_get_text("Enter the task:")
            due_date_str = sg.popup_get_text("Enter the due date (optional, format: YYYY-MM-DD):")
            due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
            to_do_list.add_task(new_task, due_date)
            window["tasks"].update(values=to_do_list.show_tasks())
        elif event == "Remove Task":
            index_to_remove = sg.popup_get_text("Enter the index of the task to remove:")
            if index_to_remove.isdigit():
                index_to_remove = int(index_to_remove)
                if to_do_list.remove_task(index_to_remove):
                    window["tasks"].update(values=to_do_list.show_tasks())
                else:
                    sg.popup_error(f"Invalid index or task not found.")
            else:
                sg.popup_error("Please enter a valid index.")
        elif event == "Show Tasks":
            sg.popup("\n".join(to_do_list.show_tasks()))

    window.close()

if __name__ == "__main__":
    main()