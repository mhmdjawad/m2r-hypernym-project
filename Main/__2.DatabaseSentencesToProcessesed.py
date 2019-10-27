#DatabaseSentencesToProcessesed
import mysql.connector
import spacy
nlp = spacy.load('en_core_web_sm')
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database=" hyp"
)
mycursor = mydb.cursor()
mycursor.execute("SELECT id,sentence FROM sentences where id not in (SELECT DISTINCT sentence_fk from processed_sentences)")
sentences = mycursor.fetchall()
isDep = 'false'
sql = "INSERT INTO processed_sentences(sentence_fk,term,lemma,pos,inx,head,dep) VALUES(%s,%s,%s,%s,%s,%s,%s)"
sqlSearch = "SELECT count(*) FROM processed_sentences where sentence_fk=%s"
for x in sentences:
	sentence_id = x[0]
	sentence = x[1]
	print(f'working for sentence {sentence_id}')
	mycursor.execute("SELECT count(*) FROM processed_sentences where sentence_fk=%s",(sentence_id,))
	if(mycursor.fetchone()[0] == 0):
		sent = sentence.strip()
		if isDep:
			parsedSent = nlp(sent) #dependency parsing
		else:
			parsedSent = nlp(sent, disable=['parser']) #shallow parsing
		index = 0
		for token in parsedSent:
			if isDep:
				w = (sentence_id, token.text , token.lemma_ , token.pos_ , index , token.head.text , token.dep_ )
			else:
				w = (sentence_id, token.text , token.lemma_ , token.pos_ , index , '' , '' )
			mycursor.execute(sql, w)
			index += 1
	else:
		print("sentence already processed")
	mydb.commit()
#end for
mydb.commit()