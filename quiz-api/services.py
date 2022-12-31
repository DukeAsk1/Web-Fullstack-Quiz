from models import Question,Answer
import sqlite3
from flask import Flask, request
from jwt_utils import decode_token


def init_db_cursor():
    # create a connection
    db_connection = sqlite3.connect("./tuto.db", timeout=10)

    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None

    
    return db_connection


def post_question(question):
    db = init_db_cursor()

    cur = db.cursor()
    cur.execute("begin")
    
    input_question = Question()

    input_answers = [Answer() for answer in question["possibleAnswers"]]

    for i,answer_json in enumerate(question["possibleAnswers"]) :
        input_answers[i].from_json(answer_json.copy())

    question["possibleAnswers"] = input_answers

    input_question.from_json(question)

    # Check if position is already filled : multiple query 

    try:
        question_by_position,status_position = get_question_by_position(input_question.position)
    except:
        question_by_position,status_position = None

    if status_position == 200 :
        # increase position by 1 for position value >= to input question
        cur.execute(
            f"UPDATE Question SET position = position + 1 "
            f"WHERE position >= {input_question.position!r}")

    insert_question= cur.execute(
        f"INSERT into Question (position,title,text,image) values"
        f"({input_question.position!r},{input_question.title!r},"
        f"{input_question.text!r},{input_question.image!r})"
    )

    # if not status_question==200 :
    #     return insert_question,status_question
    question_id = insert_question.lastrowid
    answer_query = ""
    for answer in input_answers :
       answer_query += f"({insert_question.lastrowid!r},{answer.text!r},{answer.isCorrect!r}),"

    cur.execute(
        f"INSERT into Answer (question_id,text,isCorrect) values"
        f"{answer_query[:-1]}"
    )

    # if not status_answer==200:
    #     return insert_answer,status_answer
    cur.execute('commit')
    cur.close()
    db.close()
    return {"id":question_id},200

def select_question(query,answer_id=False):
    db = init_db_cursor()
    response= db.execute(query)
    # if status_code == 200 :
    for id,position,title,text,image,answers in response :
        answers_list = answers.split("-")
        input_answers = [Answer() for answer in answers_list]
        for i,answer_tuple in enumerate(answers_list) :
            answer_tuple = answer_tuple.split("/")
            print(answer_tuple)
            answers_dict = {"id":answer_tuple[0],"text":answer_tuple[1],"isCorrect":True if answer_tuple[2] == '1' else False}
            input_answers[i].from_json(answers_dict)
        question = Question()
        question.init(id,position,title,text,image,input_answers)
        return question.to_json(answer_id), 200
    return {"message":"Question non trouvée"},404
    # else :
    #     return response, status_code

def get_question_by_id(id,answer_id=False):
    return select_question(f"SELECT Question.*, group_concat(Answer.id||'/'||Answer.text||'/'||Answer.isCorrect,'-') as possibleAnswers "
                            f"FROM Answer LEFT JOIN Question on Question.id = Answer.question_id where Question.id = {id} GROUP BY Question.id",
                            answer_id)
# TO BE TESTED


def get_question_by_position(position,answer_id=False):
    return select_question(f"SELECT Question.*, group_concat(Answer.id||'/'||Answer.text||'/'||Answer.isCorrect,'-') as possibleAnswers "
                            f"FROM Answer LEFT JOIN Question on Question.id = Answer.question_id where position = {position} GROUP BY Question.id",
                            answer_id)


def update_question(updated_question,question_id):
    db = init_db_cursor()
    cur = db.cursor()
    cur.execute("begin")
    # Set current position to the last to work on the gap
    # Given one position, if position modified check difference between old and new position based on question id
    # If position lower, increase position of all after and equal questions by 1
    # Else, decrease by 1
    # Update new position in the filling gap
    # remove old answers data 
    # re insert new values
    question_id = int(question_id)
    input_question = Question()
    print("possible answers",updated_question['possibleAnswers'])
    input_answers = [Answer() for answer in updated_question["possibleAnswers"]]

    for i,answer_json in enumerate(updated_question["possibleAnswers"]) :
        input_answers[i].from_json(answer_json.copy())
    print("input answers",input_answers)
    updated_question["possibleAnswers"] = input_answers
    input_question.from_json(updated_question)
    question_json,status = get_question_by_id(question_id,True)
    if status == 200 :

        if int(input_question.position) < question_json["position"] :
            print('smaller')
            cur.execute(
            f"UPDATE Question SET position = -1 "
            f"WHERE id = {question_id!r}"
            )
            cur.execute(
                f"UPDATE Question SET position = position + 1 "
                f"WHERE position >= {input_question.position!r} and position < {question_json['position']!r}"
                )
        elif int(input_question.position) > question_json["position"]:
            cur.execute(
            f"UPDATE Question SET position = -1 "
            f"WHERE id = {question_json['id']!r}"
            )
            cur.execute(
                f"UPDATE Question SET position = position - 1 "
                f"WHERE position <= {input_question.position!r} and position > {question_json['position']!r}"
            )
    else:
        return {"message":"Question non trouvée"},404

    cur.execute(
        f"UPDATE Question SET position = {input_question.position!r},"
        f"title = {input_question.title!r},"
        f"text = {input_question.text!r},"
        f"image = {input_question.image!r} WHERE id = {question_json['id']!r}"
    )


    cur.execute(f"DELETE FROM Answer WHERE question_id = {question_json['id']!r}")
    answer_query = ""
    for answer in input_answers :
        answer_query += f"({question_json['id']!r},{answer.text!r},{answer.isCorrect!r}),"

    cur.execute(
        f"INSERT into Answer (question_id,text,isCorrect) values"
        f"{answer_query[:-1]}"
        )

    cur.execute('commit')
    cur.close()
    db.close()

    return question_json, 204

def delete_all_questions():
    db = init_db_cursor()
    cur = db.cursor()
    cur.execute("begin")
    delete_question= cur.execute(f"DELETE FROM Question")

    cur.execute(f"DELETE FROM Answer")

    cur.execute("commit")
    cur.close()
    db.close()
    
    return delete_question,204

def delete_question_by_id(id):
    db = init_db_cursor()
    cur = db.cursor()
    cur.execute("begin")
    question,status = get_question_by_id(id)
    if status == 200 :
        cur.execute(f"DELETE FROM Question where id = {id}")
        cur.execute(f"DELETE FROM Answer where question_id = {id}")
        cur.execute(
            f"UPDATE Question SET position = position - 1 "
                f"WHERE position >= {question['position']!r}"
        )
        cur.execute('commit')
        cur.close()
        db.close()
    else:
        return {"message":"Question non trouvée"},404
    return question,204

def get_number_of_question():
    db = init_db_cursor()
    cur = db.cursor()
    cur.execute("begin")
    count_position = cur.execute(f"SELECT COUNT(DISTINCT position) as count FROM Question")

    nb = count_position.fetchone()[0]

    return nb
