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
    def send_out(self, packet, packet_in, port1):
      msg = of.ofp_packet_out()
      msg.data = packet_in
      msg.actions.append(of.ofp_action_output(port = port1))
      self.connection.send(msg)  
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 3:
    #   - port_on_switch: represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet.
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # You should use these to determine where a packet came from. To figure out where a packet 
    # is going, you can use the IP header information.
    
    # block all IP traffic from Untrusted Host to Server
    # block all ICMP traffic from Untrusted Host to anywhere internally(host10-80 and server)
    # trusted host can send traffic to hosts in dept A(host10-40) but not sent ICMP and IP traffic to server and hosts in dept B (host50-80)
    # all ICMP traffic from Dept A to Dept B should be blocked and vice versa
    
    # server: 10.3.9.90/24
    # trusted: 108.24.31.112/24
    # untrusted: 106.44.82.103/24
    #ip = packet.find('ipv4')
    print("switch_id: ", switch_id)
    ip = packet.find('ipv4')
    if ip is None:
      print("flood")
      # flow_mod = of.ofp_flow_mod()
      # flow_mod.match = of.ofp_match.from_packet(packet)
      # actions = []
      # flow_mod.idle_timeout = 60
      # flow_mod.hard_timeout = 60
      # actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
      # flow_mod.actions = actions
      msg = of.ofp_packet_out()
      msg.data = packet_in
      msg.idle_timeout = 60
      msg.hard_timeout = 60
      msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      self.connection.send(msg)  
    else:
      
      
      #A
      server_ip = '10.3.9.90'
      h_untrust_ip = '106.44.82.103'
      h_trust_ip = '108.24.31.112'
      h10_ip, h20_ip, h30_ip, h40_ip, h50_ip, h60_ip, h70_ip, h80_ip = '10.1.1.10','10.1.2.20', '10.1.3.30','10.1.4.40','10.2.5.50','10.2.6.60', '10.2.7.70','10.2.8.80'
      h10_dest = [h20_ip, h30_ip,h40_ip,h_trust_ip,server_ip]
      h20_dest = [h10_ip, h30_ip,h40_ip,h_trust_ip,server_ip]
      h30_dest = [h10_ip, h20_ip,h40_ip,h_trust_ip,server_ip]
      h40_dest = [h10_ip, h20_ip,h30_ip,h_trust_ip,server_ip]

      #B
      h50_dest = [h60_ip, h70_ip,h80_ip,h_trust_ip]
      h60_dest = [h50_ip, h70_ip,h80_ip,h_trust_ip]
      h70_dest = [h50_ip, h60_ip,h80_ip,h_trust_ip]
      h80_dest = [h50_ip, h60_ip,h70_ip,h_trust_ip]
      
      #h_trust = ['10.0.1.10/24', '10.0.2.20/24', '10.0.3.30/24','10.0.4.40/24']
      #h_untrust = ['10.0.2.20/24', '10.0.3.30/24','10.0.4.40/24','108.24.31.112/24','10.3.9.90/24']

      h_server = [h20_ip, h30_ip, h40_ip, h_trust_ip, server_ip]
      src_ip = ip.srcip
      dst_ip = ip.dstip
      print("IP_PACKET")
      print("switch_id: ", switch_id)
      print("dest: ", dst_ip)
      print("src: ", src_ip)
      # flow_mod = of.ofp_flow_mod()
      # flow_mod.match = of.ofp_match.from_packet(packet)
      # actions = []
      # flow_mod.idle_timeout = 60
      # flow_mod.hard_timeout = 60
      
      if switch_id == 1:
        if dst_ip == h10_ip:
          print("host 10")
          send_out(packet, packet_in, 1)
        elif dst_ip == h20_ip:
          print("host 20")
          send_out(packet, packet_in, 2)
        elif (src_ip == h10_ip and dst_ip in h10_dest) or (src_ip == h20_ip and dst_ip in h20_dest):
          send_out(packet, packet_in, 3)
        else:
          return
      elif switch_id == 2:
        if dst_ip == h30_ip:
          send_out(packet, packet_in, 1)
        elif dst_ip == h40_ip:
          send_out(packet, packet_in, 2)
        elif (src_ip == h30_ip and dst_ip in h30_dest) or (src_ip == h40_ip and dst_ip in h40_dest):
          send_out(packet, packet_in, 3) 
        else:
          return
      elif switch_id == 3:
        if dst_ip == h50_ip:
          send_out(packet, packet_in, 1)
        elif dst_ip == h60_ip:
          send_out(packet, packet_in, 2)
        elif (src_ip == h50_ip and dst_ip in h50_dest) or (src_ip == h60_ip and dst_ip in h60_dest):
          send_out(packet, packet_in, 3)
        else:
          return
      elif switch_id == 4:
        if dst_ip == h70_ip:
          send_out(packet, packet_in, 1)
        elif dst_ip == h80_ip:
          send_out(packet, packet_in, 2)
        elif (src_ip == h70_ip and dst_ip in h70_dest) or (src_ip == h80_ip and dst_ip in h80_dest):
          send_out(packet, packet_in, 3)
        else:
          return
      elif switch_id == 5:
        if src_ip != h_untrust_ip:
          if dst_ip in [h10_ip, h20_ip]: # to s1
            send_out(packet, packet_in, 1)
          elif dst_ip in [h30_ip, h40_ip]: # to s2
            send_out(packet, packet_in, 2)
          elif dst_ip in [h50_ip, h60_ip] and (src_ip != h_trust_ip): # to s3
            send_out(packet, packet_in, 3)
          elif dst_ip in [h70_ip,h80_ip] and (src_ip != h_trust_ip): # to s4
            send_out(packet, packet_in, 4)
          elif dst_ip == h_trust_ip: # to trusted
            send_out(packet, packet_in, 5)
          elif dst_ip == server_ip and (src_ip != h_trust_ip): # to server
            send_out(packet, packet_in, 7)
          else:
            return
      elif switch_id == 6:
        if dst_ip == server_ip:
          send_out(packet, packet_in, 2)
        elif dst_ip in h_server: 
          send_out(packet, packet_in, 1)
        else:
          return
      else:
        return

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