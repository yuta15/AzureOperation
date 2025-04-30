from ipaddress import IPv4Network, IPv4Address


i = '192.168.1.0/24'
b = '192.168.1.0/29'
add = '192.168.1.1'
ip = IPv4Network(i)
ipb = IPv4Network(b)

d = IPv4Address(add)
print(d in ip)
print(ip.subnet_of(ipb))