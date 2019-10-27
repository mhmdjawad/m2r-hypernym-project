##Read from corpus to database
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database=" hyp"
)
mycursor = mydb.cursor()
sql = "INSERT INTO sentences(sentence) VALUES(%s)"
SearchSql = "SELECT count(*) FROM sentences where sentence=%s"
min_line = 665275

import datetime
now = datetime.datetime.now()
print (now.strftime("%Y-%m-%d %H:%M:%S"))
	
	
with open('Corpus512MB.txt', "rb")as docText:
	lineIndex = 0
	for line in docText:
		lineIndex += 1
		if(lineIndex < min_line):
			#print(f'line already done {lineIndex}')
			continue
		line = line.strip().decode("utf-8", "ignore") 
		line = line.replace("\n", "")
		line = line.replace("\r", "")
		line = line.replace(" .", "")
		line = line.strip()
		
		if(lineIndex % 10000 == 0):
			print(f'at line {lineIndex}')
		mycursor.execute(sql, (line,))
		mydb.commit()
		'''
		mycursor.execute(SearchSql,(line,))
		if(mycursor.fetchone()[0] == 0):
			mycursor.execute(sql, (line,))
			mydb.commit()
		else:
			print(f"line exist in database {lineIndex}")
		#print(line)
		'''
	#end for
#end with