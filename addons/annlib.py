import time; from pystyle import Colors, Write
def logo():
    global degmain
    degmain=Colors.red_to_purple
    Write.Print("""
┏┓    ┓•┓   ┓ ┏┓
┣┫┏┓┏┓┃┓┣┓  ┃ ┃┫
┛┗┛┗┛┗┗┗┗┛  ┻•┗┛                                             
""", Colors.red_to_yellow, 0.009)
    Write.Print("✧  Custom MSP loader", Colors.red_to_yellow, 0.009)
    print()
    time.sleep(2)