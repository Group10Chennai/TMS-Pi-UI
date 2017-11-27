def __init__(self, gui):  
        self.__gui = gui  

def run(rfid):
	print "inside Search ", rfid
	if rfid != None:
		print "inside Search ", rfid

	return "Im python reply "+ rfid

def fun():
	print "inside Search 1 "

if __name__ == "__main__":
	run('123456')

	fun()
