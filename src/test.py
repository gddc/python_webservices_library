
import sugarcrm

print "hello"

#x = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php")
x = sugarcrm.Sugarcrm("http://ruttanvm.cs.kent.edu:4080/service/v2/rest.php", "class", "123")

if x.connected == 1:
    print "Connection Successful!"

if x.id != 0:
    print "Login Successful!"
