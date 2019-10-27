import datetime
print('Start' + datetime.datetime.now().strftime("%Y-%m-%d %H %M %S"))
import sys
#print(len(sys.argv))
#print(sys.argv)
if( len(sys.argv) == 1):
	...
	#print("select option main for main, ml for machine learn")
	#sys.exit()
######################################################################
import mysql.connector
import csv
import numpy as np
######################################################################
import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import average_precision_score
######################################################################
print('Import Done' + datetime.datetime.now().strftime("%Y-%m-%d %H %M %S"))
def init():
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="",
	  database=" hyp"
	)
	mycursor = mydb.cursor(buffered=True)
	mycursor2 = mydb.cursor(buffered=True)
	SentencesCount = 50000
	tablename = "2019_10_26_16_49_56_default_"+str(SentencesCount)
	sql = "select term,context,count(*) from "+tablename+" where term in (select name from datasetterms) group by term,context;"
	sql_term = "select distinct term from "+tablename+" where term in (select name from datasetterms);"
	sql_context = "select distinct context from "+tablename+" where term in (select name from datasetterms);"
	now = datetime.datetime.now()
	nowstr = now.strftime("%Y-%m-%d %H %M %S")
def __MachineLearning__(Name):
	
	
	
	
	
	dataset = pd.read_csv(f'{Name}',sep=',', engine='python')
	
	#dataset = 
	
	
	
	
	print('File Reading Complete ' + datetime.datetime.now().strftime("%Y-%m-%d %H %M %S"))
	print(f'For \t {Name}')
	dataset['Result'] = pd.cut(dataset['Result'],bins=[-1,0,1],labels=['false','true'])
	label_quality = LabelEncoder()
	dataset['Result'] = label_quality.fit_transform(dataset['Result'])
	X = dataset.drop('Result',axis=1)
	y = dataset['Result']
	X_train, X_test , y_train, y_test = train_test_split(X,y,test_size = 0.2,random_state=42)
	sc = StandardScaler()
	X_train = sc.fit_transform(X_train)
	X_test = sc.transform(X_test)
	print(f'length is {len(dataset)-1}')
	print(f'-----------------------------------------------------------------')
	############################################################################################RandomForestClassifier
	print('RandomForestClassifier')
	c = RandomForestClassifier(n_estimators=200)
	c.fit(X_train,y_train)
	pred = c.predict(X_test)
	print(classification_report(y_test,pred))
	RFC_ = f'RFC \t {accuracy_score(y_test, pred)} \t {average_precision_score(y_test, pred)}'
	print('#############################################################')
	print('SVC')
	c = svm.SVC(gamma='auto')
	c.fit(X_train,y_train)
	pred = c.predict(X_test)
	print(classification_report(y_test,pred))
	SVC_ = f'SVC \t {accuracy_score(y_test, pred)} \t {average_precision_score(y_test, pred)}'
	print('#############################################################')
	print('Neural Network')
	c = MLPClassifier(hidden_layer_sizes = (11,11,11),max_iter=500)
	c.fit(X_train,y_train)
	pred = c.predict(X_test)
	print(classification_report(y_test,pred))
	NN__ = f'N-N \t {accuracy_score(y_test, pred)} \t {average_precision_score(y_test, pred)}'
	print('#############################################################')
	############################################################################################
	print(f'ALGO \t accuracy_score \t average_precision_score')
	print(RFC_)
	print(SVC_)
	print(NN__)
########################################################################################################################
def __main__():
	print('Program Started' + datetime.datetime.now().strftime("%Y-%m-%d %H %M %S"))
	CAT_f = f'CAT_{SentencesCount}_'+nowstr+'.csv'
	DIF_f = f'DIF_{SentencesCount}_'+nowstr+'.csv'
	DOT_f = f'DOT_{SentencesCount}_'+nowstr+'.csv'

	Terms = set()
	Contexes = set()
	########################################################
	mycursor.execute(sql_term)
	rows = mycursor.fetchall()
	for r in rows:
		Terms.add(r[0])
	mycursor.execute(sql_context)
	rows = mycursor.fetchall()
	for r in rows:
		Contexes.add(r[0])
	########################################################	
	#print(f'Terms : {len(Terms)}')	
	#print(f'Contexes : {len(Contexes)}')
	Matrix = dict()
	for T in Terms:
		Matrix[T] = dict()
		for C in Contexes:
			Matrix[T][C] = 0;
	mycursor.execute(sql)
	rows = mycursor.fetchall()
	for r in rows:
		T = r[0].strip()
		C = r[1]
		n = r[2]
		if T in Matrix:
			if C in Matrix[T]:
				Matrix[T][C] += n
	FeatureVectors = dict()
	for T in Matrix:
		Vector = list()
		for V in Matrix[T]:
			c = Matrix[T][V]
			Vector.append(str(c))
		FeatureVectors[T] = np.array(Vector).astype(np.float)
	
	
	
	
	
	#For Concat
	CAT_writeFile = open(CAT_f, 'w',encoding="utf-8",newline='')
	CAT_writer = csv.writer(CAT_writeFile)
	CAT_writer.writerow(["Result"]+list(Contexes)+list(Contexes))
	
	#For Dif
	DIF_writeFile = open(DIF_f, 'w',encoding="utf-8",newline='')
	DIF_writer = csv.writer(DIF_writeFile)
	DIF_writer.writerow(["Result"]+list(Contexes))
	
	#For Dot
	DOT_writeFile = open(DOT_f, 'w',encoding="utf-8",newline='')
	DOT_writer = csv.writer(DOT_writeFile)
	DOT_writer.writerow(["Result"]+list(Contexes))
	
	
	with open("___DataSet.csv") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		il = 0
		for row in csv_reader:
			il += 1
			NP1 = row[0].strip()
			NP2 = row[1].strip()
			rsult = row[2].strip()
			if(rsult == 'True'):
				RES = 1
			else:
				RES = 0
			if NP1 in FeatureVectors and NP2 in FeatureVectors:
				
				FV1o = FeatureVectors[NP1]
				FV2o = FeatureVectors[NP2]
				
				FV1 = FeatureVectors[NP1].tolist()
				FV2 = FeatureVectors[NP2].tolist()
				
				CAT_VectorToAdd = [RES] + FV1 + FV2
				DIF_VectorToAdd = [RES] + (np.sqrt((FV1o-FV2o)*(FV1o-FV2o))).tolist()
				DOT_VectorToAdd = [RES] + (FV1o * FV2o).tolist()
				
				CAT_writer.writerow(CAT_VectorToAdd)
				DIF_writer.writerow(DIF_VectorToAdd)
				DOT_writer.writerow(DOT_VectorToAdd)
				
				
				
			#end if 
		#end for row
	#end with open dataset
	
	## Close files
	CAT_writeFile.close()
	DIF_writeFile.close()
	DOT_writeFile.close()
	# done close files
	
	print(f'File Created {CAT_f}')
	print(f'File Created {DIF_f}')
	print(f'File Created {DOT_f}')
	
	#'''
	#__MachineLearning__(DOT_f)
	#__MachineLearning__(DIF_f)
	#__MachineLearning__(CAT_f)
	#'''
	print('Program Ended ' + datetime.datetime.now().strftime("%Y-%m-%d %H %M %S"))
########
#__main__
__MachineLearning__('DIF_2019-10-26 07 28 29.csv')
'''
if( len(sys.argv) == 1):
	print("select option main for main, ml for machine learn")
elif(sys.argv[1] == "main"):
	print("main started")
	init()
	__main__()
elif(sys.argv[1] == "ml"):
	print("machine learn started")
	if(len() < 3):
		print("must define file")
	else:
		FileInput = sys.argv[2]
		__MachineLearning__(FileInput)
else:
	print("undefined command")
#'''