from scapy.all import Dot11

class Unwrap(object):
    def __init__(self, pkt, prefix="13:37:"):
        self.pkt = pkt
        self.prefix = prefix

    def unwrap_mac(self, mac):
        return mac[len(self.prefix):].replace(':', '')

    def get_data(self):
        return self.unwrap_mac(self.pkt[Dot11].addr1)

    def get_current(self):
        return self.unwrap_mac(self.pkt[Dot11].addr2)

    def get_length(self):
        return self.unwrap_mac(self.pkt[Dot11].addr3)

