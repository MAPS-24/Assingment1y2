import Utils
import Pkt


class EntityA:
    def __init__(self, sim, seqnum_limit, trace):
        self.WAIT_TIME = 10.0 + 4.0 * seqnum_limit // 2
        self.utils = Utils(sim)
        self.trace = trace

        self.seqnum_limit = seqnum_limit
        self.window_size = seqnum_limit//2

        self.base = 0
        self.layer3_pkts = []
        self.layer5_msgs = []
        self.made_progress = True
        self.n_no_progress = 0

    def output(self, message):
        self.layer5_msgs.append(message)
        self.maybe_output_from_queue()

    def maybe_output_from_queue(self):
        while (self.layer5_msgs
               and len(self.layer3_pkts) < self.window_size):
            m = self.layer5_msgs.pop(0)
            s = self.next_seqnum()
            p = Pkt(s, 0, 0, m.data)
            self.utils.pkt_insert_checksum(p)
            self.layer3_pkts.append(p)
            self.utils.to_layer3(self, p)

            if len(self.layer3_pkts) == 1:
                self.utils.start_timer(self, self.WAIT_TIME)

    def next_seqnum(self):
        return (self.base + len(self.layer3_pkts)) % self.seqnum_limit

    def input(self, packet):
        if self.utils.pkt_is_corrupt(packet):
            return

        i = 0
        while i < len(self.layer3_pkts):
            if self.layer3_pkts[i].seqnum != packet.acknum:
                i += 1
                continue

            self.base += i+1
            self.layer3_pkts = self.layer3_pkts[i+1:]

            if self.trace > 0:
                if self.n_no_progress > 0 and not self.made_progress:
                    print(f'[A:base {self.base}] Finally made some progress!')

            self.made_progress = True
            self.n_no_progress = 0
            self.utils.stop_timer(self)

            if self.layer3_pkts:
                self.utils.start_timer(self, self.WAIT_TIME)

            self.maybe_output_from_queue()
            break

    def timer_interrupt(self):
        if not self.made_progress:
            self.n_no_progress += 1
            if self.trace > 0:
                print(f'[A:base {self.base}] Rats!  Made no progress for {self.n_no_progress} timeouts.')

        self.made_progress = False

        for p in self.layer3_pkts:
            self.utils.to_layer3(self, p)

        self.utils.start_timer(self, self.WAIT_TIME * (self.n_no_progress+1))
