import os 
import time
import sqlite3
from tabulate import tabulate

def clear_page():
    os.system('cls')

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
c -> clear screen
n -> new todo
d -> delete todo
v -> view all todo's
p -> view in-progress todo's
s -> search in todo's
---------------------------------------
e - exit
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

def create_new_todo():
    header = input("Enter Todo Header -> ")
    detail = input("Enter Todo Detail -> ")
    if len(header) > 0:
        exec_query(f"insert into tbl_todos (header, detail, state) VALUES('{header}', '{detail}', 'in-progress')")
        connection.commit()
        print("Todo Saved Successfully! :)))")
    else:
        print("header cannot be empty...!")
        create_new_todo()
    
def delete_todo():
    id = input("Enter Todo id -> ")
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

def exec_query(query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result
    
def main():
    welcome_page()
    
connect_to_db()