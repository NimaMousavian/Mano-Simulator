from Register import Register
from memory import memory


class CPU:
    def __init__(self, main_memory_content : dict, microprogram_memory_content : dict) -> None:
        self.main_memory = memory("main_memory", 2048, 16)
        self.microprogram_memory = memory("microporgram_memory", 128, 20)
        self.PC = Register("PC",11,'0b' + bin(100)[2:].zfill(11))
        self.AR = Register("AR", 11,"0b0")
        self.DR = Register("DR",16, "0b0")
        self.AC = Register("AC",16,"0b0")
        self.CAR = Register("CAR",7,"0b" + bin(64)[2:].zfill(7))
        self.SBR = Register("SBR",7,"0b0")
        
        self.condition = False
        self.fetch_flag = False
        self.halt_flag = False
        
        self.main_memory_content = main_memory_content
        self.microprogram_memory_content = microprogram_memory_content
        # write content to main memory
        for line in self.main_memory_content.keys():
            addr = "0b" + bin(line)[2:].zfill(11)
            self.main_memory.write(addr,"0b" + self.main_memory_content[line],16)
            
        # write content to micro program memory
        for line in self.microprogram_memory_content.keys():
            addr = "0b" + bin(line)[2:].zfill(7)
            self.microprogram_memory.write(addr,"0b" + self.microprogram_memory_content[line],20)
        
        
    def microexecute(self) -> None:
        
        microinstruction = self.microprogram_memory.read(self.CAR.read())[2:]
        self.f1 = microinstruction[:3]
        self.f2 = microinstruction[3:6]
        self.f3 = microinstruction[6:9]
        self.cd = microinstruction[9:11]
        self.br = microinstruction[11:13]
        self.ad = microinstruction[13:]
        
        if self.f1 == '000':
            self.NOP()
        elif self.f1 == '001':
            self.ADD()
        elif self.f1 == '010':
            self.CLRAC()
        elif self.f1 == '011':
            self.INCAC()
        elif self.f1 == '100':
            self.DRTAC()
        elif self.f1 == '101':
            self.DRTAR()
        elif self.f1 == '110':
            self.PCTAR()
        elif self.f1 == '111':
            self.WRITE()

        if self.f2 == '000':
            self.NOP()
        elif self.f2 == '001':
            self.SUB()
        elif self.f2 == '010':
            self.OR()
        elif self.f2 == '011':
            self.AND()
        elif self.f2 == '100':
            self.READ()
        elif self.f2 == '101':
            self.ACTDR()
        elif self.f2 == '110':
            self.INCDR()
        elif self.f2 == '111':
            self.PCTDR()
        
        if self.f3 == '000':
            self.NOP()
        elif self.f3 == '001':
            self.XOR()
        elif self.f3 == '010':
            self.COM()
        elif self.f3 == '011':
            self.SHL()
        elif self.f3 == '100':
            self.SHR()
        elif self.f3 == '101':
            self.INCPC()
        elif self.f3 == '110':
            self.ARTPC()
        elif self.f3 == '111':
            self.HLT()
        
        if self.cd == '00':
            self.condition_U()
        elif self.cd == '01':
            self.condition_I()
        elif self.cd == '10':
            self.condition_S()
        elif self.cd == '11':
            self.condition_Z()
        
        if self.br == '00':
            self.JMP()
        elif self.br == '01':
            self.CALL()
        elif self.br == '10':
            self.RET()
        elif self.br == '11':
            self.MAP()
            
            
        if self.CAR.read() == '0b' + bin(64)[2:].zfill(7):
            self.fetch_flag = True
        else:
            self.fetch_flag = False
            
            
    def execute(self):
        self.fetch_flag = False
        while not self.fetch_flag and not self.halt_flag:
            self.microexecute()
        if self.halt_flag:
            print("program finished")


    def run(self):
        while not self.halt_flag:
            self.execute()
            
            
    def NOP(self):
        pass
    
    def ADD(self):
        result = int(self.AC.read()[2:], 2) + int(self.DR.read()[2:], 2)
        result = '0b' + bin(result)[2:].zfill(16)
        self.AC.write(result,16)
        
    def CLRAC(self):
        self.AC.clear()
        
    def INCAC(self):
        result = int(self.AC.read()[2:], 2) + 1
        result = '0b' + bin(result)[2:].zfill(16)
        self.AC.write(result,16)
        
    def DRTAC(self):
        self.AC.write(self.DR.read(),16)
        
    def DRTAR(self):
        result = self.DR.read()[7:]
        self.AR.write("0b" + self.DR.read()[7:],11)
        
    def PCTAR(self):
        self.AR.write(self.PC.read(),11)
        
    def WRITE(self):
        self.main_memory.write(self.AR.read(),self.DR.read(),16)
        
    def SUB(self):
        result = int(self.AC.read()[2:], 2) - int(self.DR.read()[2:], 2)
        result = '0b' + bin(result)[2:].zfill(16)
        self.AC.write(result,16)
        
    def OR(self):
        result = int(self.AC.read()[2:], 2) | int(self.DR.read()[2:], 2)
        result = '0b' + bin(result)[2:].zfill(16)
        self.AC.write(result,16)
        
    def AND(self):
        result = int(self.AC.read()[2:], 2) & int(self.DR.read()[2:], 2)
        result = '0b' + bin(result)[2:].zfill(16)
        self.AC.write(result,16)
        
    def READ(self):
        self.DR.write(self.main_memory.read(self.AR.read()), 16)
        
    def ACTDR(self):
        self.DR.write(self.AC.read(), 16)
        
    def INCDR(self):
        result = int(self.DR.read()[2:], 2) + 1
        result = '0b' + bin(result)[2:].zfill(16)
        self.DR.write(result,16)
        
    def PCTDR(self):
        self.DR.write(self.PC.read(),11)
        
    def XOR(self):
        result = int(self.AC.read()[2:], 2) ^ int(self.DR.read()[2:], 2)
        result = '0b' + bin(result)[2:].zfill(16)
        self.AC.write(result,16)
        
    def COM(self):
        result = int(self.AC.read()[2:], 2) ^ int('1' * 16, 2)
        result = '0b' + bin(result)[2:].zfill(16)
        self.AC.write(result,16)
        
    def SHL(self):
        result = self.AC.read()[2:]
        c = result[0]
        result = "0b" + result[1:] + c
        self.AC.write(result,16)
        
    def SHR(self):
        result = self.AC.read()[2:]
        c = result[-1]
        result = "0b" + c + result[:-1]
        self.AC.write(result,16)
            
    def INCPC(self):
        result = int(self.PC.read()[2:], 2) + 1
        result = '0b' + bin(result)[2:].zfill(11)
        self.PC.write(result,11)
        
    def ARTPC(self):
        self.PC.write(self.AR.read(),11)
        
    def HLT(self):
        self.halt_flag = True
        
        
    def condition_U(self):
        self.condition = True
        
    def condition_I(self):
        if self.DR.read()[2] == '1':
            self.condition = True
        else:
            self.condition = False
            
    def condition_S(self):
        if self.AC.read()[2] == '1':
            self.condition = True
        else:
            self.condition = False
            
    def condition_Z(self):
        if self.AC.read() == '0b' + '0' * 16:
            self.condition = True
        else:
            self.condition = False
            
            
            
    def JMP(self):
        if self.condition:
            self.CAR.write('0b' + self.ad,7)
        else:
            result = int(self.CAR.read()[2:], 2) + 1
            result = '0b' + bin(result)[2:].zfill(7)
            self.CAR.write(result,7)
            
    def CALL(self):
        if self.condition:
            self.CAR.write('0b' + self.ad)
            result = int(self.CAR.read()[2:], 2) + 1
            result = '0b' + bin(result)[2:].zfill(7)
            self.SBR.write(result,7)
        else:
            result = int(self.CAR.read()[2:], 2) + 1
            result = '0b' + bin(result)[2:].zfill(7)
            self.CAR.write(result,7)
            
    def RET(self):
        self.CAR.write(self.SBR.read(),7)
        
    def MAP(self):
        result = "0b0" + self.DR.read()[3:7] + "00"
        self.CAR.write(result,7)
            
        
    def clear(self):
        self.main_memory.clear()
        self.microprogram_memory.clear()
        self.AC.clear()
        self.AR.clear()
        self.DR.clear()
        self.PC.clear()
        self.CAR.clear()
        self.SBR.clear()
        
        
    