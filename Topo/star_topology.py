from mininet.net import Mininet
from mininet.topo import Topo


class StarTopology(Topo):
    def build(self):
        switch = self.addSwitch('s1')

        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')

        self.addLink(host1, switch)
        self.addLink(host2, switch)
        self.addLink(host3, switch)


topo = StarTopology()
net = Mininet(topo)
net.start()

# Configure the web server on one of the hosts
host1 = net.get('h1')
host1.cmd('python -m SimpleHTTPServer 80 &')

# Access the web server from the Mininet virtual machine
mininet_vm_ip = '192.168.0.100'  # Replace with the IP address of your Mininet VM
host1_ip = '10.0.0.1'  # Replace with the IP address of h1
url = f'http://{host1_ip}/'  # URL of the web server
response = net.get('h1').cmd(f'wget -O - {url} > /dev/null')
print(response)

net.stop()
