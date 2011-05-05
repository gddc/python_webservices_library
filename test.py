
import sugarcrm

S = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/akubera/service/v2/rest.php", "admin", "admin")

if S.connected == 1:
    print "Connection Successful!"

m = S.module('Accounts')

ind_name = raw_input("search for industry: ")

ind_list = m.find_by_industry(ind_name)

for i in ind_list:
    print i.name
