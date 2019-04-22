from scapy.all import (
            sniff,
            Dot11Elt,
            Dot11Beacon
        )
import collections
from Unwrap import Unwrap

class Capture(object):
    def __init__(self, logger, interface=None, ssid=None, message_handler=None):
        self.interface = interface
        self.ssid = ssid
        self.logger = logger
        self.received = {}

    def reset_received(self):
        self.received = {}

    def is_end_of_transmission(self, current):
        return current[0:2] == current[-4:-2]

    def get_ordered_data(self, received):
        od = collections.OrderedDict(sorted(received.items()))
        data = ""

        for k,v in od.iteritems():
            data += ''.join([chr(int(v[i:i+2], 16)) for i in range(0, len(v), 2)])

        return data

    def handle_packet(self, pkt):
        self.logger.debug(pkt.show(dump=True))

        unwrap = Unwrap(pkt, prefix="13:37:")
        self.received[unwrap.get_current()] = unwrap.get_data()
        total = int(unwrap.get_current()[-4:-2], 16)

        if self.is_end_of_transmission(unwrap.get_current()) and len(self.received) >= total:
            data = self.get_ordered_data(self.received)
            received_count = len(data) / 4

            self.logger.debug("Detected end of transmission")
            print data

            self.reset_received()

    def is_accepted(self, pkt):
        return pkt.haslayer(Dot11Beacon) and pkt[Dot11Elt].info == self.ssid

    def run(self):
        sniffkw = {
            "prn": self.handle_packet,
            "lfilter": self.is_accepted,
            "iface": self.interface
        }

        sniff(**sniffkw)
