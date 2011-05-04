
import sugarcrm

S = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/akubera/service/v2/rest.php", "admin", "admin")

accounts = S.module('Accounts')
contacts = S.module('Contacts')

industry = raw_input("input industry: ")
X = accounts.find_by_industry(industry)

for x in X:
    print x.name,":"
#    y = S.get_relationships('Accounts', x.id, 'contacts', '', ['first_name', 'last_name', 'title'])
 #   y = sugarcrm.SugarEntryList(y)

    y = accounts.get_relationships(x, contacts, ['first_name', 'last_name', 'title']) 

    for e in y:
        print "   ",e.title,'-',e.first_name,e.last_name






















#r = accounts.find_by_industry('retail')[0]

#con = S.get_relationships('Accounts', r.id, 'contacts', related_fields = ['first_name', 'last_name', 'title'])
#con = S.get_relationships(module = 'Accounts', module_id = r.id, link_field_name = 'contacts', related_module = "contact_id", related_fields = ['first_name', 'last_name', 'title'])
#print r
#con = accounts.get_relationships(r, 'contacts', '', ['first_name', 'title'])


#print con
#print dir(con[0])
exit()



fields = accounts.get_fields()

for field in fields:
    print field

print "-"*30


for i in r:
    print i.name

print '-'*30
print S.get_user_id()




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

