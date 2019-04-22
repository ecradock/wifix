from scapy.all import ( Dot11,
                        Dot11Beacon,
                        Dot11Elt,
                        RadioTap,
                        sendp )

class FrameDeliveryAgent(object):
    def __init__(self, interface, logger):
        self.interface = interface
        self.logger = logger

    def send(self, ssid, 
            receiver = "ab:cd:ef:12:34:56", 
            sender = "ab:cd:ef:12:34:56", 
            transmitter = "ab:cd:ef:12:34:56"): 

        dot11 = Dot11(type=0, subtype=8, addr1=transmitter,
                addr2=sender, addr3=receiver)
        beacon = Dot11Beacon()
        essid = Dot11Elt(ID="SSID",info=ssid, len=len(ssid))
        frame = RadioTap()/dot11/beacon/essid

        self.logger.debug(frame.show(dump=True))

        sendp(frame, iface=self.interface, verbose=False) 
