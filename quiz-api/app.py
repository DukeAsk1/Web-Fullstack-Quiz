from flask import Flask, request
from flask_cors import CORS
from jwt_utils import build_token,decode_token,secret
import sqlite3

app = Flask(__name__)
CORS(app)

file='tuto.db'

def connect_to_db(path):
    db_connection = sqlite3.connect(path)

    # set the sqlite connection in "manual transaction mode"
    # (by default, all execute calls are performed in their own transactions, not what we want)
    db_connection.isolation_level = None
    return db_connection

# Exemple de création de classe en python
class Question():
	def init(self, title: str):
		self.title = title

@app.route('/')
def hello_world():
	x = 'world !'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    if payload.get('password') == secret :
        return  {"token" : build_token()} , 200

    else:
        return "Unauthorized", 401

@app.route('/add_questions',methods=['POST'])
def question():
    cur = connect_to_db(file)
    #Récupérer le token envoyé en paramètre
    request.headers.get('Authorization')

    #récupèrer un l'objet json envoyé dans le body de la requète
    payload = request.get_json()

    # start transaction
    cur.execute("begin")

    # save the question to db
    cur.execute(
        f"insert into Question (Title) values"
        f"('{payload.title}')")

    # send the request
    cur.execute("commit")

    # in case of exception, rollback the transaction
    cur.execute('rollback')
    return payload



if __name__ == "__main__":
    app.run()