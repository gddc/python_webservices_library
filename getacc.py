
import sugarcrm
#import sugarmodule

S = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/akubera/service/v2/rest.php", "admin", "admin")

accounts = S.module('Accounts')

fields = accounts.get_fields()

for field in fields:
    print f

print "-"*30

r = accounts.find_by_industry('retail')

for i in r:
    print i.name

exit()



industry = raw_input("Input Industry Name: ")

retail = accounts.get_entries_where("accounts.industry = '"+industry+"'")
list = ['d26b6c07-8f18-0f15-326e-4d41e0b4c29d','478e8eb3-4362-d662-df48-4d41e0c5035d','191f6b4a-0937-90d6-3d15-4d41e04decf4']
l = accounts.get_entries(list)

for i in l:
	print "\t",i.module,i.name,i.id
	
#print retail

#print type(a)

sugarcrm.Sugarmodule(S, 'Accounts')
for f in sugarcrm.Sugarmodule(S, 'Contacts').get_fields():
    print f

