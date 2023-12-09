import Utils
import Pkt


class EntityA:
    def __init__(self, sim, trace):
        self.utils = Utils(sim)
        self.trace = trace

        self.OUTPUT = 0
        self.INPUT = 1
        self.TIMER = 2

        self.WAIT_TIME = 10.0

        # State
        self.layer5_msgs = []
        self.bit = 0
        self.sent_pkt = None
        self.handle_event = self.handle_event_wait_for_call

    def output(self, message):
        self.layer5_msgs.append(message)
        self.handle_event(self.OUTPUT)

    def input(self, packet):
        self.handle_event(self.INPUT, packet)

    # Called when A's timer goes off.
    def timer_interrupt(self):
        self.handle_event(self.TIMER)

    def handle_event_wait_for_call(self, e, arg=None):
        if e == self.OUTPUT:
            if not self.layer5_msgs:
                return

            m = self.layer5_msgs.pop(0)
            p = Pkt(self.bit, 0, 0, m.data)

            self.utils.pkt_insert_checksum(p)
            self.utils.to_layer3(self, p)
            self.sent_pkt = p
            self.utils.start_timer(self, self.WAIT_TIME)
            self.handle_event = self.handle_event_wait_for_ack

        elif e == self.INPUT:
            pass

        elif e == self.TIMER:
            if self.trace > 0:
                print('EntityA: ignoring unexpected timeout.')

        else:
            self.unknown_event(e)

    def handle_event_wait_for_ack(self, e, arg=None):
        if e == self.OUTPUT:
            pass

        elif e == self.INPUT:
            p = arg
            if self.utils.pkt_is_corrupt(p) or p.acknum != self.bit:
                return

            self.utils.stop_timer(self)

            self.bit = 1 - self.bit
            self.handle_event = self.handle_event_wait_for_call
            self.handle_event(self.OUTPUT)

        elif e == self.TIMER:
            self.utils.to_layer3(self, self.sent_pkt)
            self.utils.start_timer(self, self.WAIT_TIME)

        else:
            self.unknown_event(e)

    #####

    def self_unknown_event(self, e):
        print(f'EntityA: ignoring unknown event {e}.')
