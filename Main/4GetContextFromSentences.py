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

ID = 0
SENT = 1
WORD = 2
LEMA = 3
POS = 4
INX = 5
DEPH = 6
DEPV = 5
WINDOW_LIMIT = 5
####from 1
def getSentences(count):
	_set = set()
	mycursor.execute(f"SELECT * FROM `sentences` order by id asc limit {count} ")
	rows = mycursor.fetchall()
	for r in rows:
		_set.add(r)
	return _set
#### end from 1
#### from 2
def getProcessedSentence(_inp):
	_set = []
	mycursor.execute(f"SELECT * FROM `processed_sentences` WHERE `sentence_fk` = {_inp} order by id asc")
	rows = mycursor.fetchall()
	for r in rows:
		_set.append(r)
	return _set
#### end from 2

#end dif
def isTerm(Pw):
	pos = Pw[POS]
	return 'NOUN'==pos
#end isTerm
def getContexts(Term,Pws):
	_context = []
	for Pw in Pws :
		if Term != Pw:
			if Pw[POS] not in ["NOUN","VERB","ADJ"]:
				continue
			dist = abs(Pw[INX] - Term[INX])
			if(dist < WINDOW_LIMIT):
				_context.append(Pw[LEMA])
			#print(f"dist between {Term[LEMA]} and {Pw[LEMA]} is {str(dist)}" )
	return _context
#end getContexts
def getContexts_pos(Term,Pws):
	_context = []
	for Pw in Pws :
		if Term != Pw:
			if Pw[POS] not in ["NOUN","VERB","ADJ"]:
				continue
			dist = abs(Pw[INX] - Term[INX])
			if(dist < WINDOW_LIMIT):
				_context.append(Pw[LEMA]+"_"+Pw[POS])
			#print(f"dist between {Term[LEMA]} and {Pw[LEMA]} is {str(dist)}" )
	return _context
#end getContexts_pos
def getContexts_dep(Term,Pws):
	_context = []
	for Pw in Pws :
		if Term != Pw:
			if Pw[POS] not in ["NOUN","VERB","ADJ"]:
				continue
			dist = abs(Pw[INX] - Term[INX])
			if(dist < WINDOW_LIMIT):
				_context.append(Pw[LEMA])
			#print(f"dist between {Term[LEMA]} and {Pw[LEMA]} is {str(dist)}" )
	_context.append(Pw[DEPH]+"_dep")
	return _context
#end getContexts_dep
def getContexts_position(Term,Pws):
	_context = []
	for Pw in Pws :
		if Term != Pw:
			if Pw[POS] not in ["NOUN","VERB","ADJ","PROPN"]:
				continue
			distr = Pw[INX] - Term[INX]
			dist = abs(distr)
			if(dist < WINDOW_LIMIT):
				if(distr < 0):
					_context.append(Pw[LEMA]+"_before")
				else:
					_context.append(Pw[LEMA]+"_after")
			#print(f"dist between {Term[LEMA]} and {Pw[LEMA]} is {str(dist)}" )
	return _context
#end getContexts_dep

def dbMatrix(Terms,TermsContexts,OutTable):
	print(f"saving to {OutTable}")
	sql = f"CREATE OR REPLACE TABLE  `{OutTable}` (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY)ENGINE=INNODB;"
	mycursor.execute(sql)
	sql = f"ALTER TABLE `{OutTable}` ADD  term VARCHAR(40);"
	mycursor.execute(sql)
	sql = f"ALTER TABLE `{OutTable}` ADD  context VARCHAR(40);"
	mycursor.execute(sql)
	mydb.commit()
	sql = f"INSERT INTO `{OutTable}`(term,context) VALUES(%s,%s);"
	#mycursor.execute(sql)
	for i in range(0,len(Terms)):
		for C in TermsContexts[i]:
			mycursor.execute(sql, (Terms[i],C,))
			#print(f'{Terms[i]} \t {C} ')
		#print(f'{i} \t\t\t {Terms[i]} \t')
		mydb.commit()
	print('DONE')
def prepMatrix(Terms,TermsContexts,OutFileName):
	Matrix = dict()
	FilteredTerms = set()
	FilteredContexts = set()
	
	for T in Terms:
		FilteredTerms.add(T)
	
	for TC in TermsContexts:
		for C in TC:
			FilteredContexts.add(C)
	
	for T in FilteredTerms:
		Matrix[T] = dict()
		for C in FilteredContexts:
			Matrix[T][C] = 0;
	#print(Matrix)
	
	ofile = open(OutFileName,"w")
	
	for i in range(0,len(Terms)):
		for C in TermsContexts[i]:
			Matrix[Terms[i]][C] += 1
	#print("Features | ",end='')
	for Cx in FilteredContexts:
		ofile.write(f'{Cx.encode("utf-8")} , ')
		#print(Cx+" | ",end='')
	#print('')
	ofile.write('\n')
	
	for T,Tc in Matrix.items():
		#print(T+" | ",end='')
		ofile.write(f'{T.encode("utf-8")} , ')
		for Cx,c in Tc.items():
			#print(str(c)+" | ",end='')
			ofile.write(str(c)+" , ")
		ofile.write("\n")
		#print('')
	ofile.close()
def __main__():
	print("Program started")
	import datetime
	now = datetime.datetime.now()
	print (now.strftime("%Y-%m-%d %H:%M:%S"))
	CountSentences = 50000
	ALLPWs = []
	for i in range (0,CountSentences):
		Pws = getProcessedSentence(i)
		ALLPWs.append(Pws)
	Terms = []
	TermsContexts = []
	#-------------------------------
	Terms = []
	TermsContexts = []
	for i in range (0,CountSentences):
		Pws = ALLPWs[i]
		for Pw in Pws :
			if(isTerm(Pw)):
				ctx = getContexts(Pw,Pws)
				Terms.append(Pw[LEMA])
				TermsContexts.append(ctx)
	print("------------------------------------------------------")
	now = datetime.datetime.now()
	time = now.strftime("%Y_%m_%d_%H_%M_%S_default_") +str(CountSentences)
	print (time)
	dbMatrix(Terms,TermsContexts,time)
	#-------------------------------
	Terms = []
	TermsContexts = []
	for i in range (0,CountSentences):
		Pws = ALLPWs[i]
		for Pw in Pws :
			if(isTerm(Pw)):
				#print("get context of " + Pw[LEMA])
				ctx = getContexts_pos(Pw,Pws)
				Terms.append(Pw[LEMA])
				TermsContexts.append(ctx)
	print("------------------------------------------------------")
	time = now.strftime("%Y_%m_%d_%H_%M_%S_pos_") +str(CountSentences)
	dbMatrix(Terms,TermsContexts,time)
	#-------------------------------
	Terms = []
	TermsContexts = []
	for i in range (0,CountSentences):
		Pws = ALLPWs[i]
		for Pw in Pws :
			if(isTerm(Pw)):
				#print("get context of " + Pw[LEMA])
				ctx = getContexts_dep(Pw,Pws)
				Terms.append(Pw[LEMA])
				TermsContexts.append(ctx)
	print("------------------------------------------------------")
	time = now.strftime("%Y_%m_%d_%H_%M_%S_dep_")+str(CountSentences)
	dbMatrix(Terms,TermsContexts,time)
	#-------------------------------
	Terms = []
	TermsContexts = []
	for i in range (0,CountSentences):
		Pws = ALLPWs[i]
		for Pw in Pws :
			if(isTerm(Pw)):
				#print("get context of " + Pw[LEMA])
				ctx = getContexts_position(Pw,Pws)
				Terms.append(Pw[LEMA])
				TermsContexts.append(ctx)
	print("------------------------------------------------------")
	time = now.strftime("%Y_%m_%d_%H_%M_%S_position_")+str(CountSentences)
	dbMatrix(Terms,TermsContexts,time)
	print("------------------------------------------------------")
	now = datetime.datetime.now()
	print (now.strftime("%Y-%m-%d %H:%M:%S"))
	
__main__()