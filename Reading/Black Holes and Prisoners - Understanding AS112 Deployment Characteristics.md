# Measurement techniques

RIPE Atlas

Sent non-recursive queries directly from probes to nameservers, allowing distance and response time analysis between probes and sites

We used recursive resolvers, not DNS forwarders, to ensure they queried AS112 directly and only used IPv4 resolvers as Censys does not conduct comprehensive IPv6 scans

Analysed responses to determine site location with city-level granularity. In some non-recursive RIPE Atlas responses the geolocation violates speed-of-light constraints but these were not excluded

No distinguishment made by NSID as some operators use different NSIDs for different instances in the same site

