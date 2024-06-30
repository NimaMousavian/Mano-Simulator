from manoSimulator import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from Register import Register
from memory import memory
from cpu import CPU
from Assembler import microprogram_assembler, program_assembler
import time, threading, traceback
import datetime


class program:
    def __init__(self, ui : Ui_MainWindow) -> None:
        self.ui = ui
    
        for i in range(2048):
            self.ui.memory_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i)))
                    
        for i in range(128):
            self.ui.controlMemory_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i)))
        
        self.build_flag = False
        self.run_flag = False
        
        self.ui.build_button.clicked.connect(self.build_func)
        self.ui.next_micro_button.clicked.connect(self.next_micro_func)
        self.ui.next_button.clicked.connect(self.next_operation_func)
        self.ui.run_button.clicked.connect(self.run_func)
        self.ui.stop_button.clicked.connect(self.stop_func)
        self.ui.reset_button.clicked.connect(self.reset_func)
        
        
    def build_func(self):
        
        if self.ui.assemblyCode_text.toPlainText() == "" and self.ui.controlCode_text.toPlainText() == "":
            self.ui.console_text.clear()
            self.ui.console_text.insertPlainText("Pleas enter your assembly and miroprogram code first\n")
        elif self.ui.assemblyCode_text.toPlainText() == "":
            self.ui.console_text.clear()
            self.ui.console_text.insertPlainText("Pleas enter your assembly code first\n")
        elif self.ui.controlCode_text.toPlainText() == "":
            self.ui.console_text.clear()
            self.ui.console_text.insertPlainText("Pleas enter your miroprogram code first\n")
            
        else:
            self.ui.console_text.clear()
            
            assembly_program = self.ui.assemblyCode_text.toPlainText().split('\n')
            for i in range(len(assembly_program)):
                assembly_program[i] = assembly_program[i].split()
                
            
            assembly_microprogram = self.ui.controlCode_text.toPlainText().split('\n')
            for i in range(len(assembly_microprogram)):
                assembly_microprogram[i] = assembly_microprogram[i].split()
                
                
            try:
                self.micro_assembler = microprogram_assembler(assembly_microprogram)
                self.micro_content = self.micro_assembler.assemble()
                opcode = self.micro_assembler.get_opcode()
                
                self.prog_assembler = program_assembler(assembly_program, opcode)
                self.program_content = self.prog_assembler.assemble()
                
                self.cpu = CPU(self.program_content, self.micro_content)
            
                revers_labels = dict([(value, key) for key, value in self.prog_assembler.labels_dict.items()])
                revers_opcode = dict([(value, key) for key, value in opcode.items()])
            
            
                for addr in self.program_content.keys():
                    I = self.program_content[addr][0]
                    opcode_ = self.program_content[addr][1:5]
                    address = self.program_content[addr][5:16]
                
                    
                    self.ui.memory_table.setItem(addr, 2, QtWidgets.QTableWidgetItem(I))
                    self.ui.memory_table.setItem(addr, 3, QtWidgets.QTableWidgetItem(opcode_))
                    self.ui.memory_table.setItem(addr, 4, QtWidgets.QTableWidgetItem(address))
                
                    if addr in revers_labels.keys():
                        self.ui.memory_table.setItem(addr, 1, QtWidgets.QTableWidgetItem(revers_labels[addr] + ","))
                        
                for addr in self.micro_content.keys():
                    f1 = self.micro_content[addr][:3]
                    f2 = self.micro_content[addr][3:6]
                    f3 = self.micro_content[addr][6:9]
                    cd = self.micro_content[addr][9:11]
                    br = self.micro_content[addr][11:13]
                    ad = self.micro_content[addr][13:]
                    
                
                    self.ui.controlMemory_table.setItem(addr, 2, QtWidgets.QTableWidgetItem(f1))
                    self.ui.controlMemory_table.setItem(addr, 3, QtWidgets.QTableWidgetItem(f2))
                    self.ui.controlMemory_table.setItem(addr, 4, QtWidgets.QTableWidgetItem(f3))
                    self.ui.controlMemory_table.setItem(addr, 5, QtWidgets.QTableWidgetItem(cd))
                    self.ui.controlMemory_table.setItem(addr, 6, QtWidgets.QTableWidgetItem(br))
                    self.ui.controlMemory_table.setItem(addr, 7, QtWidgets.QTableWidgetItem(ad))
                
                    if addr in revers_opcode.keys():
                        self.ui.controlMemory_table.setItem(addr, 1, QtWidgets.QTableWidgetItem(revers_opcode[addr] + ":"))
                
                self.ui.console_text.clear()
                self.ui.console_text.insertPlainText("Successfuly compiled.\n")
                self.build_flag = True
                self.cpu.fetch_flag = False
                self.refresh()
            except Exception as e:
                self.ui.console_text.clear()
                self.ui.console_text.insertPlainText(str(e))
                
    def next_micro_func(self):
        
        if self.build_flag:
            self.cpu.fetch_flag = False
            if not self.cpu.fetch_flag and not self.cpu.halt_flag:
                self.cpu.microexecute()
                self.refresh()
            if self.cpu.fetch_flag:
                self.ui.console_text.clear()
                self.ui.console_text.insertPlainText("End of operation.\n")
            if self.cpu.halt_flag:
                self.ui.console_text.clear()
                self.ui.console_text.insertPlainText("Program successfuly finished.\n")
        else:
            self.ui.console_text.clear()
            self.ui.console_text.insertPlainText("Pleas build your code first.\n")
            
    def next_operation_func(self):
        
        if self.build_flag:
            self.cpu.fetch_flag = False
            if not self.cpu.halt_flag:
                self.cpu.execute()
                self.refresh()
            if self.cpu.halt_flag:
                self.ui.console_text.clear()
                self.ui.console_text.insertPlainText("Program successfuly finished.\n")
        else:
            self.ui.console_text.clear()
            self.ui.console_text.insertPlainText("Pleas build your code first.\n")
                   
    def run_func(self):
        
        if self.build_flag:
            if not self.cpu.halt_flag:
                self.r = threading.Timer(0.5, self.run_func)
                self.r.start()
                self.run_flag = True
                
                self.next_micro_func()
        else:
            self.ui.console_text.clear()
            self.ui.console_text.insertPlainText("Pleas build your code first.\n")
        
    def stop_func(self):
        if self.build_flag:
            if self.run_flag:
                self.r.cancel()
            else:
                self.ui.console_text.clear()
                self.ui.console_text.insertPlainText("Pleas run program first.\n")
        else:
            self.ui.console_text.clear()
            self.ui.console_text.insertPlainText("Pleas build your code first.\n")
        
    def reset_func(self):
        if self.build_flag:
            self.cpu.clear()
            self.refresh()
            
            for i in range(2048):
                self.ui.memory_table.setItem(i, 1, QtWidgets.QTableWidgetItem(""))
                self.ui.memory_table.setItem(i, 2, QtWidgets.QTableWidgetItem(""))
                self.ui.memory_table.setItem(i, 3, QtWidgets.QTableWidgetItem(""))
                self.ui.memory_table.setItem(i, 4, QtWidgets.QTableWidgetItem(""))
                
                    
            for i in range(128):
                self.ui.controlMemory_table.setItem(i, 1, QtWidgets.QTableWidgetItem(""))
                self.ui.controlMemory_table.setItem(i, 2, QtWidgets.QTableWidgetItem(""))
                self.ui.controlMemory_table.setItem(i, 3, QtWidgets.QTableWidgetItem(""))
                self.ui.controlMemory_table.setItem(i, 4, QtWidgets.QTableWidgetItem(""))
                self.ui.controlMemory_table.setItem(i, 5, QtWidgets.QTableWidgetItem(""))
                self.ui.controlMemory_table.setItem(i, 6, QtWidgets.QTableWidgetItem(""))
                self.ui.controlMemory_table.setItem(i, 7, QtWidgets.QTableWidgetItem(""))
            
            self.build_flag = False
            self.ui.console_text.clear()
            self.ui.console_text.insertPlainText("Reset successfuly.\n")
        else:
            self.ui.console_text.clear()
            self.ui.console_text.insertPlainText("Pleas build your code first.\n")
          
    def refresh(self):
        self.ui.PC_text.clear()
        self.ui.AC_text.clear()
        self.ui.AR_text.clear()
        self.ui.DR_text.clear()
        self.ui.CAR_text.clear()
        self.ui.SBR_text.clear()
        
        self.ui.PC_text.insertPlainText(str(int(self.cpu.PC.read()[2:])))
        self.ui.AC_text.insertPlainText(str(int(self.cpu.AC.read()[2:])).zfill(16))
        self.ui.AR_text.insertPlainText(str(int(self.cpu.AR.read()[2:])))
        self.ui.DR_text.insertPlainText(str(int(self.cpu.DR.read()[2:])).zfill(16))
        self.ui.CAR_text.insertPlainText(str(int(self.cpu.CAR.read()[2:])).zfill(7))
        self.ui.SBR_text.insertPlainText(str(int(self.cpu.SBR.read()[2:])).zfill(7))
        
        self.ui.memory_table.selectRow(int(self.cpu.PC.read()[2:],2))
        self.ui.controlMemory_table.selectRow(int(self.cpu.CAR.read()[2:],2))

            
        for line in self.program_content.keys():
            addr = "0b" + bin(line)[2:].zfill(11)
            code = self.cpu.main_memory.read(addr)[2:]
            I = code[0]
            opcode_ = code[1:5]
            address = code[5:16]
                
            self.ui.memory_table.setItem(line, 2, QtWidgets.QTableWidgetItem(I))
            self.ui.memory_table.setItem(line, 3, QtWidgets.QTableWidgetItem(opcode_))
            self.ui.memory_table.setItem(line, 4, QtWidgets.QTableWidgetItem(address))
                
            
                        
        for line in self.micro_content.keys():
            addr = "0b" + bin(line)[2:].zfill(7)
            code = self.cpu.microprogram_memory.read(addr)[2:]
            f1 = code[:3]
            f2 = code[3:6]
            f3 = code[6:9]
            cd = code[9:11]
            br = code[11:13]
            ad = code[13:]
                    
                
            self.ui.controlMemory_table.setItem(line, 2, QtWidgets.QTableWidgetItem(f1))
            self.ui.controlMemory_table.setItem(line, 3, QtWidgets.QTableWidgetItem(f2))
            self.ui.controlMemory_table.setItem(line, 4, QtWidgets.QTableWidgetItem(f3))
            self.ui.controlMemory_table.setItem(line, 5, QtWidgets.QTableWidgetItem(cd))
            self.ui.controlMemory_table.setItem(line, 6, QtWidgets.QTableWidgetItem(br))
            self.ui.controlMemory_table.setItem(line, 7, QtWidgets.QTableWidgetItem(ad))
            
            
            
class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False
        
            
                
            



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    p = program(ui)
    sys.exit(app.exec_())
