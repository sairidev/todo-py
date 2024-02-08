from tkinter  import *
import sqlite3

root = Tk()
root.title('Todo List')
root.geometry('500x500')

# db connection
connection = sqlite3.connect('todo.db')
sql = connection.cursor()

sql.execute("""
  CREATE TABLE IF NOT EXISTS todo (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
         description TEXT NOT NULL,
         completed BOOLEAN NOT NULL
  );
""")

connection.commit()

# functions
def add():
  todo = e.get()
  if todo:
    sql.execute(f'INSERT INTO todo (description, completed) VALUES (?, ?)', (todo, False))
    connection.commit()
    e.delete(0, END)
    render_todos()
  else:
    pass

root.bind('<Return>', lambda x: add())

def complete(id):
  def _complete(): #currying
    todo = sql.execute(f'SELECT * FROM todo WHERE id={id}').fetchone()
    sql.execute(f'UPDATE todo SET completed = {not todo[3]} WHERE id = {id}')
    connection.commit()
    render_todos()
  return _complete

def remove(id):
  def _remove():
    sql.execute(f'DELETE FROM todo WHERE id = {id}')
    connection.commit()
    render_todos()
  return _remove

def render_todos():
  rows = sql.execute('SELECT * FROM todo').fetchall()

  for widget in frame.winfo_children():
    widget.destroy()

  for i in range(0, len(rows)):
    id = rows[i][0]
    completed = rows[i][3]
    description = rows[i][2]

    color = 'gray' if completed else 'black'
    check_btn = Checkbutton(frame, text=description, fg=color, width=42, anchor='w', command=complete(id))
    check_btn.grid(row=i, column=0, sticky='w')
    check_btn.select() if completed else check_btn.deselect()

    delete_btn = Button(frame, text='delete', command=remove(id))
    delete_btn.grid(row=i, column=1)

# ui
l = Label(root, text='Todo')
l.grid(row=0, column=0)

e = Entry(root, width=40)
e.grid(row=0, column=1)
e.focus()

btn = Button(root, text='Add', command=add)
btn.grid(row=0, column=2)

frame = LabelFrame(root, text='Todos', pady=5, padx=5)
frame.grid(row=1, column=0, columnspan=3, sticky='nswe', padx=5)

root.mainloop()