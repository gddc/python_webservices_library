import sys, os, re, unittest

 
def TestSuite():
	## return current directory
    path = os.getcwd()  
	## implement this directory into Python lib
    sys.path.append(path)
	## dir under current directory
    files = os.listdir(path)
	## file filter ".py" 
    test = re.compile("\.py$", re.IGNORECASE)
	## do a match search
    files = filter(test.search, files)
	
    filenameToModuleName = lambda case: os.path.splitext(case)[0]
    module_list = map(filenameToModuleName, files)
    modules = map(__import__, module_list)
    load = unittest.defaultTestLoader.loadTestsFromModule
    return unittest.TestSuite(map(load, modules))

if __name__ == "__main__":
    unittest.main(defaultTest="TestSuite")



