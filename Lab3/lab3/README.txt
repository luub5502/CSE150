Lab 3 explanations:

Since pingall uses ICMP, all the packets will be dropped due to the firewall only accepting TCP and ARP packets. 

Dpctl dump flows dumps all the entries in the flow table from the pingall. I set my timeout to 60 seconds so it shows all the packets saved into the flow table within the last 60 seconds. It also shows icmp packets that were marked as dropped, and ARP packets that were marked as FLOOD which is what was specified in the firewall. 

Iperf tests TCP bandwidth by generating TCP traffic between 2 hosts. Since TCP traffic is allowed by the firewall, it should succeed. 
