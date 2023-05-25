# Lab 3 Skeleton
#
# Based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet.
    flow_mod = of.ofp_flow_mod()
    flow_mod.match = of.ofp_match.from_packet(packet)
    actions = []
    flow_mod.idle_timeout = 60
    flow_mod.hard_timeout = 60
    
    if packet.find('ipv4') and packet.find('arp'): # arp packet
        log.debug("Allowing ARP packet")
        actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        flow_mod.actions = actions
    elif packet.find('ipv4') and packet.find('tcp'): # tcp packet
        log.debug("Allowing TCP packet")
        actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        flow_mod.actions = actions
        
    self.connection.send(flow_mod)



  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
