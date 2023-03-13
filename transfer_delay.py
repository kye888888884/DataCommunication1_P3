import time

RATE = 1 # 1 RATE means sending 1 amount of data per frame.

class Packet:
    def __init__(self, size:int, is_full:bool=False, id:int=0) -> None:
        self.size = size
        self.data = size if is_full else 0
        self.completed = is_full
        self.id = id
    
    def is_empty(self) -> bool:
        return self.data == 0

    def is_full(self) -> bool:
        return self.data == self.size
    
    def send(self) -> None:
        self.data -= RATE
        if self.data <= 0:
            self.data = 0

    def take(self) -> None:
        self.data += RATE
        if self.data >= self.size:
            self.data = self.size
            
class Router:
    def __init__(self, next=None) -> None:
        self.packets = []
        self.next: Router = next

    def add_packets(self, packets: list[Packet]):
        for packet in packets:
            self.packets.append(packet)
    
    def add_packet(self, packet: Packet):
        self.packets.append(packet)
    
    def send_data(self):
        packet: Packet = self.packets[0]
        if not packet.completed:
            return
        if packet.is_full():
            self.next.add_packet(Packet(packet.size, id=packet.id))
        
        packet.send()
        self.next.take_data(packet.id)
        if packet.is_empty():
            self.packets.pop(0)
            self.next.take_complete(packet.id)
        
    def take_data(self, id:int):
        packet: Packet
        for packet in self.packets:
            if packet.id is id:
                packet.take()
    
    def take_complete(self, id:int):
        packet: Packet
        for packet in self.packets:
            if packet.id is id:
                packet.completed = True

    def run(self):
        if len(self.packets) == 0 or self.next is None:
            return
        self.send_data()
    
    def print(self):
        s = ''
        packet: Packet
        for packet in self.packets:
            s += str(packet.data) + '/'
        s = s[:-1]
        print(s)
    
    def get_data(self, id:int=0) -> int:
        if len(self.packets) == 0:
            return 0
        packet = [p for p in self.packets if p.id == id]
        if len(packet) == 0:
            return 0
        return packet[0].data

# Array of link what you want to test.
links = [1,2,3,4,5]

# Size of packets.
sizes = [2,3,1]

for link_count in links:
    router_count = link_count + 1
    routers = [(Router()) for _ in range(router_count)]

    for idx, router in enumerate(routers):
        if idx == len(routers) - 1:
            continue
        router.next = routers[idx + 1]

    routers[0].add_packets([Packet(size, is_full=True, id=i) for i, size in enumerate(sizes)])

    frame_count = 1

    ## If you want to see progress of transmission of packets, uncomment below.
    # print(f'----------Init----------')
    # for i, router in enumerate(routers):
        # print(f'[router {i}]')
        # router.print()

    while True:
        for router in list(reversed(routers)):
            router.run()
        ## If you want to see progress of transmission of packets, uncomment below.
        # print(f'----------frame {frame_count}----------')
        # for i, router in enumerate(routers):
        #     print(f'[router {i}]')
        #     router.print()
        
        is_end = True
        for router in routers[:-1]:
            if len(router.packets) > 0:
                is_end = False
        
        if is_end:
            print(f'link: {link_count}, packets: {sizes}, delay: {frame_count}')
            break

        frame_count += 1