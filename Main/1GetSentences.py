import mysql.connector
######################################################################

#𝑖𝑓 𝒘𝒐𝒓𝒅 𝑖𝑠𝐶𝑜𝑛𝑡𝑒𝑥𝑡(𝑻𝒆𝒓𝒎)  "and  distance(" 𝑻𝒆𝒓𝒎", " 𝑖𝑓𝒘𝒐𝒓𝒅") < WINDOW"


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database=" hyp"
)
mycursor = mydb.cursor(buffered=True)
mycursor2 = mydb.cursor(buffered=True)
def getSentences(count):
	_set = set()
	mycursor.execute(f"SELECT * FROM `sentences` ORDER BY RAND() limit {count}   ")
	rows = mycursor.fetchall()
	for r in rows:
		_set.add(r)
	return _set
def __main__():
	print("Program started")
	count = input("enter number of sentences wanted")
	sentences = getSentences(count)
	print("------------------------------------------------------")
	for s in sentences :
		print(s[1])
	print("------------------------------------------------------")
__main__()