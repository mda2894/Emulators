import time

class Clock:
    def __init__(self, frequency):
        self.frequency = frequency
        self.cycle_time = 1 / frequency

        self.start_time = 0

    def start(self):
        self.start_time = time.perf_counter()

    def reset(self):
        self.start_time = time.perf_counter()
    
    def wait(self, cycles):
        expected_time = cycles * self.cycle_time
        elapsed_time = time.perf_counter() - self.start_time
        
        time.sleep(expected_time - elapsed_time)

        self.reset()

    def pulse(self):
        self.wait(1)