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
def prepMatrix(Terms,TermsContexts):

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
	
	
	for i in range(0,len(Terms)):
		for C in TermsContexts[i]:
			Matrix[Terms[i]][C] += 1
	
	print("Features | ",end='')
	for Cx in FilteredContexts:
		print(Cx+" | ",end='')
	print('')

	for T,Tc in Matrix.items():
		print(T+" | ",end='')
		for Cx,c in Tc.items():
			print(str(c)+" | ",end='')
		print('')
		



			
def __main__():
	print("Program started")
	_inp = 1 #input("enter sentence id wanted: ")
	Pws = getProcessedSentence(_inp)
	
	Terms = []
	TermsContexts = []
	print("------------------------------------------------------")
	for Pw in Pws :
		print(Pw)
		if(isTerm(Pw)):
			#print("get context of " + Pw[LEMA])
			ctx = getContexts(Pw,Pws)
			Terms.append(Pw[LEMA])
			TermsContexts.append(ctx)
			#print(f"for term {Pw[LEMA]} contexes are {ctx}")
		#for p in Pw:
		#	print(str(p)+" | ", end='')
		#print('')
	prepMatrix(Terms,TermsContexts)
	print("------------------------------------------------------")
__main__()