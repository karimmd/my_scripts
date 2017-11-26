from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import Controller,OVSSwitch, RemoteController
from mininet.topo import Topo
from mininet.cli import CLI
def myTopo():

	info("This topology contains two controllers \n")
	
	net = Mininet (controller = Controller, switch = OVSSwitch)
	
	info("*** Starting Controllers *** \n")
	c0 = net.addController(name='odlController' ,
                                 controller=RemoteController ,
                                 ip='172.16.6.39')
                               		
	c1 = net.addController(name='odlController' ,
                                 controller=RemoteController ,
                                 ip='172.16.2.142')
                           
	info("*** Starting Switches *** \n")
	s1 = net.addSwitch ('s1')
	s2 = net.addSwitch ('s2')
	s3 = net.addSwitch ('s3')
	s4 = net.addSwitch ('s4')
	s5 = net.addSwitch ('s5')

	info("*** Starting Hosts *** \n")
	h1 = net.addHost ('h1')
	h2 = net.addHost ('h2')
	h3 = net.addHost ('h3')
	h4 = net.addHost ('h4')
	h5 = net.addHost ('h5')
	h6 = net.addHost ('h6')
	h7 = net.addHost ('h7')

	info("*** Adding Links *** \n")

	net.addLink(h1, s1)
	net.addLink(h2, s1)
	net.addLink(h3, s2)
	net.addLink(h4, s2)
	net.addLink(h5, s3)
	net.addLink(h6, s4)
	net.addLink(h7, s5)
	net.addLink(s1, s2)
	net.addLink(s2, s3	)
	net.addLink(s3, s5)
	net.addLink(s3, s4)

	info("***Starting Network *** \n")
	net.build()
	c0.start()
	c1.start()
	s1.start( [ c0 ] )
	s2.start( [ c0 ] )
	s3.start( [ c1 ] )
	s4.start( [ c1 ] )
	s5.start( [ c1 ] )

	CLI(net)
	info("***Ending Network ***")
	net.stop()

if __name__ =='__main__':
	setLogLevel( 'info' )  # for CLI output
        myTopo()
