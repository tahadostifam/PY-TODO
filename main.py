import os 
import time
import sqlite3
from tabulate import tabulate

def clear_page():
    os.system('clear')

clear_page()

connection = None

def connect_to_db():
    global cursor, connection 
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    print("+ Connected To Database Successfully!")
    main()

def welcome_page():
    clear_page()
    text = """
Welcome To tahadostifam Python Todo-App
---------------------------------------
c  -> clear screen
n  -> new todo
d  -> delete todo
j  -> update todo state
v  -> view all todo's
p  -> view in-progress todo's
\q -> to exit from current command
---------------------------------------
l  -> export all todo's
---------------------------------------
e  -> exit
    """.strip()
    print(text)
    get_input()

def get_input():
    while True:
        cmd = input("Enter You're Command -> ").strip()
        if cmd and len(cmd) == 1:
            exec_user_commands(cmd)
        else:
            welcome_page()
            break
    
def print_todos_table(data):
    table_rows = []
    for row in data:
        table_rows.append([row[0], row[1], row[2], row[3]])
    table = tabulate(table_rows, headers=['id', 'header', 'detail', 'state'])
    print('\n')
    print(table)
    print('\n')
            
def exec_user_commands(command):
    if command == 'c':
        welcome_page()
    elif command == 'e':
        connection.close()
        time.sleep(0.3)
        exit()
    elif command == 'v':
        result = exec_query("SELECT * from tbl_todos")
        print_todos_table(result)
    elif command == 'p':
        result = exec_query("SELECT * from tbl_todos where state='in-progress'")
        print_todos_table(result)
    elif command == 'n':
        create_new_todo()
    elif command == 'd':
        delete_todo()
    elif command == 'j':
        update_todo_state()
    elif command == 'l':
        export_all_todos()

def create_new_todo():
    header = input("Enter Todo Header -> ")
    if header == '\q':
        return 

    detail = input("Enter Todo Detail -> ")
    if detail == '\q':
      return

    if len(header) > 0:
        exec_query(f"insert into tbl_todos (header, detail, state) VALUES('{header}', '{detail}', 'in-progress')")
        connection.commit()
        print("Todo Saved Successfully! :)))")
    else:
        print("header cannot be empty...!")
        create_new_todo()
    
def delete_todo():
    id = input("Enter Todo id -> ")

    if id == '\q':
      return

    if len(id) > 0:
        todo_search_result = exec_query(f"SELECT * from tbl_todos where id={id}")
        if len(todo_search_result) > 0:    
            exec_query(f"delete from tbl_todos where id={id}")
            connection.commit()
            print("Todo Deleted Successfully! :)))")
        else:
            print("todo not exist...!")
            delete_todo()        
    else:
        print("id cannot be empty...!")
        delete_todo()

def update_todo_state():
    id = input("Enter Todo id -> ")
    if id == '\q':
      return
      
    state_id = input("Select State (1=in-progress, 2=done) -> ")
    if state_id == '\q':
      return

    if len(id) > 0 and len(state_id) > 0:
        todo_search_result = exec_query(f"SELECT * from tbl_todos where id={id}")
        if len(todo_search_result) > 0:
            states = ['in-progress', 'done']
            set_todo_state_value = None
            if state_id == '1':
              set_todo_state_value = states[0]
            elif state_id == '2':
                set_todo_state_value = states[1]
            else:
                print("Selected State Not Valid!!!")
                update_todo_state()
                return 
            exec_query(f"update tbl_todos set state='{set_todo_state_value}' where id={id}")
            connection.commit()
            print("Todo State Changed! :)))")
        else:
            print("todo not exist...!")
            update_todo_state()        
    else:
        print("id and state_id cannot be empty...!")
        update_todo_state()

def export_all_todos():
    table_result = exec_query(f"SELECT * from tbl_todos")
    filename = input("Enter File Name (without format) ->")
    if filename == '\q':
        return 

    if len(filename) > 0:
        table_rows = []
        for row in table_result:
            table_rows.append([row[0], row[1], row[2], row[3]])
        table = tabulate(table_rows, headers=['id', 'header', 'detail', 'state'])
        try:
            f = open(filename, 'w')
            f.write(table)
            f.close()
            print("Data Exported Successfully :)))")
        except:
            print("Error in Write File :(((")
    else:
        print("file name cannot be empty")
        export_all_todos()

def exec_query(query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result
    
def main():
    welcome_page()
    
connect_to_db()