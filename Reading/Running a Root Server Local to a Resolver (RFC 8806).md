
# Running a Root Server Local to a Resolver (RFC 8806)

Service running on same machine as recursive resolver acts as root zone, eliminates need to reprogram all resolvers

Some resolver software even allows this to happen in the same process, but in different "views"

RFC7706 required the local root to run on the loopback of the host running the resolver

RFC8806 allows a fallback to remote root, and also enforces that only queries from the same host can be answered by the local root

### Root zone sources

Root zone can be retrieved from anywhere as long as it is encrypted with DNSSEC
Root zone can be obtained from ICANN by zone transfer AXFR over TCP from DNS servers

### Further reading

- RFC5936
- RFC7706