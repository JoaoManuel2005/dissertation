
# On Eliminating Root Nameservers from the DNS

Hyperlocal DNS = DNS root nameservers are eliminated and instead recursive resolvers should use a local copy of the root zone file

95% of traffic at root nameservers is "junk" - could we measure this and repeate this result?

Could we measure the number of recursive resolvers which do not updat their root hints file in a timely fashion?

Measuring root manipulation?

Measure QNAME minimization (QMin) use? (thought this one was particularly cool)

### Things to learn

- I lack a high level understanding of DHCP
- I understand local recursive resolvers but not public ones
- Root hints file
- Zone transfer mechanism
- Resolvers vs forwarders. OS has a forwarder that makes a request to a resolver

### Further reading

- RFC 7706