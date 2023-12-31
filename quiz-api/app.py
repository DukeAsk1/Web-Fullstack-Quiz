from flask import Flask, request
from flask_cors import CORS
from jwt_utils import build_token,decode_token,secret
import services
import jwt_utils
# from questions_data import post_question_from_JSON
import os
import json

app = Flask(__name__)
CORS(app)

# @app.before_first_request
# def post_question_from_JSON(directory):
#     print('in before app')
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.json'):
#                 file_path = os.path.join(root, file)
#                 with open(file_path) as f:
#                     data = json.load(f)
#                     services.post_question(data)



@app.route('/')
def hello_world():
	x = 'world !'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def get_quiz_info():
    return services.get_quiz_info()
	#return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    if payload.get('password') == secret :
        return  {"token" : build_token()} , 200

    else:
        return "Unauthorized", 401

@app.route('/questions',methods=['POST'])
def post_question():
    # Récupérer le token envoyé en paramètre
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

@app.route('/questions/<question_id>', methods=['GET'])
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
    # Récupérer le token envoyé en paramètre
    auth_token = request.headers.get('Authorization')
    try :
        decode_token(auth_token[7:])
    except TypeError:
        return {"message" : "Not authenticated"} ,401
    except Exception as e:
        return e.__dict__ ,401
    return services.delete_all_questions()

@app.route('/questions/<question_id>', methods=['DELETE'])
def delete_question_by_id(question_id):
    # Récupérer le token envoyé en paramètre
    auth_token = request.headers.get('Authorization')
    print("id tot be deleted",question_id)
    print("ATUH",auth_token)
    try :
        decode_token(auth_token[7:])
    except TypeError:
        return {"message" : "Not authenticated"} ,401
    except Exception as e:
        return e.__dict__ ,401
    print(question_id)
    return services.delete_question_by_id(question_id)

@app.route('/questions/<question_id>', methods=['PUT'])
def update_question(question_id):
    # Récupérer le token envoyé en paramètre
    auth_token = request.headers.get('Authorization')
    try :
        decode_token(auth_token[7:])
    except TypeError:
        return {"message" : "Not authenticated"} ,401
    except Exception as e:
        return e.__dict__ ,401
    list_question = request.get_json()
    print(list_question)
    return services.update_question(list_question,question_id)

@app.route('/nb_question',methods=['GET'])
def get_number_of_question():
    return {"nb_question" : services.get_number_of_question()},200

@app.route('/participations',methods=['POST'])
def post_participation():
    player_answers = request.get_json()
    return services.post_participation(player_answers)

@app.route('/participations/all', methods=['DELETE'])
def deleteAllParticipations():
   #Récupérer le token envoyé en paramètre
    auth_token = request.headers.get('Authorization')
    try :
        jwt_utils.decode_token(auth_token[7:])
    except TypeError:
        return {"message" : "Veuillez vous authentifier"} ,401
    except Exception as e:
        return e.__dict__ ,401

    return services.delete_all_participations()

@app.route('/rebuild-db', methods=['POST'])
def rebuild_db():
    return services.rebuild_db()

if __name__ == "__main__":
    app.run()
