import threading, time, random, queue

CUSTOMERS = 50
BARBERS = 3
waitingRoom = queue.Queue(maxsize = 15)
ARRIVAL_WAIT = 0.5

def wait():
    time.sleep(ARRIVAL_WAIT * random.random())

class Barber(threading.Thread):
    condition = threading.Condition()
    should_stop = threading.Event()

    def run(self):
        while True:
            with self.condition:
                if waitingRoom.qsize() == 0:
                    print("Barber is sleeping.")
                    self.condition.wait()
                if self.should_stop.is_set():
                    return

                customer = waitingRoom.get()
                print("Barber is waking up.")
            customer.trim()

class Customer(threading.Thread):
    WAIT = 0.05

    def wait(self):
        time.sleep(self.WAIT * random.random())

    def trim(self):
        print("Customer is getting a haircut.")
        self.wait()
        self.serviced.set()

    def run(self):
        self.serviced = threading.Event()
        with Barber.condition:
            Barber.condition.notify(1)

        self.serviced.wait()
        print("Customer is leaving.")
        if waitingRoom.qsize() == 0:
            print("Barber has gone to sleep.")

if __name__ == '__main__':
    allCustomers = []

    for b in range(BARBERS):
        Barber().start()

    for c in range(CUSTOMERS):
        c = Customer()
        allCustomers.append(c)

    for c in allCustomers:
        wait()
        waitingRoom.put(c)
        c.start()
        c.join()

    Barber.should_stop.set()
    print("The shop is now closed.")
