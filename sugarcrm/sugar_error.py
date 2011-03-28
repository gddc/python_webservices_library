
class GeneralException(Exception): pass
class InvalidConnection(Exception): pass
class InvalidLogin(Exception): pass

class sugarerror:
    def __init__(self, data = {}):
        self.name = ""
        self.msg = ""

        if is_sugar_error(data):
            self.name = data["name"]
            self.msg = data["description"]
        else:
            raise GeneralException


    def __str__(self):  
        return self.name+" : "+self.msg


def is_sugar_error(data):
    try:
        return data["name"] != None and data["description"] != None
    except KeyError:
        return False

