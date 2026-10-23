import dns.message
import dns.query
import dns.flags
import time

def check_resolver_ttl(resolver_ip):
    domain = dns.name.from_text('.')
    q = dns.message.make_query(domain, dns.rdatatype.NS)
    q.flags &= ~dns.flags.RD  # Ensure Recursion Desired is 0
    
    response = dns.query.udp(q, resolver_ip, timeout=3)
    
    print(f"Response Rcode: {response.rcode()}")
    print(f"Answer section length: {len(response.answer)}")
    print(f"Authority section length: {len(response.authority)}")
    print(f"Additional section length: {len(response.additional)}")
    
    # Print everything found in any section
    for section_name, section in [("Answer", response.answer), ("Authority", response.authority), ("Additional", response.additional)]:
        for rrset in section:
            for rr in rrset:
                print(f"[{section_name}] {rrset.name} | Type: {rr.rdtype} | TTL: {rrset.ttl}")

target_resolver = "1.1.1.1"
for i in range(3):
    print(f"\n--- Attempt {i+1} ---")
    try:
        check_resolver_ttl(target_resolver)
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(3)
