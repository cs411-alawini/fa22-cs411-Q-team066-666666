"""Defines all the functions related to the database"""
from app._init_ import db

# def fetch_todo():
#     todo_list = [
#     {"id": 1, "task": "Task 1" , "status": "In Progress"},
#     {"id": 2, "task": "Task 2", "status": "Todo"},\
#     ]
#     return todo_list

def fetch_todo() -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from Company;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[1],
            "task": result[2],
            "status": result[3]
        }
        todo_list.append(item)

    return todo_list


# def update_task_entry(task_id: int, text: str) -> None:
#     """Updates task description based on given `task_id`

#     Args:
#         task_id (int): Targeted task_id
#         text (str): Updated description

#     Returns:
#         None
#     """

#     conn = db.connect()
#     query = 'Update tasks set task = "{}" where id = {};'.format(text, task_id)
#     conn.execute(query)
#     conn.close()


# def update_status_entry(task_id: int, text: str) -> None:
#     """Updates task status based on given `task_id`

#     Args:
#         task_id (int): Targeted task_id
#         text (str): Updated status

#     Returns:
#         None
#     """

#     conn = db.connect()
#     query = 'Update tasks set status = "{}" where id = {};'.format(text, task_id)
#     conn.execute(query)
#     conn.close()


def insert_new_task(text: str) ->  str:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query = 'Insert Into tasks (CompanyId, Status) VALUES ("{}", "{}");'.format(
        text, "Unfollow")
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][1]
    conn.close()

    return task_id


def remove_task_by_id(task_id: str) -> None:
    """ remove entries based on task ID """
    # print(2)
    conn = db.connect()
    query = 'Delete From Company where CompanyID="{}";'.format(task_id)
    print(task_id)
    conn.execute(query)
    conn.close()
