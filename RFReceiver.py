from pi_switch import RCSwitchReceiver
from Config import Config

#---------------------------------------------------------------------------# 
# Configure receiver
#---------------------------------------------------------------------------# 
receiver = RCSwitchReceiver()
receiver.enableReceive(Config.RPi_Pin_Receiver)

num = 0

#---------------------------------------------------------------------------# 
# Loop and wait for commands
#---------------------------------------------------------------------------# 
while True:
    if receiver.available():
        received_value = receiver.getReceivedValue()
        if received_value:
            num += 1
            print("Received[%s]:" % num)
            print(received_value)
            print("%s / %s bit" % (received_value, receiver.getReceivedBitlength()))
            print("Protocol: %s" % receiver.getReceivedProtocol())
            print("")

        receiver.resetAvailable()