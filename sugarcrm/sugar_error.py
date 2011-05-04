#
#   sugar_error.py
#
#   Exceptions to be raised when various problems occur while running sugarcrm software
#

class GeneralException (Exception): pass
class InvalidConnection (GeneralException): pass
class InvalidRelationship (GeneralException): pass
class InvalidLogin (GeneralException): pass

## sugarerror
# potential class which would deal with errors returned by server,
#   currently not in use as the exceptions defined above + sugarcrm.testForError(obj)
#   are being used to handle all server errors and user input errors.
#
#   Modifying and using this class could create more custom user-defined handling
#       than testing for exceptions everywhere in the user's code. One possibility
#       being to give the sugarcrm connection a sugarerror object with custom methods 
#       defined by user for specific handling in all cases.
#
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

    def onError(self):
        pass

    def onFailedLogin(self):
        pass
    
    #called when an invalid command is sent to the server
    def onInvalidCommand(self):
        pass
        
    #called when attempt is made to access element of a sugarbean or module which doesn't exist
    def onAccessorError(self):
        pass

def is_sugar_error(data):
    try:
        return data["name"] != None and data["description"] != None
    except KeyError:
        return False

