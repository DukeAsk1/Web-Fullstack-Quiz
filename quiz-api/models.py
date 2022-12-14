# Exemple de création de classe en python
class Question():

    def init(self, id:int, position: int, title:str,text:str, image:str):
        self.id = id
        self.position = position
        self.title = title
        self.text = text
        self.image = image
    
    def to_json(self):
        list_question = dict()
        for key, value in self.__dict__.items():
            if value is not None:
                list_question[key] = value
        return list_question

    def from_json(self,list_question):
        for k,v in list_question.items() :
            setattr(self,k,v)