
import sugarcrm

S = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/akubera/service/v2/rest.php", "admin", "admin")

if S.connected == 1:
    print "Connection Successful!"

m = S.module('Accounts')

new_name = raw_input("new account name: ")
new_indu = raw_input("new industry name: ")
x = m.newBean({'name': new_name, 'industry': new_indu})

ind_name = raw_input("search for industry: ")
ind_list = m.find_by_industry(ind_name)

for i in ind_list:
    print i.name
