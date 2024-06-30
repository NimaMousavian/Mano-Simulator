
class program_assembler:
    def __init__(self, assembly_code : list, opcode : dict) -> None:
        self.assembly_code = assembly_code
        self.opcode = opcode
        
        self.labels_dict = {}
        self.values = {}
        
        
    def extract_labels(self):
        line_counter = 0
        l = 1
        
        for line in self.assembly_code:
            if line == []:
                l += 1
                continue
            elif line[0] == 'ORG':
                line_counter = int(line[1])
            
            elif line[0][-1] == ',':
                self.labels_dict[line[0][:-1]] = line_counter
                line_counter += 1
                l += 1
            elif line[0] == 'END':
                break
            else:
                line_counter += 1
                l += 1
                
                
    def extract_values(self):
        op_code = ""
        address = ""
        I = ""
        line_counter = 0
        l = 1
        
        for line in self.assembly_code:
            if line == []:
                l += 1
                continue
            elif line[0] == 'ORG':
                line_counter = int(line[1])
                continue
            
            elif line[0][-1] == ',':
                if line[1] == 'BIN':
                    self.values[self.labels_dict[line[0][:-1]]] = line[2].zfill(16)
                elif line[1] == 'DEC':
                    self.values[self.labels_dict[line[0][:-1]]] = bin(int(line[2]))[2:].zfill(16)
                elif line[1] == 'HEX':
                    self.values[self.labels_dict[line[0][:-1]]] = bin(int(line[2],16))[2:].zfill(16)
                else:
                    if len(line) == 2:
                        if line[1] in self.opcode.keys():
                            op_code = bin(int(self.opcode[line[1]]) // 4)[2:].zfill(4)
                        else:
                            raise Exception(f"instruction not found in microprogram code in line {str(l)}.")
                        address = '0' * 11
                        I = '0'
                    elif len(line) == 3:
                        if line[1] in self.opcode.keys():
                            op_code = bin(int(self.opcode[line[1]]) // 4)[2:].zfill(4)
                        else:
                            raise Exception(f"instruction not found in microprogram code in line {str(l)}.")
                        if line[2] in self.labels_dict.keys():
                            address = bin(self.labels_dict[line[2]])[2:].zfill(11)
                        else:
                            raise Exception(f"address not found in line {str(l)}.")
                        I = '0'
                    elif len(line) == 4:
                        if line[1] in self.opcode.keys():
                            op_code = bin(int(self.opcode[line[1]]) // 4)[2:].zfill(4)
                        else:
                            raise Exception(f"instruction not found in microprogram code in line {str(l)}.")
                        if line[2] in self.labels_dict.keys():
                            address = bin(self.labels_dict[line[2]])[2:].zfill(11)
                        else:
                            raise Exception(f"address not found in line {str(l)}.")
                        if line[3] == 'I':
                            I = '1'
                        else:
                            Exception(f"I not found in line {str(l)}.")
                    self.values[line_counter] = I + op_code + address
            elif line[0] == 'END':
                break
            else:
                if len(line) == 1:
                    if line[0] in self.opcode.keys():
                        op_code = bin(int(self.opcode[line[0]]) // 4)[2:].zfill(4)
                    else:
                        raise Exception(f"instruction not found in microprogram code in line {str(l)}.")
                    address = '0' * 11
                    I = '0'
                elif len(line) == 2:
                    if line[0] in self.opcode.keys():
                         op_code = bin(int(self.opcode[line[0]]) // 4)[2:].zfill(4)
                    else:
                        raise Exception(f"instruction not found in microprogram code in line {str(l)}.")
                    if line[1] in self.labels_dict.keys():
                        address = bin(self.labels_dict[line[1]])[2:].zfill(11)
                    else:
                        raise Exception(f"address not found in line {str(l)}.")
                    I = '0'
                elif len(line) == 3:
                    if line[0] in self.opcode.keys():
                        op_code = bin(int(self.opcode[line[0]]) // 4)[2:].zfill(4)
                    else:
                        raise Exception(f"instruction not found in microprogram code in line {str(l)}.")
                    if line[1] in self.labels_dict.keys():
                        address = bin(self.labels_dict[line[1]])[2:].zfill(11)
                    else:
                        raise Exception(f"address not found in line {str(l)}.")
                    if line[2] == 'I':
                            I = '1'
                    else:
                        Exception(f"I not found in line {str(l)}.")
                self.values[line_counter] = I + op_code + address
            line_counter += 1
            l += 1
            
         
    def assemble(self) -> dict:
        self.extract_labels()
        self.extract_values()
        
        return self.values
        
         
class microprogram_assembler:
    def __init__(self, assembly_code: list) -> None:
        self.assembly_code = assembly_code
        self.labels_dict = {}
        self.value = {}
        self.F1 = {'NOP': '000', 'ADD': '001', 'CLRAC': '010', 'INCAC': '011', 'DRTAC': '100', 'DRTAR': '101', 'PCTAR': '110', 'WRITE': '111'}
        self.F2 = {'NOP': '000', 'SUB': '001', 'OR': '010', 'AND': '011', 'READ': '100', 'ACTDR': '101', 'INCDR': '110', 'PCTDR': '111'}
        self.F3 = {'NOP': '000', 'MUL': '001', 'COM': '010', 'SHL': '011', 'SHR': '100', 'INCPC': '101', 'ARTPC': '110', 'HLT': '111'}
        self.CD = {'U': '00', 'I': '01', 'S': '10', 'Z': '11'}
        self.BR = {'JMP': '00', 'CALL': '01', 'RET': '10', 'MAP': '11'}   


    def extract_labels(self):
        line_counter = 0
        l = 1
        
        for line in self.assembly_code:
            if line == []:
                l += 1
                continue
            elif line[0] == 'ORG':
                line_counter = int(line[1])

            elif line[0][-1] == ':':
                self.labels_dict[line[0][:-1]] = line_counter
                line_counter += 1
                l += 1
            elif line[0] == 'END':
                break
            else:
                line_counter += 1
                l += 1
                
                
    def extract_values(self):
        
        line_counter = 0
        l = 1
        
        for line in self.assembly_code:
            
            f1 = "000"
            f2 = "000"
            f3 = "000"
            cd = "00"
            br = "00"
            ad = "0000000"
            
            if line == []:
                l += 1 
                continue
            elif line[0] == "ORG":
                line_counter = int(line[1])
                l += 1
                continue
            elif line[0][-1] == ":":
                instructions = []
                instructions = line[1].split(',')
                if len(instructions) == 1:
                    if instructions[0] in self.F1.keys():
                        f1 = self.F1[instructions[0]]
                    elif instructions[0] in self.F2.keys():
                        f2 = self.F2[instructions[0]]
                    elif instructions[0] in self.F3.keys():
                        f3 = self.F3[instructions[0]]
                    else:
                        raise Exception(f"instrucion not found in line {str(l)}.")
                elif len(instructions) == 2:
                    if instructions[0] in self.F1.keys() and instructions[1] in self.F2.keys():
                        f1 = self.F1[instructions[0]]
                        f2 = self.F2[instructions[1]]
                    elif instructions[0] in self.F1.keys() and instructions[1] in self.F3.keys():
                        f1 = self.F1[instructions[0]]
                        f3 = self.F3[instructions[1]]
                    elif instructions[0] in self.F2.keys() and instructions[1] in self.F3.keys():
                        f2 = self.F2[instructions[0]]
                        f3 = self.F3[instructions[1]]
                    else:
                        raise Exception(f"instruction not found in line {str(l)}")
                elif len(instructions) == 3:
                    if instructions[0] in self.F1.keys() and instructions[1] in self.F2.keys() and instructions[2] in self.F3.keys():
                        f1 = self.F1[instructions[0]]
                        f2 = self.F2[instructions[1]]
                        f3 = self.F3[instructions[2]]
                    else:
                        raise Exception(f"instruction not found in line {str(l)}")
                
                if line[2] in self.CD.keys():
                    cd = self.CD[line[2]]
                else:
                    raise Exception(f"condition not found in line {str(l)}")
                
                if line[3] in self.BR.keys():
                    br = self.BR[line[3]]
                else: 
                    raise Exception(f"branch not found in line {str(l)}")
                
                
                if len(line) == 4:
                    pass
                elif line[4] == "NEXT":
                    ad = bin(line_counter + 1)[2:].zfill(7)
                elif line[4] in self.labels_dict.keys():
                    ad = bin(self.labels_dict[line[4]])[2:].zfill(7)
                else:
                    raise Exception(f"address not found in line {str(l)}")
                
                self.value[line_counter] = f1 + f2 + f3 + cd + br + ad
                
            elif line[0] == 'END':
                break
            else:
                instructions = []
                instructions = line[0].split(',')
                if len(instructions) == 1:
                    if instructions[0] in self.F1.keys():
                        f1 = self.F1[instructions[0]]
                    elif instructions[0] in self.F2.keys():
                        f2 = self.F2[instructions[0]]
                    elif instructions[0] in self.F3.keys():
                        f3 = self.F3[instructions[0]]
                    else:
                        raise Exception(f"instrucion not found in line {str(l)}.")
                elif len(instructions) == 2:
                    if instructions[0] in self.F1.keys() and instructions[1] in self.F2.keys():
                        f1 = self.F1[instructions[0]]
                        f2 = self.F2[instructions[1]]
                    elif instructions[0] in self.F1.keys() and instructions[1] in self.F3.keys():
                        f1 = self.F1[instructions[0]]
                        f3 = self.F3[instructions[1]]
                    elif instructions[0] in self.F2.keys() and instructions[1] in self.F3.keys():
                        f2 = self.F2[instructions[0]]
                        f3 = self.F3[instructions[1]]
                    else:
                        raise Exception(f"instruction not found in line {str(l)}")
                elif len(instructions) == 3:
                    if instructions[0] in self.F1.keys() and instructions[1] in self.F2.keys() and instructions[2] in self.F3.keys():
                        f1 = self.F1[instructions[0]]
                        f2 = self.F2[instructions[1]]
                        f3 = self.F3[instructions[2]]
                    else:
                        raise Exception(f"instruction not found in line {str(l)}")
                    
                if line[1] in self.CD.keys():
                    cd = self.CD[line[1]]
                else:
                    raise Exception(f"condition not found in line {str(l)}")
                
                if line[2] in self.BR.keys():
                    br = self.BR[line[2]]
                else: 
                    raise Exception(f"branch not found in line {str(l)}")
                
                if len(line) == 3:
                    pass
                elif line[3] == "NEXT":
                    ad = bin(line_counter + 1)[2:].zfill(7)
                elif line[3] in self.labels_dict.keys():
                    ad = bin(self.labels_dict[line[3]])[2:].zfill(7)
                else:
                    raise Exception(f"address not found in line {str(l)}")
                
                self.value[line_counter] = f1 + f2 + f3 + cd + br + ad
                
                
            line_counter += 1
            l += 1
                
                
    def assemble(self) -> dict:
        self.extract_labels()
        self.extract_values()
        
        return self.value
    
    def get_opcode(self) -> dict:
        return self.labels_dict
                         
            
            
            
            
            
            
