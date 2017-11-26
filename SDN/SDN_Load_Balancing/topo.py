
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController, OVSSwitch, Controller
from mininet.log import setLogLevel, info

def myTopo():

	"This is my first Topology"
	
	net = Mininet (controller = Controller, switch = OVSSwitch)

	info("*** Starting Controllers *** \n")
	c0 = net.addController(name='odlController' ,
                                 controller=RemoteController ,
                                 ip='127.0.0.1')
       
	info("Adding Switches \n")
	s1=net.addSwitch('s1')
	s2=net.addSwitch('s2')
	s3=net.addSwitch('s3')
	s4=net.addSwitch('s4')
	s5=net.addSwitch('s5')
	
	info("Adding Hosts \n")
	h1=net.addHost('h1')
	h2=net.addHost('h2')
	h3=net.addHost('h3')
	h4=net.addHost('h4')
	
	info("Adding Links \n")
	net.addLink(h1, s1)
	net.addLink(h2, s1)
	net.addLink(h3, s3)
	net.addLink(h4, s3)
	net.addLink(s1, s2)
	net.addLink(s2, s3)
	net.addLink(s1, s4)
	net.addLink(s3, s4)
	net.addLink(s1, s5)
	net.addLink(s3, s5)
	
	info("Starting Network \n")
	net.start()
	CLI(net)
	info("Stoping Network \n")
	net.stop()
if __name__ == '__main__':
	setLogLevel( 'info' )
	myTopo()
