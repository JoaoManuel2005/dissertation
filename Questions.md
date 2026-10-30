
- How many DNS resolvers currently have a locally served root zone deployed?
	- Probably the best one and most measurable one

Prioritization besides first?

- Is the root zone data served by these hyperlocal resolvers up-to-date?
	- Not sure how to define up-to-date? Could be that they keep serving data whose root zone file TTL has expire

- Does a locally served root zone measurably improve latency for negative responses compared to positive responses?



- Does the deployment of a local DNS root negatively affect other users of the DNS?
- To what extent does hyperlocal root deployment improve privacy?