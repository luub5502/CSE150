# Final Skeleton
#
# Hints/Reminders from Lab 3:
#
# To check the source and destination of an IP packet, you can use
# the header information... For example:
#
# ip_header = packet.find('ipv4')
#
# if ip_header.srcip == "1.1.1.1":
#   print "Packet is from 1.1.1.1"
#
# Important Note: the "is" comparison DOES NOT work for IP address
# comparisons in this way. You must use ==.
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
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

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 3:
    #   - port_on_switch: represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet.
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # You should use these to determine where a packet came from. To figure out where a packet 
    # is going, you can use the IP header information.
    flow_mod = of.ofp_flow_mod()
    flow_mod.match = of.ofp_match.from_packet(packet)
    actions = []
    flow_mod.idle_timeout = 60
    flow_mod.hard_timeout = 60
    # block all IP traffic from Untrusted Host to Server
    # block all ICMP traffic from Untrusted Host to anywhere internally(host10-80 and server)
    # trusted host can send traffic to hosts in dept A(host10-40) but not sent ICMP and IP traffic to server and hosts in dept B (host50-80)
    # all ICMP traffic from Dept A to Dept B should be blocked and vice versa
    # switch id ? 
    
    # server: 10.3.9.90/24
    # trusted: 108.24.31.112/24
    # untrusted: 106.44.82.103/24
    # (switch, src_ip, dst_ip): src_port?
    ip = packet.find('ipv4')
    if ip is None:
      actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
      flow_mod.actions = actions
      return
    else:
      #A
      h10 = ['10.0.2.20/24', '10.0.3.30/24','10.0.4.40/24','108.24.31.112/24','10.3.9.90/24']
      h20 = ['10.0.1.10/24', '10.0.3.30/24','10.0.4.40/24','108.24.31.112/24','10.3.9.90/24']
      h30 = ['10.0.1.10/24', '10.0.2.20/24','10.0.4.40/24','108.24.31.112/24','10.3.9.90/24']
      h40 = ['10.0.1.10/24', '10.0.2.20/24','10.0.3.30/24','108.24.31.112/24','10.3.9.90/24']

      #B
      h50 = ['10.0.6.60/24', '10.0.7.70/24','10.0.8.80/24','108.24.31.112/24']
      h60 = ['10.0.5.50/24', '10.0.7.70/24','10.0.8.80/24','108.24.31.112/24']
      h70 = ['10.0.5.50/24', '10.0.6.60/24','10.0.8.80/24','108.24.31.112/24']
      h80 = ['10.0.5.50/24', '10.0.6.60/24','10.0.7.70/24','108.24.31.112/24']
      
      #h_trust = ['10.0.1.10/24', '10.0.2.20/24', '10.0.3.30/24','10.0.4.40/24']
      #h_untrust = ['10.0.2.20/24', '10.0.3.30/24','10.0.4.40/24','108.24.31.112/24','10.3.9.90/24']

      h_server = ['10.0.2.20/24', '10.0.3.30/24','10.0.4.40/24','108.24.31.112/24','10.3.9.90/24']
      src_ip = ip.srcip
      dst_ip = ip.dstip
      
      if switch_id == 1:
        #log.debug("Allowing packet")
        if dst_ip == '10.0.1.10/24':
          actions.append(of.ofp_action_output(port=1))
          flow_mod.actions = actions
          return
        elif dst_ip == '10.0.2.20/24':
          actions.append(of.ofp_action_output(port=2))
          flow_mod.actions = actions
          return
        elif (src_ip == '10.0.1.10/24' and dst_ip in h10) or (src_ip == '10.0.2.20/24' and dst_ip in h20):
          actions.append(of.ofp_action_output(port=3))
          flow_mod.actions = actions
          return
      elif switch_id == 2:
        #log.debug("Allowing packet")
        if dst_ip == '10.0.3.30/24':
          actions.append(of.ofp_action_output(port=1))
          flow_mod.actions = actions
          return
        elif dst_ip == '10.0.4.40/24':
          actions.append(of.ofp_action_output(port=2))
          flow_mod.actions = actions
          return
        elif (src_ip == '10.0.3.30/24' and dst_ip in h30) or (src_ip == '10.0.4.40/24' and dst_ip in h40):
          actions.append(of.ofp_action_output(port=3))
          flow_mod.actions = actions
          return
      elif switch_id == 3:
        if dst_ip == '10.0.5.50/24':
          actions.append(of.ofp_action_output(port=1))
          flow_mod.actions = actions
          return
        elif dst_ip == '10.0.6.60/24':
          actions.append(of.ofp_action_output(port=2))
          flow_mod.actions = actions
          return
        elif (src_ip == '10.0.5.50/24' and dst_ip in h50) or (src_ip == '10.0.6.60/24' and dst_ip in h60):
          actions.append(of.ofp_action_output(port=3))
          flow_mod.actions = actions
          return
      elif switch_id == 4:
        if dst_ip == '10.0.7.70/24':
          actions.append(of.ofp_action_output(port=1))
          flow_mod.actions = actions
          return
        elif dst_ip == '10.0.8.80/24':
          actions.append(of.ofp_action_output(port=2))
          flow_mod.actions = actions
          return
        elif (src_ip == '10.0.7.70/24' and dst_ip in h70) or (src_ip == '10.0.8.80/24' and dst_ip in h80):
          actions.append(of.ofp_action_output(port=3))
          flow_mod.actions = actions
          return
      elif switch_id == 5:
        if src_ip != '106.44.82.103/24':
          if dst_ip in ['10.0.1.10/24', '10.0.2.20/24']: # to s1
            actions.append(of.ofp_action_output(port=1))
            flow_mod.actions = actions
            return
          elif dst_ip in ['10.0.3.30/24','10.0.4.40/24']: # to s2
            actions.append(of.ofp_action_output(port=2))
            flow_mod.actions = actions
            return
          elif dst_ip in ['10.0.5.50/24', '10.0.6.60/24'] and (src_ip != '108.24.31.112/24'): # to s3
            actions.append(of.ofp_action_output(port=3))
            flow_mod.actions = actions
            return
          elif dst_ip in ['10.0.7.70/24','10.0.8.80/24'] and (src_ip != '108.24.31.112/24'): # to s4
            actions.append(of.ofp_action_output(port=4))
            flow_mod.actions = actions
            return
        if dst_ip == '108.24.31.112/24': # to trusted
          actions.append(of.ofp_action_output(port=5))
          flow_mod.actions = actions
          return
        elif dst_ip == '10.3.9.90/24': # to server
          actions.append(of.ofp_action_output(port=7))
          flow_mod.actions = actions
          return
      elif switch_id == 6:
        if dst_ip == '10.3.9.90/24':
          actions.append(of.ofp_action_output(port=2))
          flow_mod.actions = actions
          return
        elif dst_ip in h_server: 
          actions.append(of.ofp_action_output(port=1))
          flow_mod.actions = actions
          return
      else:
        return

    # if packet.find('icmp') and packet.find('arp'): # arp packet
    #     log.debug("Allowing ARP packet")
    #     actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    #     flow_mod.actions = actions
    # elif packet.find('ipv4') and packet.find('tcp'): # tcp packet
    #     log.debug("Allowing TCP packet")
    #     actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    #     flow_mod.actions = actions

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
