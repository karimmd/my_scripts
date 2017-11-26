import xml.etree.ElementTree as ET
import requests
from requests.auth import HTTPBasicAuth
import json
import unicodedata
import networkx as nx
import matplotlib.pyplot as plt
import time
from sys import exit
from subprocess import Popen, PIPE
def getResponce(url,choice):
	response = requests.get(url, auth=HTTPBasicAuth('admin','admin'))
	if (response.ok):
		jData = json.loads(response.content)
		if(choice=='topology'):
			getTopoInfo(jData)
		if(choice=='statistics'):
			getStats(jData)
def getTopoInfo(data):
	global src_port
	global dest_port
	global node_lst
	global src_link_lst
	global dest_link_lst
	global index
	global link_lst
	global srcport
	global destport
	global hostport
	global ports
	#Finding MAC and IP
	for nettopo in data["network-topology"]["topology"]:
		for nodes in nettopo["node"]:
			if('host-tracker-service:addresses') in nodes:
				for net_info in nodes['host-tracker-service:addresses']:
					ip = net_info["ip"].encode('ascii','ignore')
					host = ip[-1]
					mac = net_info["mac"].encode('ascii','ignore')
					node_lst.append(ip)
			#Finding Switch ID and Ports
			if('host-tracker-service:attachment-points') in nodes:
				for net_info in nodes['host-tracker-service:attachment-points']:
					temp = net_info["tp-id"].encode('ascii','ignore')
					switchID = temp[0:10]
					port = temp[-1].encode('ascii','ignore')	
#					print("Host ",host, "with IP", ip ,"and MAC ", mac, " is connected with switch ",switchID, "and port ", port)
					link_lst.append(switchID)
					hostport.append(port)
				
		for i in range(len(node_lst)):
			G.add_edge(node_lst[i],link_lst[i])
	#Finding Switch Links
	#for nettopo in data["network-topology"]["topology"]:
		for links in nettopo["link"]:
			if("host" not in links['link-id']):
				temp_src=links['link-id']
				src = temp_src[0:10]
				src_link_lst.append(src)
				src_switch=src[-1].encode('ascii','ignore')
				src_port = temp_src[-1].encode('ascii','ignore')
				srcport.append(src_port)
				ports.append(temp_src[10:])
				temp_dest=links['destination']['dest-tp']
				dest = temp_dest[0:10]
				dest_link_lst.append(dest)
				dest_switch=dest[-1].encode('ascii','ignore')
				dest_port = temp_dest[-1].encode('ascii','ignore')
				destport.append(dest_port)
#				print(src, ":", src_port, "is connected with destination" , dest, ":",dest_port )
				
				if(src in link_lst):
					a=link_lst.index(src)
					src_switch=link_lst[a]
					G.add_edge(src,dest)
def getStats(data):
	print("Cost Computation")
	global cost
	
	BW = 0
	for i in data["node-connector"]:
		tx = int(i["opendaylight-port-statistics:flow-capable-node-connector-statistics"]["packets"]["transmitted"])
		rx = int(i["opendaylight-port-statistics:flow-capable-node-connector-statistics"]["packets"]["received"])
		BW = tx + rx
		#print(rx,current_node)
		#print(BW)
		time.sleep(2)	
	response = requests.get(stats, auth=HTTPBasicAuth('admin', 'admin'))
	tempJSON = ""
	if(response.ok):
		tempJSON = json.loads(response.content)
		
	for i in tempJSON["node-connector"]:
		tx = int(i["opendaylight-port-statistics:flow-capable-node-connector-statistics"]["packets"]["transmitted"])
		rx = int(i["opendaylight-port-statistics:flow-capable-node-connector-statistics"]["packets"]["received"])
		cost = tx + rx - BW
	#print(cost)
def systemCommand(cmd):
	terminalProcess = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
	terminalOutput, stderr = terminalProcess.communicate()
	print "\n*** Flow Pushed\n"

def pushFlows(bestPath):
	#for i in node_lst(0,len(node_lst)):
	a=node_lst.index(source)
	#print(a)
	for currentNode in range(0, len(bestPath)-1):
		if (currentNode==0):
			inport = hostport[a]
			#print("Inport for Source in if = ", inport)
			srcNode = bestPath[currentNode]
			#print("Src Node is = ", srcNode)
			dstNode = bestPath[currentNode+1]
			#print("Dest Node = ", dstNode)
			for i in range(0,len(src_link_lst)):
				if(srcNode==src_link_lst[i] and dstNode==dest_link_lst[i]):
					outport=srcport[i]
			#print("Outport in if is =",outport)
		else:
			prevNode = bestPath[currentNode-1]
			#print("Previous Node was in else = ",prevNode)
			srcNode = bestPath[currentNode]
			#print("Now Src Node is =",srcNode)
			dstNode = bestPath[currentNode+1]
			#print("Now Dest Node is =",dstNode)
			for i in range(0,len(src_link_lst)):
				if(prevNode==src_link_lst[i] and srcNode==dest_link_lst[i]):
					inport=destport[i]
			#print("Now Inport is =",inport)
			for i in range(0,len(dest_link_lst)):
				if(srcNode==src_link_lst[i] and dstNode==dest_link_lst[i]):
					outport=srcport[i]
			#print("outport in else is",outport)
			#print ("And outport is =",outport)
		#print("this is node now",bestPath	[-1])
		xmlSrcToDst = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>32767</priority><flow-name>Load Balance 1</flow-name><match><in-port>' + inport +'</in-port><ipv4-destination>10.0.0.1/32</ipv4-destination><ipv4-source>10.0.0.4/32</ipv4-source><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>1</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + outport +'</output-node-connector></output-action></action></apply-actions></instruction></instructions></flow>\''
		
		xmlDstToSrc = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>32767</priority><flow-name>Load Balance 2</flow-name><match><in-port>' + outport +'</in-port><ipv4-destination>10.0.0.4/32</ipv4-destination><ipv4-source>10.0.0.1/32</ipv4-source><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>2</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + inport +'</output-node-connector></output-action></action></apply-actions></instruction></instructions></flow>\''

		flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/"+ bestPath[currentNode] +"/table/0/flow/1"

		
		command = 'curl --user "admin":"admin" -H "Accept: application/xml" -H "Content-type: application/xml" -X PUT ' + flowURL + ' -d ' + xmlSrcToDst

		systemCommand(command)

		flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/"+ bestPath[currentNode] +"/table/0/flow/2"

		command = 'curl --user "admin":"admin" -H "Accept: application/xml" -H "Content-type: application/xml" -X PUT ' + flowURL + ' -d ' + xmlDstToSrc

		systemCommand(command)

	srcNode = bestPath[-1]
	#print("Src Node at end: ",srcNode)
	prevNode = bestPath[-2]
	#print prevNode
	b=node_lst.index(dest)
	for i in range(0,len(src_link_lst)):
		if(srcNode==dest_link_lst[i] and prevNode==src_link_lst[i]):
			inport=destport[i]
	#print("inport at end:",inport)
	#print(inport)
	outport = hostport[b]
	
	#print("outport at end:",outport)
	xmlSrcToDst = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>32767</priority><flow-name>Load Balance 1</flow-name><match><in-port>' + inport +'</in-port><ipv4-destination>10.0.0.1/32</ipv4-destination><ipv4-source>10.0.0.4/32</ipv4-source><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>1</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + outport +'</output-node-connector></output-action></action></apply-actions></instruction></instructions></flow>\''

	xmlDstToSrc = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>32767</priority><flow-name>Load Balance 2</flow-name><match><in-port>' + outport +'</in-port><ipv4-destination>10.0.0.4/32</ipv4-destination><ipv4-source>10.0.0.1/32</ipv4-source><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>2</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + inport	 +'</output-node-connector></output-action></action></apply-actions></instruction></instructions></flow>\''

	flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ bestPath[-1] +"/table/0/flow/1"
	
	command = 'curl --user \"admin\":\"admin\" -H \"Accept: application/xml\" -H \"Content-type: application/xml\" -X PUT ' + flowURL + ' -d ' + xmlSrcToDst

	systemCommand(command)

	flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ bestPath[-1] +"/table/0/flow/2"

	command = 'curl --user "admin":"admin" -H "Accept: application/xml" -H "Content-type: application/xml" -X PUT ' + flowURL + ' -d ' + xmlDstToSrc

	systemCommand(command)

#main
node_lst = []
link_lst = []
src_link_lst = []
dest_link_lst = []
srcport = []
destport = []
all_costs = []
path_lst = []
hostport = []
ports = []
global all_paths
global key
global h1
global current_node
global source
global dest

print("Enter Source Host =")
h1 = int(input())
print("Enter Destination Host =")
h2 = int(input())
source = "10.0.0."+str(h1)
dest = "10.0.0."+str(h2)
G=nx.Graph()
flag = 'True'
while flag:
	try:
		node_lst[:] = []
		link_lst[:] = []
		src_link_lst[:] = []
		dest_link_lst[:] = []
		srcport[:] = []
		destport[:] = []
		all_costs[:] = []
		path_lst[:] = []
		hostport[:] = []
		topo = "http://localhost:8181/restconf/operational/network-topology:network-topology"
		getResponce(topo,"topology")
		if(dest not in node_lst):
			import new
			exit()
#print("Shortest Path from source to destination is ")
		for paths in nx.all_shortest_paths(G,source,dest):
			all_path = paths[1:(len(paths)-1)]
			#print(all_path)
			for paths in range(0,len(all_path)):
				for node in range(0,len(all_path)-1):
					current_node = all_path[node]
			#		print(current_node)
					next_node = all_path[node+1]
					current_path=str(current_node)+str(next_node)
			#		print(current_path)
					for i in range(0,len(src_link_lst)):
						if(current_node==src_link_lst[i] and next_node==dest_link_lst[i]):
							key=srcport[i]
						#print(key)
			stats = "http://localhost:8181/restconf/operational/opendaylight-inventory:nodes/node/"+str(current_node)+"/node-connector/"+str(current_node)+":"+str(key)
			getResponce(stats,"statistics")
			current_path = current_path.strip('::')
			#print(current_path)
#			cost = 0
			current_path = ""
			print(all_path,"cost is =",cost)
			all_costs.append(cost)
			path_lst.append(all_path)
			#print(path_lst)
			cost_index=all_costs.index(min(all_costs))
			#print(cost_index)
			best_path = path_lst[cost_index]
		print("Best path is: ",best_path)
		
		pushFlows(best_path)
		time.sleep(30)
#		nx.draw(G)
#		plt.show()
	except KeyboardInterrupt:
		break
		exit
##########################################################################################################################

