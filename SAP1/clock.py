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
    
    def pulse(self, cycles = 1):
        expected_time = cycles * self.cycle_time
        elapsed_time = time.perf_counter() - self.start_time
        
        if expected_time - elapsed_time > 0:
            time.sleep(expected_time - elapsed_time)

        self.reset()
