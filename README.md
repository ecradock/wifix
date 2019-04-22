# Wifi Exfiltration

Uses MAC addresses to smuggle data across as wifi beacons. Using each occet within the MAC address as a separate byte.

Its purpose at this point is purely to create a challenge within a CTF event.

## Sending a message
```
usage: wifix-send [-h] --ssid SSID [--file FILE] [--message MESSAGE]
                  --interface INTERFACE [--debug] [--prefix PREFIX]
                  [--interval INTERVAL]

optional arguments:
  -h, --help            show this help message and exit
  --ssid SSID, -s SSID  SSID for network
  --file FILE, -f FILE  File to encode as wifi frames
  --message MESSAGE, -m MESSAGE
                        Message to encode as wifi frames
  --interface INTERFACE, -i INTERFACE
                        Network Interface Name
  --debug, -d           Print packets rather than send
  --prefix PREFIX, -p PREFIX
                        The prefix for mac address
  --interval INTERVAL, -t INTERVAL
                        Interval between packet sends
```

### Example usage

```
wifix-send -i wlan0mon -s Broadcast -m "My Secret Message"
```

## Receiving a message
```
usage: wifix-recv [-h] [--interface INTERFACE] [--ssid SSID] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --interface INTERFACE, -i INTERFACE
                        Interface
  --ssid SSID, -s SSID  Wifi SSID
  --debug, -d           Enable verbose output
```

### Example usage

```
wifix-recv -i wlan0mon -s Broadcast
```
