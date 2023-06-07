#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    # Examples!
    # Create a host with a default route of the ethernet interface. You'll need to set the
    # default gateway like this for every host you make on this assignment to make sure all 
    # packets are sent out that port. Make sure to change the h# in the defaultRoute area
    # and the MAC address when you add more hosts!
    # h1 = self.addHost('h1',mac='00:00:00:00:00:01',ip='1.1.1.1/24', defaultRoute="h1-eth0")
    # h2 = self.addHost('h2',mac='00:00:00:00:00:02',ip='2.2.2.2/24', defaultRoute="h2-eth0")
    # floor 1 hosts
    h10 = self.addHost('h10',mac='00:00:00:00:00:01',ip='10.0.1.10/24', defaultRoute="h10-eth0")
    h20 = self.addHost('h20',mac='00:00:00:00:00:02',ip='10.0.2.20/24', defaultRoute="h20-eth0")
    h30 = self.addHost('h30',mac='00:00:00:00:00:03',ip='10.0.3.30/24', defaultRoute="h30-eth0")
    h40 = self.addHost('h40',mac='00:00:00:00:00:04',ip='10.0.4.40/24', defaultRoute="h40-eth0")
    # floor 2 hosts
    h50 = self.addHost('h50',mac='00:00:00:00:00:05',ip='10.2.5.50/24', defaultRoute="h50-eth0")
    h60 = self.addHost('h60',mac='00:00:00:00:00:06',ip='10.2.6.60/24', defaultRoute="h60-eth0")
    h70 = self.addHost('h70',mac='00:00:00:00:00:07',ip='10.2.7.70/24', defaultRoute="h70-eth0")
    h80 = self.addHost('h80',mac='00:00:00:00:00:08',ip='10.2.8.80/24', defaultRoute="h80-eth0")

    trusted_host = self.addHost('h_trust',mac='00:00:00:00:00:09',ip='108.24.31.112/24', defaultRoute="h_trust-eth0")
    untrusted_host = self.addHost('h_untrust',mac='00:00:00:00:00:10',ip='106.44.82.103/24', defaultRoute="h_untrust-eth0")
    server = self.addHost('h_server',mac='00:00:00:00:00:11',ip='10.3.9.90/24', defaultRoute="h_server-eth0")
    # Create a switch. No changes here from Lab 1.
    # s1 = self.addSwitch('s1')
    f1s1 = self.addSwitch('f1s1')
    f1s2 = self.addSwitch('f1s2')
    f2s1 = self.addSwitch('f2s1')
    f2s2 = self.addSwitch('f2s2')
    core = self.addSwitch('core')
    dataCenter = self.addSwitch('dataCenter')
    # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on 
    # Host 2. This is representing the physical port on the switch or host that you are 
    # connecting to.
    #
    self.addLink(core,dataCenter)
    #floor 1 connections
    self.addLink(h10, f1s1, port1 = 0, port2 = 8)
    self.addLink(h20, f1s1, port1 = 0, port2 = 9)
    self.addLink(core, f1s1)
    self.addLink(h30, f1s2)
    self.addLink(h40, f1s2)
    self.addLink(core, f1s2)
    #floor 2 connections 
    self.addLink(h50, f2s1)
    self.addLink(h60, f2s1)
    self.addLink(core, f2s1)
    self.addLink(h70, f2s2)
    self.addLink(h80, f2s2)
    self.addLink(core, f2s2)

    self.addLink(core, trusted_host)
    self.addLink(core, untrusted_host)

    # IMPORTANT NOTES: 
    # - On a single device, you can only use each port once! So, on s1, only 1 device can be
    #   plugged in to port 1, only one device can be plugged in to port 2, etc.
    # - On the "host" side of connections, you must make sure to always match the port you 
    #   set as the default route when you created the device above. Usually, this means you 
    #   should plug in to port 0 (since you set the default route to h#-eth0).
    #
    # self.addLink(s1,h1, port1=8, port2=0)
    # self.addLink(s1,h2, port1=9, port2=0)

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()
  h10, h20, h30, h40, h50, h60, h70, h80 = net.get('h10', 'h20', 'h30', 'h40','h50', 'h60', 'h70', 'h80')  
  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
