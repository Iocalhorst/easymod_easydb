import os
import sqlite3
import sys
import traceback
import json

conffile="easydb.conf"

def oops(*args):
	print("oops")
	for arg in args:
		print(arg)

def ezjason(line):
		try : 
			data=json.loads(line.replace('\n',''))
		except : 
			oops("json error")
			data=None
		return data	

class EasyDB():
	def __init__(self,conf):
		self.conf=conf
		self.connected=False
		
		
	#	self.connection=pymysql.connect("localhost","dbuser","password123456","TESTDB" )
		#pymysql.connect("localhost","dbuser","password123456","TESTDB" )
	def connect(self):
		if self.conf["dialect"]=="sqlite3":
			print("sqlite3 case")
		elif self.conf["dialect"]=="mysql":
			#print("mysql case")
			import pymysql
			self.con=pymysql.connect(host='localhost',user='dbuser',password='password123456',database='mysql')
			self.cursor=self.con.cursor()
			self.connected=True
	
	def getversion(self):
			self.cursor.execute('SELECT VERSION()')
			version = self.cursor.fetchone()
			print(f'Database version: {version[0]}')

class Easyclass():

	@staticmethod
	def load(*args,**kwargs):
		#print(kwargs)

		if "fromfile" in kwargs:
			filename=kwargs["filename"]
			try : file=open(filename,'r')
			except : oops("nosuchfile")
			try : lines=file.readlines()
			except : oops("cantreadthis")
		if "issql" in kwargs :
			s_lines=[]
			validlines=[]
			for i,line in enumerate(lines):
				line=line.replace('\n','').strip()
				s_lines.append(line)
			for line in s_lines :
				if not (line[0] in ["#","--"]):
					validlines.append(line)
			return validlines

			#print(s_lines)
			#for line in lines :
			#	print(line,"\n")
				#if line[0] in ["#","-"] :
				#	lines.remove(line)
				#	print("removed")
					#line=line.replace('\n','').strip()
			#for i,line in enumerate(lines) :
			#	lines[i]=line.replace('\n','').strip()
			#print(lines)
		#	return lines
				

		if "isjson" in kwargs:	
			data={}
			for index,line in enumerate(lines):
				try :
					newdata=ezjason(line)
				except : 
					oops("json error - line "+str(index)+" ignored.")
					newdata=None
				data.update(newdata)
				

			if ("confname" not in kwargs):
				return data
			else :
				key=kwargs["confname"]
				#print(key)
				if key in data :
				#	print("keyindata")
					return data[key]
				else : 
					oops("conf not found")
					return None