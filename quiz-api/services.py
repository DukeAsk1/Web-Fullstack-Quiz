from models import Question
import sqlite3
from flask import Flask, request
from jwt_utils import decode_token

def init_db_cursor():
    # create a connection
    db_connection = sqlite3.connect("./tuto.db")

    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None

    cur = db_connection.cursor()
    # start transaction
    cur.execute("begin")

    return cur

def check_token():
    # Récupérer le token envoyé en paramètre
    auth_token = request.headers.get('Authorization')
    try :
        decode_token(auth_token[7:])
    except TypeError:
        return {"message" : "Not authenticated"} ,401
    except Exception as e:
        return e.__dict__ ,401

def execute_statement(statement) :
    cur = init_db_cursor()
    try:
    # Use the cursor to execute an INSERT statement
        cur.execute(statement)
        # send the request
        return cur, 200
    except sqlite3.Error as e:
    # If an error occurred, print the error message
        cur.execute('rollback')
        return {"error" : {e.args[0]}}, 500

def select_statement(statement):
    response,status_code = execute_statement(statement)
    if status_code == 200 :
        return response,status_code
    else :
        return response, status_code

def insert_statement(statement) :
    response,status_code = execute_statement(statement)
    if status_code == 200 :
        response.execute("commit")
        return {"id":response.lastrowid},status_code
    else :
        return response, status_code

def update_statement(statement):
    response,status_code = execute_statement(statement)
    if status_code == 200 :
        response.execute("commit")
        return {},204
    else :
        return response, status_code

def delete_statement(statement):
    response,status_code = execute_statement(statement)
    if status_code == 200 :
        response.execute("commit")
        return {},204
    else :
        return response, status_code

def post_question(question):
    input_question = Question()
    input_question.from_json(question)

    cur = init_db_cursor()

    # try:
    #     position_sql = cur.execute(f"select position FROM Question")
    #     print(position_sql)
    # except:
    #     pass
    return insert_statement(
        f"insert into Question (position,title,text,image) values"
        f"({input_question.position!r},{input_question.title!r},"
        f"{input_question.text!r},{input_question.image!r})")

def select_question(statement):
    response,status_code = select_statement(statement)
    if status_code == 200 :
        for id,position,title,text,image in response :
            question = Question()
            question.init(id,position,title,text,image)
            return question.to_json(), 200
        return {"message":"Question non trouvée"},404
    else :
        return response, status_code

def get_question_by_id(id):
    return select_question(f"SELECT * FROM Question where id = {id}")

def get_question_by_position(position):
    return select_question(f"SELECT * FROM Question where position = {position}")

def update_question(list_question,question_id):
    input_question = Question()
    input_question.from_json(list_question)

    list_question,status = get_question_by_id(question_id)

    if status == 200 :
        return update_statement(
            f"UPDATE Question SET position = {input_question.position!r},"
            f"title = {input_question.title!r},"
            f"text = {input_question.text!r},"
            f"image = {input_question.image!r} WHERE id = {input_question.id!r}")
            
    return list_question,status

def delete_all_questions():
    return delete_statement("DELETE FROM Question")

def delete_question_by_id(id):
    list_question,status = get_question_by_id(id)
    if status == 200 :
        return delete_statement(f"DELETE FROM Question where id = {id}")
    return list_question,status