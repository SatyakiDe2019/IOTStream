###############################################
#### Written By: SATYAKI DE                ####
#### Written On: 25-Sep-2021               ####
#### Modified On 25-Sep-2021               ####
####                                       ####
#### Objective: Main Tk Circuit GUI script ####
#### to create an IOT Device to generate   ####
#### the events, which will consumed.      ####
###############################################

# We keep the setup code in a different class as shown below.
import clsBuildCircuit as csb
import json
import clsPublishStream as cps
import datetime
from clsConfig import clsConfig as cf
import logging

###############################################
###           Global Section                ###
###############################################

# Initiating Ably class to push events
x1 = cps.clsPublishStream()

# Create the instance of the Tk Circuit API Class.
circuit = csb.clsBuildCircuit()

###############################################
###    End of Global Section                ###
###############################################

# Invoking the IOT Device Generator.
@circuit.genCir
def main():

    from gpiozero import PWMLED, Motor, Servo, MCP3008, Button
    from time import sleep

    # Circuit Components
    ledAlert = PWMLED(21)
    dcMotor = Motor(22, 23)
    servoMotor = Servo(24)

    ioMeter1 = MCP3008(0)
    ioMeter2 = MCP3008(2)
    ioMeter3 = MCP3008(6)
    switch = Button(15)
    # End of circuit components

    # Other useful variables
    cnt = 1
    idx = 0
    debugInd = 'Y'
    var = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # End of useful variables

    # Initiating Log Class
    general_log_path = str(cf.conf['LOG_PATH'])
    msgSize = int(cf.conf['limRec'])

    # Enabling Logging Info
    logging.basicConfig(filename=general_log_path + 'IOTDevice.log', level=logging.INFO)


    while True:
        ledAlert.value = ioMeter1.value

        if switch.is_pressed:
            dcMotor.forward(ioMeter2.value)
            xVal = 'Motor Forward'
        else:
            dcMotor.backward(ioMeter2.value)
            xVal = 'Motor Backward'

        servoMotor.value = 1 - 2 * ioMeter3.value

        srcJson = {
        "LedMeter": ledAlert.value,
        "DCMeter": ioMeter2.value,
        "ServoMeter": ioMeter3.value,
        "SwitchStatus": switch.is_pressed,
        "DCMotorPos": xVal,
        "ServoMotor": servoMotor.value
        }

        tmpJson = str(srcJson)

        if cnt == 1:
            srcJsonMast = '{' + '"' + str(idx) + '":'+ tmpJson
        elif cnt == msgSize:
            srcJsonMast = srcJsonMast + '}'
            print('JSON: ')
            print(str(srcJsonMast))

            # Pushing both the Historical Confirmed Cases
            retVal_1 = x1.pushEvents(srcJsonMast, debugInd, var)

            if retVal_1 == 0:
                print('Successfully IOT event pushed!')
            else:
                print('Failed to push IOT events!')

            srcJsonMast = ''
            tmpJson = ''
            cnt = 0
            idx = -1
            srcJson = {}
            retVal_1 = 0
        else:
            srcJsonMast = srcJsonMast + ',' + '"' + str(idx) + '":'+ tmpJson

        cnt += 1
        idx += 1

        sleep(0.05)
