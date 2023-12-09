class Pkt:
    def __init__(self, seqnum, acknum, checksum, payload):
        self.seqnum = seqnum
        self.acknum = acknum
        self.checksum = checksum
        self.payload = payload

    def __str__(self):
        return ('Pkt(seqnum=%s, acknum=%s, checksum=%s, payload=%s)'% (self.seqnum, self.acknum, self.checksum, self.payload))