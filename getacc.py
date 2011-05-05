
import sugarcrm

S = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/akubera/service/v2/rest.php", "admin", "admin")

accounts = S.module('Accounts')
contacts = S.module('Contacts')

industry = raw_input("input industry: ")
X = accounts.find_by_industry(industry)

for x in X:
    print x.name,":"

    y = accounts.get_relationships(x, contacts, fields = ['first_name', 'last_name', 'title']) 

    for e in y:
        print "   ",e.title,'-',e.first_name,e.last_name
    print ""
