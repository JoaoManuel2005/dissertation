
# Wireshark captures

I ran:
```bash
nslookup wireshark.org
```

I got:
![[Pasted image 20261008165504.png]]

Packet 1:

![[Pasted image 20261008170141.png]]

This is from 127.0.0.1 to 127.0.0.53 which is from the process running nslookup to the Linux stub resolver

Packet 2:

![[Pasted image 20261008170221.png]]

This is from 192.168.0.21 to 194.168.4.100. THis is from my machines IP to an upstream DNS server (ISP or router)

This forwards the query as type A and for same domain name, but changes transaction ID

Includes additional information to increase allowed UDP payload size

Packet 3:

![[Pasted image 20261008170323.png]]

This is from 192.168.4.100 (the upstream DNS server) to 192.168.0.21 (my machines IP). This is of type response and matches the query transaction ID

It provides 3 different IPv4 addresses for `wireshark.org` and tells the client it can cache them for 300 secons

Packet 4:

![[Pasted image 20261008170346.png]]

This is from 127.0.0.53 (local stub resolver) to 127.0.0.1 (application) and its transacton ID matches the original query

This delivers the same 3 IP addresses to the application