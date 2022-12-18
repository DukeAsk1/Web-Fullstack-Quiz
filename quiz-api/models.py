class Answer() :
    def init(self,text:str,isCorrect:bool,answer_id) :
        self.text = text
        self.isCorrect = isCorrect
        self.question_id = None
        self.answer_id=None

    def to_json(self,answer_id=False):
        question_json = dict()
        for key, value in self.__dict__.items():
            if value is not None and not key=='id':
                question_json[key] = value
            if answer_id:
                question_json['id'] = self.answer_id
        return question_json

    def from_json(self,question_json):
        for k,v in question_json.items() :
            setattr(self,k,v)





# Exemple de création de classe en python
class Question():

    def init(self, id:int, position: int, title:str,text:str, image:str,possibleAnswers=list[Answer]):
        self.id = id
        self.position = position
        self.title = title
        self.text = text
        self.image = image
        self.possibleAnswers = possibleAnswers
    
    def to_json(self,answer_id=False):
        list_question = dict()
        for key, value in self.__dict__.items():
            if value is not None and not key=='id':
                list_question[key] = value
        list_question["possibleAnswers"] = [answer.to_json(answer_id) for answer in self.possibleAnswers]
        return list_question

    def from_json(self,list_question):
        for k,v in list_question.items() :
            setattr(self,k,v)


