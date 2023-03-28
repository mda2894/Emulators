import time

class Clock:
    def __init__(self, frequency):
        self.frequency = frequency
        self.cycle_time = 1 / frequency

        self.start_time = 0
        self.stopped = False


    def reset(self):
        self.stopped = False
        self.start_time = time.perf_counter()


    def stop(self):
        self.stopped = True


    def pulse(self, cycles = 1):
        if not self.stopped:
            expected_time = cycles * self.cycle_time
            elapsed_time = time.perf_counter() - self.start_time
            
            if expected_time > elapsed_time:
                time.sleep(expected_time - elapsed_time)

            self.start_time = time.perf_counter()
