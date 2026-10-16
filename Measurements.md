## Active

### DNS Cache Probing

- To find out if a root zone resource record is being served locally we can use DNS cache probing 
- We can use `dmap` to probe resolvers from the outside through forwarders located on ISP networks
	- According to one of the papers you cant do this from outside the network
- Wesend DNS queries with the recursion desired (RD) flag set to 0, which forces the resolver to answer using only its cache
-  Resolvers with a hyperlocal root will have a non-decaying TTL compared to standard cached responses so we just repeat the query and see if the TTL stays the same


Explanation:
- A standard DNS resolver caches records and continuously counts down their Time-to-Live (TTL) timere. A resolver running a local root zone acts as the authoritative server for that root data so it serve it directly from the local zone file and not a cache, meaning it always return the exact, original maximum TTL value without decrementing it

## Passive

### Passive Measurements and Dataset Querying

- We can conduct passive measurements by deploying sensors on the path between resolvers and authoritative name servers and use `tcpdump` to take measurements. Reesolvers with a hyperlocal root will not have upstream root queries resulting from cache misses


- We could also analyze passively collected datasets, such as the Day-In-The-Life (DITL) 2018 dataset or DNSDB, to identify broad usage patterns and query volumes
- Or we could query Censys to search structured fields derived from application handshakes that may indicate authoritative local root configurations