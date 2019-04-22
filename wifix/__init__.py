import argparse
import sys
import time
import logging

from wifix.Data.BlockProcessor import BlockProcessor
from wifix.Wifi.FrameDeliveryAgent import FrameDeliveryAgent
from wifix.Wifi.Capture import Capture
from wifix.Decorator.Mac import Mac as MacDecorator

def print_same_line(msg):
    print msg
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")

def get_logger(debug):
    logging.basicConfig(format="[%(levelname)s] %(message)s")
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    return logger

def send():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ssid", "-s", help="SSID for network", required=True)
    parser.add_argument("--file", "-f", help="File to encode as wifi frames")
    parser.add_argument("--message", "-m", help="Message to encode as wifi frames", default="Sample message")
    parser.add_argument("--interface", "-i", help="Network Interface Name", required=True)
    parser.add_argument("--debug", "-d", help="Print packets rather than send", action="store_true", default=False)
    parser.add_argument("--prefix", "-p", help="The prefix for mac address", default="13:37")
    parser.add_argument("--interval", "-t", help="Interval between packet sends", default=None, type=float) 

    args = parser.parse_args()
    logger = get_logger(args.debug)

    block_processor = BlockProcessor(MacDecorator(prefix=args.prefix).decorate)
    delivery_agent = FrameDeliveryAgent(args.interface, logger=logger)
    message = args.message

    if args.file:
        with open(args.file, "rb") as fp:
            message = fp.read()

    for entry in block_processor.process(message):
        print_same_line('[STATUS] Sending {} out of {}'.format(entry.stats['current'], entry.stats['total']))

        delivery_agent.send(args.ssid, transmitter=entry.data, sender=entry.current, receiver=entry.total)
        if args.interval:
            time.sleep(args.interval)

    print "[STATUS] Packet delivery complete"


def recv():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interface", "-i", help="Interface")
    parser.add_argument("--ssid", "-s", help="Wifi SSID")
    parser.add_argument("--debug", "-d", help="Enable verbose output", default=False, action="store_true")

    args = parser.parse_args()
    logger = get_logger(args.debug)

    sniffer = Capture(logger=logger, interface=args.interface, ssid=args.ssid)
    sniffer.run()

