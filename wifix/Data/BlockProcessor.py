import binascii

class BlockProcessor(object):
    def __init__(self, decorator=None):
        self.decorator = decorator

    def process(self, message, block_size=4):
        blocks = self._get_blocks(message, block_size)

        for i in range(0, len(blocks)):
            yield self.decorator(blocks[i], len(blocks), i+1) if self.decorator else blocks[i]

    def _get_blocks(self, data, block_size):
        blocks = []

        for i in range(0, len(data), block_size):
            blocks.append(binascii.hexlify(data[i:i+block_size]))

        return blocks
