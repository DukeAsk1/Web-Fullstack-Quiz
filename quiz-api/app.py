from flask import Flask, request
from flask_cors import CORS
from jwt_utils import build_token,decode_token,secret
import services


app = Flask(__name__)
CORS(app)

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

@app.route('/questions',methods=['POST'])
def postQuestions():
   #Récupérer le token envoyé en paramètre
    auth_token = request.headers.get('Authorization')
    try :
        decode_token(auth_token[7:])
    except TypeError:
        return {"message" : "Not authenticated"} ,401
    except Exception as e:
        return e.__dict__ ,401

    #récupèrer un l'objet json envoyé dans le body de la requète
    question_json = request.get_json()
    return services.post_question(question_json)

@app.route('/questions/<question_id>',methods=['GET'])
def get_question_by_id(question_id):
    return services.get_question_by_id(question_id)



if __name__ == "__main__":
    app.run()