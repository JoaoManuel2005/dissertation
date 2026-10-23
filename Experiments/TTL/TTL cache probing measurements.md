# TTL cache probing measurements

I first ran 
```bash
resolvectl status
```
to find my local resolver's IP address

I got:
![[Pasted image 20261022160117.png]]

So my local resolver is at `194.168.4.100`

## Querying my local resolver

Then I ran the following script:
```Python
import dns.message
import dns.query
import dns.flags
import time

def check_resolver_ttl(resolver_ip):
    domain = dns.name.from_text('.')
    q = dns.message.make_query(domain, dns.rdatatype.NS)
    q.flags &= ~dns.flags.RD
    
    response = dns.query.udp(q, resolver_ip, timeout=3)
    
    print(f"Response Rcode: {response.rcode()}")
    print(f"Answer section length: {len(response.answer)}")
    print(f"Authority section length: {len(response.authority)}")
    print(f"Additional section length: {len(response.additional)}")
    
    for section_name, section in [("Answer", response.answer), ("Authority", response.authority), ("Additional", response.additional)]:
        for rrset in section:
            for rr in rrset:
                print(f"[{section_name}] {rrset.name} | Type: {rr.rdtype} | TTL: {rrset.ttl}")

target_resolver = "194.168.4.100"
for i in range(3):
    print(f"\n--- Query {i+1} ---")
    try:
        check_resolver_ttl(target_resolver)
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(3)

```

This line 
```Python
    domain = dns.name.from_text('.')
```
makes the query for the root zone

This line
```Python
    q.flags &= ~dns.flags.RD
```
sets the RD flag to 0

This line
```Python
    q = dns.message.make_query(domain, dns.rdatatype.NS)
```
makes the query for a NS record. So this should return the resource records that point to the 13 sets of root name servers:

It works but from the TTL we can see that my local resolver is not running a hyperlocal root since the TTL decays between queries:
![[Pasted image 20261022160639.png|566]]


## Querying 8.8.8.8 and 1.1.1.1

Google did not answer the query:
![[Pasted image 20261022184132.png]]

This is probably because of configs to stop cache snooping. Since we set the RD=0 flag, the query got rejected

Cloudflare answered:
![[Pasted image 20261022184243.png]]

but it did not include glue records in the response. The TTL decay is also inconsistent compared to the answers from my local resolver. This is because Cloudflare is running a globally distributed Anycast network and my queries must have hit different nodes 


