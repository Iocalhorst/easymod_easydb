from ezmod import Easyclass as ez
from ezmod import EasyDB, oops
import json
import os
import sys
import logging



def main():
	#edit the easydb.conf and put you database user and password there
	conf=ez.load(confname="mysql",fromfile=True,filename="easydb.conf",isjson=True)

	#print(conf)
	try : 
		db=EasyDB(conf)
		db.connect()
		print("connected")
		db.getversion()
	except :
		oops("couldnt connect")

	#script=ez.load(fromfile=True,issql=True,filename='film.sql')
	shellmode=False
	print("easydb cli - usage ")
	print('"load" <scriptfile.sql> to load a script')
	print('"run" to run it')
	print('"shell" to enter interactive mode')
	print('"exit" to exit')
	script=None
	while True :
		c=input('>').strip()
		args=c.split(' ')
		for i in range(len(args)):
			args[i]=args[i].replace('\n','')
			args[i]=args[i].strip()

		cmd=args[0]
		if cmd=="exit": 
			break
		elif cmd=="load" :
			try :	
				script=ez.load(fromfile=True,issql=True,filename=args[1])
				for command in script :
					print(command)
			except : 
				script=None
				oops("scriptfile not found")
		elif cmd=="run":
			if script :
				for command in script :
				#	print(command)
					db.cursor.execute(command)
				#	print("ok")
					rows=db.cursor.fetchall()
					for row in rows:
						if len(row>1):
							print(row)
				print("ok")
		elif cmd=="shell":
			print("entering interactive shell - enter exit to quit")
			while True:
				command=input("sql>").strip()
				if command=="exit": 
					print("leaving interactive shell mode")
					break
				else :
					try : 
						db.cursor.execute(command)
						rows=db.cursor.fetchall()
						print(rows)
					except :
						oops("sql error")


				#print('running '+(str(args[1])))
			#filename=[args]
		#args[1]
	#script=ez.load(fromfile=True,issql=True,filename='film.sql')
	#if db.connected :
	#	print(script)
	#for e in script:
	#	print(e)
	#for i,command in enumerate(script):
		#print("line "+str(i)+" "+command)
	#	db.cursor.execute(command)
	#	rows=db.cursor.fetchall()
		#print(rows)
		#print("total rows ",len(rows))
	

	#print(conf)


	#print(conf.__repr__)
main()