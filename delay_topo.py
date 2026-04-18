from mininet.topo import Topo
from mininet.link import TCLink

class DelayTopo(Topo):
    def build(self):
        # Add hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')

        # Add switches (DPIDs are assigned sequentially: s1=1, s2=2, etc.)
        s1 = self.addSwitch('s1') 
        s2 = self.addSwitch('s2') # Will act as the Fast Path
        s3 = self.addSwitch('s3') # Will act as the Slow Path
        s4 = self.addSwitch('s4') 

        # Connect h1 to s1
        self.addLink(h1, s1, port1=0, port2=1)

        # Create Path 1 (Fast Path: ~10ms total delay)
        self.addLink(s1, s2, port1=2, port2=1, cls=TCLink, delay='5ms')
        self.addLink(s2, s4, port1=2, port2=1, cls=TCLink, delay='5ms')

        # Create Path 2 (Slow Path: ~100ms total delay)
        self.addLink(s1, s3, port1=3, port2=1, cls=TCLink, delay='50ms')
        self.addLink(s3, s4, port1=2, port2=2, cls=TCLink, delay='50ms')

        # Connect s4 to h2
        self.addLink(s4, h2, port1=3, port2=0)

topos = { 'delaytopo': (lambda: DelayTopo()) }