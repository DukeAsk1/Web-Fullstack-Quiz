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
    services.check_token()
    #récupèrer un l'objet json envoyé dans le body de la requète
    question_json = request.get_json()
    return services.post_question(question_json)

@app.route('/questions/{question_id}', methods=['GET'])
def get_question_by_id(question_id):
    return services.get_question_by_id(question_id)

@app.route('/questions', methods=['GET'])
def get_question_by_position():
    position = request.args.get("position")
    if position :
        return services.get_question_by_position(position)
    return {"message" : "Position non spécifiée"}, 404

@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions():
    services.check_token()
    return services.delete_all_questions()

@app.route('/questions/{question_id}', methods=['DELETE'])
def delete_question_by_id(question_id):
    services.check_token()
    return services.delete_question_by_id(question_id)

@app.route('/questions/{question_id}', methods=['PUT'])
def update_question(question_id):
    services.check_token()
    list_question = request.get_json()
    return services.update_question(list_question,question_id)

if __name__ == "__main__":
    app.run()