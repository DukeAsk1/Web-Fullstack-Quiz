from models import Question,Answer
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

def execute_statement(list_query) :
    cur = init_db_cursor()
    try:
    # Use the cursor to execute an INSERT list_query
        for query in list_query:
            cur.execute(query)
        # send the request
        return cur, 200
    except sqlite3.Error as e:
    # If an error occurred, print the error message
        cur.execute('rollback')
        return {"error" : e}, 500

def select_statement(list_query):
    response,status_code = execute_statement(list_query)
    if status_code == 200 :
        return response,status_code
    else :
        return response, status_code

def insert_statement(list_query) :
    response,status_code = execute_statement(list_query)
    if status_code == 200 :
        response.execute("commit")
        return {"id":response.lastrowid},status_code
    else :
        return response, status_code

def update_statement(list_query):
    response,status_code = execute_statement(list_query)
    if status_code == 200 :
        response.execute("commit")
        return {},204
    else :
        return response, status_code

def delete_statement(list_query):
    response,status_code = execute_statement(list_query)
    if status_code == 200 :
        response.execute("commit")
        return {},204
    else :
        return response, status_code

def post_question(question):
    input_question = Question()

    input_answers = [Answer() for answer in question["possibleAnswers"]]
    # answer =question["possibleAnswers"][0]

    for i,answer_json in enumerate(question["possibleAnswers"]) :
        input_answers[i].from_json(answer_json.copy())

    question["possibleAnswers"] = input_answers
    print(input_answers[1])

    input_question.from_json(question)



    #cur = init_db_cursor()

    # try:
    #     position_sql = cur.execute(f"select position FROM Question")
    #     print(position_sql)
    # except:
    #     pass
    # return insert_statement(
    #     f"insert into Question (position,title,text,image) values"
    #     f"({input_question.position!r},{input_question.title!r},"
    #     f"{input_question.text!r},{input_question.image!r})")


    insert_question,status_question = insert_statement([
        f"insert into Question (position,title,text,image) values"
        f"({input_question.position!r},{input_question.title!r},"
        f"{input_question.text!r},{input_question.image!r})"])

    if not status_question == 200 :
        return insert_question,status_question

    insert_answer_string = ""
    for answer in input_answers :
       insert_answer_string += f"({insert_question['id']!r},{answer.text!r},{answer.isCorrect!r}),"

    insert_answer,status_answer = insert_statement([
        f"insert into Answer (question_id,text,isCorrect) values"
        f"{insert_answer_string[:-1]}"])

    if not status_answer == 200 :
        return insert_answer,status_answer
    return insert_question,200

def select_question(list_query):
    response,status_code = select_statement(list_query)
    if status_code == 200 :
        for id,position,title,text,image in response :
            question = Question()
            question.init(id,position,title,text,image)
            return question.to_json(), 200
        return {"message":"Question non trouvée"},404
    else :
        return response, status_code

def get_question_by_id(id):
    return select_question([f"SELECT * FROM Question where id = {id}"])

def get_question_by_position(position):
    return select_question([f"SELECT * FROM Question where position = {position}"])

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
    return delete_statement(["DELETE FROM Question","DELETE FROM Answer"])

def delete_question_by_id(id):
    list_question,status = get_question_by_id(id)
    if status == 200 :
        return delete_statement([f"DELETE FROM Question where id = {id}","DELETE FROM Question where question_id= {id}"])
    return list_question,status

