
# Measurements

This paper introduces Censys, public search engine and data processing faciclity backed by data from internet-wide scanning

Supports full-text searches on protocol banners and generates statistical reports on broad usage patterns

IPv4 address space only

https://censys.io

Measurements were made through horizontal application scans of the public IPv4 address space scheduled across a pool of scan workers

1. Perform host discovery scans using ZMap
2. Complete application handshakes with responsive hosts 
3. Derive structured fields from handshakes
4. Process, anotate and save data

Sounds similar to what we want to do

Censys also measured DNS so they have data for this already potentially