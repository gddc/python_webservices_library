
import sugarcrm, urllib

print "hello"

#x = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php")
S = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/akubera/service/v2/rest.php", "admin", "admin")

if S.connected == 1:
    print "Connection Successful!"

if S.id != 0:
    print "Login Successful!"

"""
entry = S.set_entry('Accounts',[{'name':'name','value':'New Account'},{'name':'description', 'value':'NEW ACCOUNT FROM PYTHON!'}])

print entry['id']


exit()
"""

retail = S.get_entry_list('Accounts',"accounts.industry = 'retail'", "", "", ['id','name','sic_code'],[])

print "RETAIL:"
x = retail['entry_list'][0]
print x
print ""
for i,j in x['name_value_list']:
    print i


modules = S.get_available_modules()

print modules



exit()

s = S.get_user_id()
print "ID: "+s
#f = S.get_module_fields("Contacts")
#print f

#z = S.set_relationship('Accounts','blahblahblah','wdfjkslkdjf')

try:
 t = S.get_entries_count("Contacts")
 print "TEAM: "+str(t)
except sugarcrm.GeneralException:
 pass

#data = {'session':x.id, 'module_name':'Accounts', 'query':"accounts.industry = 'Retail'", \
#   'order_by':'', 'offset':'','select_fields':['id','name','sic_code'],'link_name_to_fields_array':[]}
#args = {'method': 'get_entry_list', 'input_type': 'JSON', 'response_type' : 'JSON', 'rest_data' : data}

#args = urllib.urlencode(args)
#x.sendRequest(args)
#m = S.get_module_fields("Accounts")

#print m
