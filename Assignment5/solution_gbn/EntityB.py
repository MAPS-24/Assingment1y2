import Utils
import Pkt
import Msg


class EntityB:
    def __init__(self, sim, seqnum_limit):
        self.utils = Utils(sim)

        self.seqnum_limit = seqnum_limit

        self.expected_seqnum = 0
        self.last_acked = seqnum_limit - 1

    def input(self, packet):
        if self.utils.pkt_is_corrupt(packet) or packet.seqnum != self.expected_seqnum:
            p = Pkt(0, self.last_acked, 0, packet.payload)
            self.utils.pkt_insert_checksum(p)
            self.utils.to_layer3(self, p)
        else:
            self.utils.to_layer5(self, Msg(packet.payload))
            p = Pkt(0, self.expected_seqnum, 0, packet.payload)
            self.utils.pkt_insert_checksum(p)
            self.utils.to_layer3(self, p)
            self.last_acked = self.expected_seqnum
            self.expected_seqnum = self.next_expected_seqnum()

    def next_expected_seqnum(self):
        return (self.expected_seqnum + 1) % self.seqnum_limit

    # Called when B's timer goes off.
    def timer_interrupt(self):
        pass