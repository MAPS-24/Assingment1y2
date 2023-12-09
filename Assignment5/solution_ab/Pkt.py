class Pkt:
    def __init__(self, seqnum, acknum, checksum, payload):
        self.seqnum = seqnum            # type: integer
        self.acknum = acknum            # type: integer
        self.checksum = checksum        # type: integer
        self.payload = payload          # type: bytes[Msg.MSG_SIZE]

    def __str__(self):
        return ('Pkt(seqnum=%s, acknum=%s, checksum=%s, payload=%s)'
                % (self.seqnum, self.acknum, self.checksum, self.payload))