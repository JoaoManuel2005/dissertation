The previous approach I discussed would fail because just looking for the root NS record and a static TTL inst actually enough to separate a true hyperlocal root from standard root hints or cache entries. 

To resolve this ambiguity I thought we could look at the AA flag. "Authoritative Answer"

With RD=0, the resolver is told to only use its local information. If it responds with local information with AA=1 it means it is the authoritative nameserver for that resource. 

But this is also not true.

Section 2 "Requirements" of RFC 8806 explicitly states that:
"The authoritative root service MUST only respond to queries from the same host."

In Section 3 "Operation of the Root Zone on the Local Server" the second step for setting up the hyperlocal root is:
"Start the authoritative service for the root zone in a manner that prevents any system other than a recursive resolver on the same host from accessing it."

So the root service is only available to one machine, not even by other devices on a local network, and so obviously not by the external internet. It would only be avaialable to the local resolver daemon. 

Lets say we are within a network with a hyperlocal root. We send a DNS request to our recursive resolver. The resolver would talk to its own internal local root server instance available on loopback to get the root zone. Then the resolver completes the rest of the query and answers the client. 

So we can only rely on external infromation from it such as TTL. I can think of 2 options:
1. Send a query for an un-cached TLD
	- But we cant possibly know what is cached or not 
	- We could flood a resolver with queries to clean up its cache but this is wasteful and probably illegal/unethical
2. Send a query for a non-existent TLD
	- Theoretically, if we query a non-existent TLD, a normal resolver would have to to the real global root servers to get a NXDOMAIN response but a hyperlocal root would answer with a NXDOMAIN with a much lower TTL from its local zone copy
	- Unfortunately Im not sure this would work 100% of the time either because of RFC 8198. Using cached DNSSEC records from the root zone, a normal resolver could still answer instantly without querying a global root zone as it could use NSEC or NSEC3 records to cryptographically prove that a TLD does not exist. 

RFC8198:
"""
The validating resolver needs to check the existence of an NSEC RR matching/covering the source of synthesis and an NSEC RR covering the query name.

If denial of existence can be determined according to the rules set out in Section 5.4 of [RFC4035], using NSEC records in the cache, then the resolver can immediately return an NXDOMAIN or NODATA (as appropriate) response.
"""

Section 3.1 of RFC 4033 states that:
""Chains of NSEC records explicitly describe the gaps, or 'empty space', between domain names in a zone... The claim that a name does not exist is signed by verifying that the name in question falls within one of the gaps described by an NSEC record.""

Section 4.1 of RFC 4034 states that:
""The Next Domain Name field lists the next owner name of a character-string-sorted list of all the owner names in the zone... This creates a linked list of all the names in the zone, which allows for authenticating the non-existence of a name.""

This means these NSEC records each stand for a gap between TLD names. A simplistic view could assume this is alphabetical, e.g. the first NSEC records protects the gaps between .a and .b and so forth

There are 1437 TLDs, meaning there are 1437 distinct NSEC gaps spanning the entire root zone. It is statistically unlikely that a nameserver has all of the NSEC records for all these gaps cached. So we could send 1437 malformed queries for unexisting TLDs, one in each gap to a server. If it always responds with 0 or very low latency, it is very likely that this is a hyperlocal root. If it responds with a zig-zag pattern of latency, meaning some are cached, some arent, then it is normal server. 

1500 queries is a bit DDoSy, so we could do 26, for each letter of the alphabet. Or 200. Whatever is deemed "ethical"

In reality, this simplistic view is complicated by NSEC3 records which obfuscate the plain-text alphabetical boundaries of the gaps. This is done with a hash.  "The NSEC3 record is like an NSEC record, but, rather than a signed gap of domain names for which there are no answers to the question, NSEC3 provides a signed gap of hashes of domain names. This was intended to prevent zone enumeration." (https://www.cloudflare.com/dns/dnssec/dnssec-complexities-and-considerations/)

So if we just fired 26 queries, it is possible they all hashed to be within the same gap and our test is useless. But instead we just use a script to generate 26 or 200 or whatever strings whose hashes are guaranteed to be spread evenly across the hexadecimal spectrum. We can grab the live "salt" that the root zone is currently using to hash its names by querying the root parameters

This is fake data for demonstration purposes but this is the expected output:
![[Pasted image 20261030130118.png]]


This still doesn't solve:
- How to find resolvers?
- Where to probe them from?
- How many to probe?
- For how long to run experiments?

But this weeks research has brought us closer to answers to these. These experiments will not be possible from the external internet, simply because of the nature of hyperlocal root implementations. 

We should use a similar methodology as "Cache Me Outside":

1. Scanning IPv4 space for DNS resolvers
	1. We extract the Censys DNS scan data
	2. We filter out any IPs that did not respond correctly
	3. We exclude shared DNS services, e.g. 8.8.8.8

2. We use RIPE Atlas to probe resolvers
	1. We select probes in the same network as resolvers we found from Censys


Im still very unsure of how this works exactly, my understanding of local networks vs whole internet is still very limited


Possible next steps:
1. Perform this Censys passive scan and see if i can find probes that can query resolvers
2. Setup a local root on my machine to see if my methodology holds true. I would compare my local root results with probing my ISPs resolver and we should see a flat line vs zig-zag