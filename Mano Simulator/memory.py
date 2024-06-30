from atexit import register
import imp
from math import log2
from Register import Register


class memory:
    def __init__(self, name : str, size : int = 1024, word_width : int = 16) -> None:
        self.name = name
        self.size = size
        self.word_width = word_width
        self.address_bits = log2(self.size)
        
        self.memory = [Register("reg" + str(i), word_width) for i in range(self.size)]
        
        
    def write(self, address : str, value : str, len_ : int) -> None:
        if len(address[2:]) != self.address_bits:
            raise ValueError("address is not in range.")
        
        self.memory[int(address[2:], 2)].write(value,len_)
        
        
    def read(self, address) -> str:
        if len(address[2:]) != self.address_bits:
            raise ValueError("address is not in range.")
        
        return self.memory[int(address[2:], 2)].read()        
        
    def clear(self):
        for i in range(self.size):
            self.memory[i].clear()
    