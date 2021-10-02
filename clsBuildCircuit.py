##############################################
#### Written By: SATYAKI DE               ####
#### Written On: 25-Sep-2021              ####
#### Modified On 25-Sep-2021              ####
####                                      ####
#### Objective: Calling Tk Circuit API    ####
##############################################

from tkgpio import TkCircuit
from json import load
from clsConfig import clsConfig as cf

fileName = str(cf.conf['JSONFileNameWithPath'])

print('File Name: ', str(fileName))

# initialize the circuit inside the GUI
with open(fileName, "r") as file:
    config = load(file)

class clsBuildCircuit:
    def __init__(self):
        self.config = config

    def genCir(self, main_function):
        try:
            config = self.config
            circuit = TkCircuit(config)
            circuit.run(main_function)

            return circuit
        except Exception as e:
            x = str(e)
            print(x)

            return ''
