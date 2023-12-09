import Pkt
import Utils
import Msg


class EntityB:
    def __init__(self, sim):
        self.expecting_bit = 0
        self.utils = Utils(sim)

    def input(self, packet):
        if packet.seqnum != self.expecting_bit or self.utils.pkt_is_corrupt(packet):
            p = Pkt(0, 1 - self.expecting_bit, 0, packet.payload)
            self.utils.pkt_insert_checksum(p)
            self.utils.to_layer3(self, p)
        else:
            self.utils.to_layer5(self, Msg(packet.payload))
            # Ack.
            p = Pkt(0, self.expecting_bit, 0, packet.payload)
            self.utils.pkt_insert_checksum(p)
            self.utils.to_layer3(self, p)

            self.expecting_bit = 1 - self.expecting_bit

    # Called when B's timer goes off.
    def timer_interrupt(self):
        pass