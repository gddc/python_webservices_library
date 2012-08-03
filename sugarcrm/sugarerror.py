#
#   sugarerror.py
#
#   Exceptions to be raised when various problems occur while running sugarcrm software
#

class SugarError(Exception):
    def __init__(self, data):
        self.name = data['name']
        self.description = data['description']
        self.number = data['number']

    def is_invalid_session(self):
        return self.number == 11

    def is_invalid_login(self):
        return self.number == 10


class SugarUnhandledException(Exception):
    pass


def is_error(data):
    try:
        return data["name"] != None and data["description"] != None
    except KeyError:
        return False

