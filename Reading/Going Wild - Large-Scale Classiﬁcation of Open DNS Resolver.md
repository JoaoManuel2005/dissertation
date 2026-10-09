## Scanning setup

Weekly internet-wide scans in IPv4 for more than 1 year to enumerate responsive DNS resolvers

Used efficient scanning practices suggested by Drumeric et al. :
- Durumeric, Z., Wustrow, E., and Halderman, J. A. ZMap: Fast Internet-Wide Scanning and its Security Applications. In USENIX Security Symposium (2013)

Sent a single DNS A lookup request for a specific domain to each IP address in IPV4 exclusing well-known private and unallocate network ranges

Requests are specifically crafted and include random domain prefixes to avoid cahcing and hex-formatted IP address of the target host in the form `prefix.hex-ip.domain.edu` which allows us to obtain the IP address of the target host to which the request was send by inspecting the DNS response

Created a blacklist