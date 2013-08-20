from multiprocessing.pool import ThreadPool
import time

class MultiThreadIt:

    # Initializes the ThreadPool with the number of processes    
    def __init__(self, proc):
        self.pool = ThreadPool(proc)

    # Performs multithreading and returns the result
    def multiThreadIt(self, func_name, args):
        self.time_start = time.time()
        self.result = self.pool.apply_async(func_name, args)
        self.return_val = self.result.get()
        self.time_end = time.time()
        self.pool.close()
        
        return self.return_val
    
    # Returns the time taken to execute the multithreading block
    def timeTaken(self):
        return self.time_end - self.time_start