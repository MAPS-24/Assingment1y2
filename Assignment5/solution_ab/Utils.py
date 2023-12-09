from binascii import crc32


class Utils:
    def __init__(self, sim):
        self.sim = sim

    def start_timer(self, calling_entity, increment):
        self.sim.start_timer(calling_entity, increment)

    def stop_timer(self, calling_entity):
        self.sim.stop_timer(calling_entity)

    def to_layer3(self, calling_entity, packet):
        self.sim.to_layer3(calling_entity, packet)

    def to_layer5(self, calling_entity, message):
        self.sim.to_layer5(calling_entity, message)

    def get_time(self, calling_entity):
        return self.sim.get_time(calling_entity)

    def pkt_compute_checksum(self, packet):
        crc = 0
        crc = crc32(packet.seqnum.to_bytes(4, byteorder='big'), crc)
        crc = crc32(packet.acknum.to_bytes(4, byteorder='big'), crc)
        crc = crc32(packet.payload, crc)
        return crc

    def pkt_insert_checksum(self, packet):
        packet.checksum = self.pkt_compute_checksum(packet)

    def pkt_is_corrupt(self, packet):
        return self.pkt_compute_checksum(packet) != packet.checksum