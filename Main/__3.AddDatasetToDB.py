import csv
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database=" hyp"
)
mycursor = mydb.cursor()

#datasetTerms 
sql = "datasetTerms"
sql = "INSERT INTO datasetTerms(name) VALUES(%s)"
s = set()
with open("___DataSet.csv") as csv_file:
 csv_reader = csv.reader(csv_file, delimiter=',')
 for row in csv_reader:
  NP1 = row[0].strip()
  NP2 = row[1].strip()
  RES = row[2]
  s.add(NP1)
  s.add(NP2)
print(s)
for t in s:
 mycursor.execute(sql, (t,))
 mydb.commit()