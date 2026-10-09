
# Measurements

DNS cache probing infers whether a resoruce record (RR) is present in the resolvers cache

The most common method to do this is to perform DNS queries with the recursion desired (RD) flag set to 0, which resolvers answer to from their caches alone. The answers TTL is then used to infer when the resolver cached the RR and thus when the domain was last queried

This allows people to perform DNS cache snooping

Most DNS resolvers nowadays now dont respond to queries from outside their network so the researchers in this paper developed a tool called `dmap` that lets them probe resolvers through fowarders on ISP networks

