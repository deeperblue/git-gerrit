#!/usr/bin/python
#coding=utf-8

#
#	发送数据到从dow server 端
#

import socket
import sys
import os
from xml.dom.minidom import parse
import xml.dom.minidom

##server para####
#CURRENT_HOST[ip]="172.16.8.48"
#CURRENT_HOST[LinuxSamba]="/home/zhangbin/meitu/"
#CURRENT_HOST[WinSamba]="z:\\"
#CURRENT_HOST[Win]=r'"C:\Program Files\Notepad++\notepad++.exe"'
#CURRENT_HOST[WinCompare]=r'"C:\Program Files (x86)\Beyond Compare 4\BCompare.exe"'
#
CFG_FILE=os.path.join(os.path.expandvars('$HOME'), ".dow/config")

PARAMETER_LIST=( "ip", "LinuxSamba", "WinSamba", "Win", "WinCompare" )
####function####
port=48879

def show_str(str):
        print "\033[1;31;40m" + str  + "\033[0m"


def send_cmd(cmd):
	try:
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((CURRENT_HOST["ip"],port))
		s.send(cmd)
		data=s.recv(1024)	
		s.close()
		return int(data)
	except ValueError:		
		return -1

def linuxPath2winPath(linux_path):
	win_path=linux_path.replace(CURRENT_HOST["LinuxSamba"], CURRENT_HOST["WinSamba"])
	win_path=win_path.replace("/", "\\")	
	return win_path

def do_help():
        print CMD_ACTIONS.keys()

def is_path_valid(path):
	#print CURRENT_HOST["LinuxSamba"]
	#print path
	if CURRENT_HOST["LinuxSamba"] in path and os.path.exists(path) == True:
		return True
	return False

def do_win():
	for i in range(1, len(sys.argv)):
		full_path = os.path.realpath(sys.argv[i])
		if is_path_valid(full_path):
			show_str("Open " + full_path)		
			sendcmd = "\"" + CURRENT_HOST["Win"] + "\" " + linuxPath2winPath(full_path)		
			send_cmd(sendcmd)
		else:
			show_str("File " + sys.argv[1] + "is not exist!")			
	
def do_windir():
	for i in range(1, len(sys.argv)):
		full_path = os.path.realpath(sys.argv[i])
		if os.path.isdir(full_path) == True:
			dir_path = full_path
		else:			
			dir_path = os.path.dirname(full_path)		
		if is_path_valid(dir_path):
			show_str("Open dir " + dir_path)		
			sendcmd = "explorer " + linuxPath2winPath(dir_path)		
			send_cmd(sendcmd)		
		else:
			
			show_str("File " + sys.argv[1] + "is not exist!")			

def do_wincompare():	
	if len(sys.argv) == 3:
		src_path = os.path.realpath(sys.argv[1])
		tar_path = os.path.realpath(sys.argv[2])
		if is_path_valid(src_path) and is_path_valid(tar_path):
			sendcmd = "\"" + CURRENT_HOST["WinCompare"]  + "\" " +  linuxPath2winPath(src_path) + " " + linuxPath2winPath(tar_path)	 
			send_cmd(sendcmd)
	else:
		sendcmd = "\"" + CURRENT_HOST["WinCompare"] + "\""
		for i in range (1, len(sys.argv) - 1):
			#show_str(sys.argv[i])
			p = os.path.realpath(sys.argv[i])
			if is_path_valid(p):
				sendcmd += " " + linuxPath2winPath(p)
			else:
				show_str(sys.argv[i] + "is not exist")
				exit(1)
		#show_str(sendcmd)        
		return send_cmd(sendcmd)

## do init things
def create_element(doc, tag, attr):
    #创建一个元素节点
    elementNode = doc.createElement(tag)
    #创建一个文本节点
    textNode = doc.createTextNode(attr)
    #将文本节点作为元素节点的子节点
    elementNode.appendChild(textNode)
    return elementNode
	
def env_init():
	DOW_CONFIG_DIR=os.path.join(os.path.expandvars('$HOME'), ".dow/")
	if os.path.exists(os.path.join(DOW_CONFIG_DIR)) == False:
		os.makedirs(DOW_CONFIG_DIR)
	
	CURRENT_HOST={}
	hosts_list=[]
	if os.path.exists(CFG_FILE) == False:
		show_str("env is not set! Pls set it first")
		para_list={}
		for i in PARAMETER_LIST:
				content = raw_input("Please input " + i + " : ")
				if (content != "" ) or (content == "null"):
					para_list[i] = content                        
				else:
					show_str("error! invaild value")
					return -1
						
		##write config file
		dom1 = xml.dom.getDOMImplementation()#创建文档对象，文档对象用于创建各种节点。
		doc = dom1.createDocument(None, "config", None)
		top_element = doc.documentElement# 得到根节点
		hosts_list = [{'ip': para_list["ip"], 'Win': para_list["Win"], 'WinCompare': para_list["WinCompare"], 'LinuxSamba': para_list["LinuxSamba"], 'WinSamba': para_list["WinSamba"]}]
		#sNode=doc.createElement('CurrentCURRENT_HOST[ip]')
		for h in hosts_list:
			sNode = doc.createElement('hosts')
			sNode.setAttribute('ip',str(h['ip']))
			
			LNode = create_element(doc,'LinuxSamba',h['LinuxSamba'])
			WNode = create_element(doc,'WinSamba',h['WinSamba'])
			WinNode = create_element(doc,'Win',h['Win'])
			WinCompareNode = create_element(doc,'WinCompare',h['WinCompare'])
			
			sNode.appendChild(LNode)
			sNode.appendChild(WNode)
			sNode.appendChild(WinNode)
			sNode.appendChild(WinCompareNode)
			top_element.appendChild(sNode)# 将遍历的节点添加到根节点下
		
		
		xmlfile = open(CFG_FILE,'wb')
		doc.writexml(xmlfile,addindent=' '*4, newl='\n', encoding='utf-8')
		xmlfile.close()
		CURRENT_HOST = hosts_list
	else:		
		# 使用minidom解析器打开 XML 文档
		DOMTree = xml.dom.minidom.parse(CFG_FILE)
		collection = DOMTree.documentElement
		if collection.hasAttribute("CurrentHost"):
		   print "CurrentCURRENT_HOST[ip] : %s" % collection.getAttribute("CurrentHost")

		# 在集合中获取所有主机
		xmlhosts = collection.getElementsByTagName("hosts")
		# 打印每部主机的详细信息
		i = 0
		for h in xmlhosts:		   
		   IP = h.getAttribute('ip')		   
		   #print "ip: %s" % IP
		   win = h.getElementsByTagName('Win')[0]
		   #print "win: %s" % win.childNodes[0].data		   		   
		   wincompare = h.getElementsByTagName('WinCompare')[0]
		   #print "wincompare: %s" % wincompare.childNodes[0].data		   
		   LinuxSamba = h.getElementsByTagName('LinuxSamba')[0]
		   #print "LinuxSamba: %s" % LinuxSamba.childNodes[0].data		   
		   WinSamba = h.getElementsByTagName('WinSamba')[0]
		   #print "WinSamba: %s" % WinSamba.childNodes[0].data
		   hosts_list.insert(i, {'ip': IP, 'Win': win.childNodes[0].data, 'WinCompare': wincompare.childNodes[0].data, 'LinuxSamba': LinuxSamba.childNodes[0].data, 'WinSamba': WinSamba.childNodes[0].data})	
		   i += 1
		if i == 1:
		   CURRENT_HOST = hosts_list[0]
	#print CURRENT_HOST
	return CURRENT_HOST, hosts_list
		
		
CMD_ACTIONS = {  
"win":do_win,        
"windir":do_windir,
"wincompare":do_wincompare
}   
	
####main####
CURRENT_HOST={}
if len(sys.argv) > 1: 
	cmd=CMD_ACTIONS.get(os.path.basename(sys.argv[0]))
	if not cmd:	
		show_str("unknow cmd")
		do_help()
		exit(1)
	(CURRENT_HOST, HOSTS_LIST) = env_init()
	if len(CURRENT_HOST) != 0:
		cmd()
	else:
		show_str("Could not found CURRENT_HOST!")
		exit(1)
else:
	do_help()
	exit(1)