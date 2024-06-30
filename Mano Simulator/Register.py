class Register:
    def __init__(self, name : str, size: int = 16, value: str = "0b0") -> None:
        self.name = name
        self.size = size
        self.value = value
        
        
        
    def write(self, value , len : int):
        if len > self.size:
            raise ValueError("Length of value is too long")
        
        if len == self.size:
            self.value = str(value)
        else:
            v = '0' * (self.size-len)
            v += value[2:]
            self.value = '0b' + v
            
            
    def read(self) -> str:
        return self.value
    
    
    def get_name(self) -> str:
        return self.name
    
    def get_size(self) -> int:
        return self.size
    
    def clear(self) -> None:
        self.value = '0b' + '0' * self.size
        
        