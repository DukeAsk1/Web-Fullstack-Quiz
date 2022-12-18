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
    print(list_query)
    cur = init_db_cursor()
    try:
    # Use the cursor to execute an INSERT list_query
        for query in list_query:
            cur.execute(query)
        # send the request
        return cur, 200
    except sqlite3.Error as e:
        print('EXE ERROR')
    # If an error occurred, print the error message
        cur.execute('rollback')
        return {"error" : e}, 500

def select_statement(list_query):
    print('in select statement')
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


    insert_question,status_question = insert_statement([
        f"insert into Question (position,title,text,image) values"
        f"({input_question.position!r},{input_question.title!r},"
        f"{input_question.text!r},{input_question.image!r})"])

    if not status_question == 200 :
        return insert_question,status_question

    answer_query = ""
    for answer in input_answers :
       answer_query += f"({insert_question['id']!r},{answer.text!r},{answer.isCorrect!r}),"

    insert_answer,status_answer = insert_statement([
        f"insert into Answer (question_id,text,isCorrect) values"
        f"{answer_query[:-1]}"])

    if not status_answer == 200 :
        return insert_answer,status_answer
    return insert_question,200

def select_question(list_query,answer_id=False):
    print('in select question')
    response,status_code = select_statement(list_query)
    if status_code == 200 :
        print('in status 200')
        for id,position,title,text,image,answers in response :
            answers_list = answers.split("-")
            print('answers_list',answers_list)
            input_answers = [Answer() for answer in answers_list]

            for i,answer_tuple in enumerate(answers_list) :
                answer_tuple = answer_tuple.split("/")
                print('answer_tuple',answer_tuple)
                answers_dict = {"answer_id":answer_tuple[0],"text":answer_tuple[1],"isCorrect":True if answer_tuple[2] == '1' else False}
                input_answers[i].from_json(answers_dict)

            print(input_answers)

            question = Question()
            question.init(id,position,title,text,image,input_answers)
            return question.to_json(answer_id), 200
        return {"message":"Question non trouvée"},404
    else :
        return response, status_code

def get_question_by_id(id,answer_id=False):
    return select_question([f"SELECT Question.*, group_concat(Answer.answer_id||'/'||Answer.text||'/'||Answer.isCorrect,'-') as possibleAnswers "
                            f"FROM Question LEFT JOIN Answer on Question.id = Answer.question_id where Question.id = {id} GROUP BY Question.id"],
                            answer_id)

def get_question_by_position(position,answer_id=False):
    return select_question([f"SELECT Question.*, group_concat(Answer.answer_id||'/'||Answer.text||'/'||Answer.isCorrect,'-') as possibleAnswers "
                            f"FROM Question LEFT JOIN Answer on Question.id = Answer.question_id where Question.position = {position} GROUP BY Question.id"],
                            answer_id)

def update_question(updated_question,question_id):
    # Set current position to the last to work on the gap
    # Given one position, if position modified check difference between old and new position based on question id
    # If position lower, increase position of all after and equal questions by 1
    # Else, decrease by 1
    # Update new position in the filling gap
    # remove old answers data 
    # re insert new values
    input_question = Question()
    # input_question.from_json(list_question)

    #updated_question,status = get_question_by_id(question_id)
    input_answers = [Answer() for answer in updated_question["possibleAnswers"]]

    for i,answer_json in enumerate(updated_question["possibleAnswers"]) :
        input_answers[i].from_json(answer_json.copy())

    updated_question["possibleAnswers"] = input_answers
    print("updated question",updated_question)
    input_question.from_json(updated_question)
    print("input json question",input_question)
    try:
        question_json,status = get_question_by_id(question_id,True)
    except:
        print('get id wrong')

    if status == 200 :
        list_query = []
        if int(input_question.position) != question_json["position"] :
            list_query.append(
                f"UPDATE Question SET position = -1 "
                f"WHERE id = {question_id!r}"
            )

            if int(input_question.position) < question_json["position"] :
                list_query.append(
                    f"UPDATE Question SET position = position + 1 "
                    f"WHERE position >= {input_question.position!r} and position < {question_json['position']!r}"
                )
            else:
                list_query.append(
                    f"UPDATE Question SET position = position - 1 "
                    f"WHERE position <= {input_question.position!r} and position > {question_json['position']!r}"
                ) 

        list_query.append(
            f"UPDATE Question SET position = {input_question.position!r},"
            f"title = {input_question.title!r},"
            f"text = {input_question.text!r},"
            f"image = {input_question.image!r} WHERE id = {question_id!r}"
        )

        list_query.append(f"DELETE FROM Answer WHERE question_id = {question_id!r}")

        answer_query = ""
        for answer in input_answers :
            answer_query += f"({question_id!r},{answer.text!r},{answer.isCorrect!r}),"

        list_query.append(
            f"insert into Answer (question_id,text,isCorrect) values"
            f"{answer_query[:-1]}")

        return update_statement(list_query)
            
    return updated_question,status

def delete_all_questions():
    return delete_statement(["DELETE FROM Question","DELETE FROM Answer"])

def delete_question_by_id(id):
    list_question,status = get_question_by_id(id)
    if status == 200 :
        return delete_statement([f"DELETE FROM Question where id = {id}",f"DELETE FROM Question where question_id = {id}"])
    return list_question,status

