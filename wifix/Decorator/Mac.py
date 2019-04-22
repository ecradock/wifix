from wifix.Data.FrameEntry import FrameEntry

class Mac(object):
    MAC_DEFAULT_LENGTH = 12

    def __init__(self, prefix="0000"):
        self.prefix = prefix.replace(":", "")

    def split_by_char(self, string, separator=":", every=2):
        return ":".join([string[i:i+every] for i in range(0, len(string), every)])

    def pad_mac(self, remaining):
        return self.split_by_char("{:<012}".format(self.prefix + remaining))

    def decorate_status(self, current, total, checksum="AB"):
        return "{:02x}0F{:02x}".format(current, total)

    def decorate(self, bytestring, total, current):
        stats = {"current":current, "total": total}
        padded = self.pad_mac(bytestring.strip())

        if total > 255:
            position = self.pad_mac("{:02x}".format(current))
        else:
            position = self.pad_mac(self.decorate_status(current, total))

        total = self.pad_mac("{:02x}".format(total))

        return FrameEntry(padded, position, total, stats)
