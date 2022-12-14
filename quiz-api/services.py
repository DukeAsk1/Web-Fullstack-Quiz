from models import Question
import sqlite3

def post_question(list_question):
    input_question = Question()
    input_question.from_json(list_question)

    # create a connection
    db_connection = sqlite3.connect("./tuto.db")

    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None

    cur = db_connection.cursor()
    # start transaction
    cur.execute("begin")

    try:
    # Use the cursor to execute an INSERT statement
        insertion_result = cur.execute(
        f"insert into Question (position,title,text,image) values"
        f"({input_question.position!r},{input_question.title!r},"
        f"{input_question.text!r},{input_question.image!r})")

    except sqlite3.Error as e:
    # If an error occurred, print the error message
        print(f"An error occurred: {e.args[0]}")
        return {"error" : {e.args[0]}}, 500

    # send the request
    cur.execute("commit")

    # # in case of exception, rollback the transaction
    # cur.execute('rollback')


    return {"id":cur.lastrowid}, 200

def get_question_by_id(id):
    # create a connection
    db_connection = sqlite3.connect("./tuto.db")

    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None

    cur = db_connection.cursor()
    # start transaction
    cur.execute("begin")

    try:
    # Use the cursor to execute an INSERT statement
        cur.execute(
        f"SELECT * FROM Question where id = {id}")
        for id,position,title,text,image in cur :
            question = Question()
            question.init(id,position,title,text,image)
            return question.to_json(), 200

    except sqlite3.Error as e:
        return {"error" : {e.args[0]}}, 500

    return cur.fetchone(), 200