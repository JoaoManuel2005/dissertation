
Sources: 
- https://dl.acm.org/doi/epdf/10.1145/2504730.2504734

# On Measuring the client-side DNS infrastructure

"Our measurements cover only a fraction of the Internet and therefore we must consider bias"

"Non-interference with normal operation" even in "cache injections"

## Client-side infrastructure

Ingress servers - receieve DNS queries directly from user devices

Egress servers - directly communicate with authoritative DNS servers

Hidden servers - act as intermediaries bewteen ingess and egress but are not exposed to clients or ADNS

Origin devices - user devices or sources of probing requests

ODNSes (open DNS) - ingress servers that accept requests from any host

RDNSes (recursive DNS resolvers) - egress resolvers that communicate directly with ADNSes

FDNSes (forwarding ODNS) - ODNS that does not resolve query itself but forwards query to another resolver

RDNSdes (direct RDNS) - RDNSes that are also ODNSes, ie.e both an ingress and egress server

RDNSies (indirect RDNS) - RDNSes observed at the ADNS resolving queries on behalf of an FDNS

HDNSes (hidden DNS) - servers which operate between FDNSes and RDNSes. Neithing ingress nor egress and invisible externally

A typical path is:
1. Client computer starts by sending a DNS request to a home routing device (FDNS)
2. FDNS forwards the request through a chain of zero or more HDNSes and ultimately to an RDNSi
3. RDNSi sends the request to the appropriate ADNS
	- RDNSi may cooperate with other RDNSIes and subsequent requests from the same FDNS may be handled by a differed RDNSi
	- This structure is called an RDNS pool

## Measurement techniques

We registered a domain name and deployed an ADNS for this domain

We then used 100 PlanetLab nodes as origins and randomly probed the IP address space for hostnmaes within our domain

By observing the queries that arrive at our ADNS we collect the IP addresses willing to handle our probes (ODNSes)

The IP address from which the queries ultimately arrive at our ADNS illuminate the set of RDNSes

SInce the ADNS has the addresses of both the RDNS and ODNS we can associate FDNSes with the RDNSes used. So we can get responses from an RDNS that will not respond directly to probing by indirectly probing via the FDNS

