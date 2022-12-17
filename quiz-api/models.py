class Answer() :
    def init(self,text:str,isCorrect:bool) :
        self.text = text
        self.isCorrect = isCorrect
        self.question_id = None

    def to_json(self):
        question_json = dict()
        for key, value in self.__dict__.items():
            if value is not None:
                question_json[key] = value
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
    
    def to_json(self):
        list_question = dict()
        for key, value in self.__dict__.items():
            if value is not None:
                list_question[key] = value
        return list_question

    def from_json(self,list_question):
        for k,v in list_question.items() :
            setattr(self,k,v)


