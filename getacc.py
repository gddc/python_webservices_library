
import sugarcrm
#import sugarmodule

S = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/akubera/service/v2/rest.php", "admin", "admin")

a = S.get_module_fields('Accounts')

accounts = sugarcrm.Sugarmodule(S, 'Accounts')

industry = raw_input("Input Industry Name: ")
retail = accounts.get_entries_where("accounts.industry = '"+industry+"'")

for i in retail:
	print "\t"+i.name
	
#print retail

#print type(a)

