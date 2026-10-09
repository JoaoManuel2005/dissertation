Sources: 
- Addressing the challenges of modern DNS a comprehensive tutorial https://www.hesselman.net/publicaties/Addressing-the-challenges-of-modern-DNS-published.pdf
- https://support.dnsimple.com/articles/empty-non-terminals/

# Addressing the challenges of modern DNS a comprehensive tutorial

In the early DNS, every site connected to the network contained a file called HOSTS.TXT proiding a mapping from names to network addresses

But keeping separate copies of this file synchronized for a growing network was tricky

## Domain names

The central concept in the DNS is the domain name. A domain name is a structured ASCII character string. Domain names are built up from labels separated by dots

![[Pasted image 20261006090342.png]]

### Labels

Domain names are composed of labels. Labels are a maximum of 63 characters long, A-Z, a-z, 0-9 and hyphens. Labels are case insensitive

In DNS messages, labels are encoded using a single unsigned byte indicating the length of the label, followed by the 8-bit ASCII characters for the label text

### Root label

The root label terminates a domain name, being represented by an empty label

Sometimes the root label is indicated by a single dot at the end of the name but the dot is often omitted

In DNS messages, the root label is represented as a single byte value set to 0 x 00 which indicates the top of the DNS hierarchy

### Hostname

Refers to left-most label of a domain name. But it is ambiguous as it sometimes means the whole domain name

### Fully Qualified Domain Name (FQDN)

Means the whole domain name, i.e. all labels, including the root label

### {cc | g}TLD

TLD is top-level domain is the label directly below the root in the DNS hierarchy

ccTLDs refer to country codes like .uk

gTLDs are genereric like .org


## DNS hierarchy

The DNS has a hierarchical organization shaped like an inverted tree
![[Pasted image 20261006090733.png]]

At the top of the tree is the root of the DNS managed by ICANN

ICANN delegates responsibility for the maintenance of top-level domains to registries 

Some registries divide the namespace under their control into separate branches (public suffixes), e.g. the .uk ccTLD has .co.uk for commercial domains and .ac.uk for academic domains

Next are second-level domains which generally belong to people or organizations and below are third-level and further levels. There is no formal convention for how this part of the namespace is organized, although there are common practices, e.g. a www to indicate a World Wide Web service


## DNS message format

All messages use the same format, with certain fields filled, depending on the type:
![[Pasted image 20261006091754.png]]

The format of the header is as follows:
![[Pasted image 20261006092129.png]]

Each of the 4 sections after the header in a DNS message is filled with resource records. In a DNS query only the question and sometimes the additional section contain information. In a DNS response all 4 sections may contain information

In general each of the four sections has the following semantics:
![[Pasted image 20261006092343.png]]

The Question constains the question in a DNS query (generally the name and type queried for)

The Answer contains the resource records that form the response to the question

The Authority contains resource records pointing to authorities (name servers) for the queried name

The Additional contains additional resource records pertaining to aspects of a DNS message, e.g. glue records

### Typical DNS message exchange

In a typical exchange (UDP):
1. Client sends query
	- Client fills in question section of message
	- FIlls in name, query type and query class
	- Sets QR flag to 0 to indicate message is a query
	- Optionally sets RD flag to 1 if it wants server to perform DNS recursion on its behalf
2. Server sends response
	- Server copies question section into response
	- Fills other sections depending on whether it was able to answer the request
3. (Optional) TCP fallback
	- If the server cannot fit a full response into a single message, it will set the TC flag in the response over UDP
	- This tells the client to rety over TCP to get the full response

## DNS record types

![[Pasted image 20261008103334.png]]

## DNS zones

Data for domains in the DNS is organizd into zones

DNS zones contain resource records under a certain name in the DNS hierarchy

Zones are represented using ASCII text in zone files, e.g. for example.com:
![[Pasted image 20261008103945.png]]

`$ORIGIN` declares that all names are relative example.com so line 6 means `www.example.com`

Lines 2-5 show records for apex-records, signified using `@` and point to the origin of the zone (example.com)

RRsets or resource record sets are all resource records of a certain class and type for a certain name, e.g. lines 4-5 are an RRset of all NS records for example.com

Line 6 shows how a CNAME record is used to create an alias from `www.example.com` to the apex records of `example.com`

Lines 7-8 show a delegation of a subdomain called `sub.example.com` to be managed by the two authoritative name servers specified

Line 9 shows a resource record consisting of two labels. A DNS zone can contian multiple label levels under a delegation point. THe zone not only contains records for `example.com` but also for `ipsum.example.com`. Because the subdomain ipsum is not delegated to another nameserer and because there are no recors in the example zone for ipsum, it becomes empty non-terminal

Line 10 shows that DNS supports wildcards. DNS servers will only return a wildcard if the queried record does not explicitly exist

### Empty non-terminal

![[Pasted image 20261008105332.png]]
![[Pasted image 20261008105341.png]]
 
 in this zone both `network.example.com` and `retails.network.example.com` are empty non-terminals. They have no records themselves but exist because of srv1 and srv2 records beneath them

This is because of the DNS tree structure which causes intermediate domain names to exist only because they are paths to deeper names but dont have records of their own


## Authoritative name servers

Authoritative name servers are authority for a domain. Authority for a domain is delegated to an authoritative name server in the parent zone of that domain using NS records. There is a delegation chain from the root which delegates to a TLD, then to a second-level domain and so on

If an authoritative name servers responds to a query for a name for which it is auhoritative it indicates this in the response by setting the AA flag

## DNS resolution

This is the process of mapping a domain name to a value contained in the DNS

Most clients start by calling the OS which typically has a stub resolver (a resolver that cant perform recursion). Instead a stub resolver sends a query to a recursive caching name servers, often called a resolver

Resolvers perform DNS recursion and cache results:
1. Resolver sends query to authoritative name server for root A record
	- When a resolver first starts up it forms a root priming query
		- Sends a query to one of the known 13 root name servers to request a set of authoritative name servers for the root (NS query)
		- Primes its cache with records on authoritative name servers for the root
	- A request for example.com will be replied with a list of authoritatibve name servers for the .com TLD as the root name servers not authoritative for example.com
2. Resolve address for .com authoritative servers
	- A resolver with an empty cache will first have to perform a separate recursion process to resolve these addresses, unless the root name sever includes the addresses for the .com authoritative servers in the additional section
3. Query to a .com authoritative name server for A record for `www.example.com`
	- The .com name servers are not authoritative for this so so delegate the response to one of the example.com authoritative name servers
4. Resolve addresses for example.com authoritative name servers
5. Query an exaple.com authoritative name server for the A record
6. Respond to client and cache

## Glue records

Consider the delegation for google.com
![[Pasted image 20261008111850.png]]

A resolver with an empty cache cant answer for google.com without knowing the addresses of one the four name servers but to know these it must know the address for google.com

To remedy this circular dependency, the .com zone includes glue records with the A and AAAA records for the four Google name servers. If a .com authoritative name servers returns a referral for google.com it includes these glue records in the additional section of the DNS response


# DNS measurements

## Passive

DNS traffic is typically unencrypted enabling passive observation directly at the clinet, resolver, authoritative name server or on the path betweeen them

Placing a measurement sensor at the client directly limits us to only that clients DNS traffic

Placing a sensor at a recursive resolver allows us to see traffic of potentially millions of clients. Clients however may configure multiple resolvers so observing just one resolver may not give us a complete picture of a clients traffic

Placing a sensor on the path between a resolver and the authoritative name servers captures all DNS exchanges that are the result of cache misses. This collects the data for all names that clients of a resolver queried without identifying specific clients, protecting their privacy. This traffic is not completely devoid of privacy risks. Since this trafic is the result of cache misses, these may be user mistakes which reveal information about the user

Sensor can also be placed on the authoritative nameservers. But a zone may be distributed across many servers and nameservers only see requests for non-cached requests

tcpdump can be used for measurements


## Active

The basis of an active DNS measurement is a list of domains which need to be measured, typically from TLD zone files

![[Pasted image 20261008160708.png]]

ZDNS can be used to actively measure the DNS

Active DNS measurement projects:
- OpenINTEL
- Active DNS Project
- Netray

Active DNS measurements have limited privacy impacts as the traffic is generated by the researcher

Actively collected DNS data is often confidential with operators of TLDs often considering the contents of their DNS commercially sensitive and requiring a contract for data access

Passive measurements observr information resulting from real interest by real clients and thus better represent real user activity

In passive measurements there is no control over the frequency at which the same DNS query is observed as this entirely depends on client and caching behaviour. This makes active DNS more suitable for longitudinal studies where it is important that there are regular measurement results whereas passive DNS is more suitable for measurements to gauge the popularity of names and to identify threats

DNSDB is a good source of passively collecteddata