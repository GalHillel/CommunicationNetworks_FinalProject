import asyncio
import struct
import socket
from scapy.layers.dns import DNS, DNSQR, DNSRR

# Extract the domain name from the DNS request and craft a DNS response


def handleRequest(request):
    domain = request[DNSQR].qname.decode('utf-8')
    res = DNS(id=request[DNS].id, qr=1, qd=request[DNSQR], an=DNSRR(
        rrname=request[DNSQR].qname, ttl=10, rdata='127.0.0.1'))
    return res

# Handle incoming DNS requests.
# It takes a client socket and address as input,
# receives a DNS request packet from the socket,
# passes the request to handleRequest to generate a response packet,
# and sends the response back to the client socket


async def handleClient(clientSock, clientAddr):
    data, addr = await clientSock.recvfrom(4096)
    request = DNS(data)
    res = handleRequest(request)
    resData = bytes(res)
    await clientSock.sendto(resData, clientAddr)

# Creates a RUDP socket and binds it to port 99
# Enters an infinite loop to listen for incoming DNS requests


async def runServer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RDM)
    sock.bind(('127.0.0.1', 99))
    while True:
        clientSock, clientAddr = await asyncio.get_event_loop().sock_recvfrom(sock, 4096)
        asyncio.create_task(handleClient(clientSock, clientAddr))

    async def main():
        await runServer()

    if __name__ == '__main__':
        asyncio.run(main())