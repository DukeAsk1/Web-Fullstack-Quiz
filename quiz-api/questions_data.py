import os
import json
from models import Question,Answer
from services import post_question

def post_question_from_JSON(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path) as f:
                    data = json.load(f)
                    post_question(data)

