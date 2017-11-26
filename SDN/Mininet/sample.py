#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def myNet():


    #OpenDayLight controller
    ODL_CONTROLLER_IP='192.168.84.135'

    #Floodlight controller
    FL_CONTROLLER_IP='192.168.84.138'

    net = Mininet( topo=None, build=False)

    # Create nodes
    h1 = net.addHost('h1', mac='01:00:00:00:01:00', ip='192.168.0.1/24')
    h2 = net.addHost('h2', mac='01:00:00:00:02:00', ip='192.168.0.2/24')
    h3 = net.addHost('h3', mac='01:00:00:00:03:00', ip='192.168.0.3/24')
    h4 = net.addHost('h4', mac='01:00:00:00:04:00', ip='192.168.0.4/24')
    h5 = net.addHost('h5', mac='01:00:00:00:05:00', ip='192.168.0.5/24')
    h6 = net.addHost('h6', mac='01:00:00:00:06:00', ip='192.168.0.6/24')


    # Create switches
    s1 = net.addSwitch('s1', listenPort=6634, mac='00:00:00:00:00:01')
    s2 = net.addSwitch('s2', listenPort=6634, mac='00:00:00:00:00:02')
    s3 = net.addSwitch('s3', listenPort=6634, mac='00:00:00:00:00:03')
    s4 = net.addSwitch('s4', listenPort=6634, mac='00:00:00:00:00:04')
    s5 = net.addSwitch('s5', listenPort=6634, mac='00:00:00:00:00:05')
    s6 = net.addSwitch('s6', listenPort=6634, mac='00:00:00:00:00:06')

    print "*** Creating links"
    net.addLink(h1, s1, )
    net.addLink(h2, s2, )
    net.addLink(h3, s3, )
    net.addLink(s1, s2, )
    net.addLink(s2, s3, )
    net.addLink(s3, s4, )
    net.addLink(h4, s4, )
    net.addLink(h5, s5, )
    net.addLink(h6, s6, )
    net.addLink(s4, s5, )
    net.addLink(s5, s6, )

    # Add Controllers
    odl_ctrl = net.addController( 'c0', controller=RemoteController, ip=ODL_CONTROLLER_IP, port=6633)

    fl_ctrl = net.addController( 'c1', controller=RemoteController, ip=FL_CONTROLLER_IP, port=6633)


    net.build()

    # Connect each switch to a different controller
    s1.start([odl_ctrl])
    s2.start([odl_ctrl])
    s3.start([odl_ctrl])
    s4.start([fl_ctrl])
    s5.start([fl_ctrl])
    s6.start([fl_ctrl])


    s1.cmdPrint('ovs-vsctl show')

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNet()
