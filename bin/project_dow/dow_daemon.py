#!/usr/bin/python
#coding=utf-8

#
#	监听从dow client 端发来的命令并执行
#


import socket
import os
import commands
import optparse,subprocess
import sys
import datetime
import pickle
import string
import codecs

####function####

def show_str(str):
        print "\033[1;31;40m" + str  + "\033[0m"


def dow_run_programme(pro):
	ret = os.system(pro)
	return ret

#def dow_run_programme(cmd):
#	cmd = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#	out, err = cmd.communicate()
#	if cmd.returncode != 0:
#		print >> sys.stderr, 'Error do cmd:' + cmd.to
#		print >> sys.stderr, err
#		return None, None
#	else:
#		return out, err

####main####
host=socket.gethostbyname(socket.gethostname())#得到本地ip
ports=[ 48879, 48880 ]

show_str("Server Ip is " + host)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
for p in ports:
	try:
		s.bind((host,p))
		s.listen(5)
	except socket.error:		
		pass
while 1:
	sock,addr=s.accept()
	print "got connection form ",sock.getpeername()
	data=sock.recv(1024)
	if not data:
		break
	else:
		print data
		ret = dow_run_programme(data)
		print ret
		ret_str = str(ret)
		print ret_str
		sock.send(ret_str)
		#exit(0)
#os.system(r'"C:\Program Files\Notepad++\notepad++.exe"' + "  test.log")
