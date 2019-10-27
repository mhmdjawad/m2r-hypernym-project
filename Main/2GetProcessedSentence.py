import mysql.connector
######################################################################
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database=" hyp"
)
mycursor = mydb.cursor(buffered=True)
mycursor2 = mydb.cursor(buffered=True)
def getProcessedSentence(_inp):
	_set = []
	mycursor.execute(f"SELECT * FROM `processed_sentences` WHERE `sentence_fk` = {_inp} order by id asc")
	rows = mycursor.fetchall()
	for r in rows:
		_set.append(r)
	return _set
def __main__():
	print("Program started")
	_inp = input("enter sentence id wanted: ")
	Pws = getProcessedSentence(_inp)
	print("------------------------------------------------------")
	for Pw in Pws :
		for p in Pw:
			print(str(p)+" | ", end='')
		print('')
	print("------------------------------------------------------")
__main__()