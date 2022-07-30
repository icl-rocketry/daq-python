import serial

def convert_data(x):
    COL_NAMES = [
           'DAQ Temp',
           'Tc1: run tank',
           'Tc2: Feed system pre injection',
           'Tc3: PreCCTemp',
           'Tc4: detached',
           'PTD_1', # pressure transducer 1
           'UPSTREAM_PTD',
           'unknown8',
           'unknown9',
           'unknown10',
           'unknown11',
           'RunTank', # mass of run tank
           'Thrust',
           'unknown14',
           'unknown15'
    ]

    CONVERSION_FACTORS = {
            'DAQ Temp':lambda x: x, # 0
            'Tc1: run tank':lambda x: x, # 1
            'Tc2: Feed system pre injection':lambda x: x, # 2
            'Tc3: PreCCTemp':lambda x: x, # 3
            'Tc4: detached':lambda x: x, # 4
            'PTD_1':lambda x: x/50.35 - 5.2, # pressure transducer 1 # 5
            'UPSTREAM_PTD':lambda x: x/50.35 - 5.2, # 6
            'unknown8':lambda x: x/50.35 - 5.2, # 7 
            'unknown9':lambda x: x, # 8
            'unknown10':lambda x: x, # 9
            'unknown11':lambda x: x, # 10
            'RunTank':lambda x: 1.53e-4 * x - 7.67, # mass of run tank # 11
            'Thrust':lambda x: -x/90436.0, # 12
            'unknown14':lambda x: x, # 13
            'unknown15':lambda x: x # 14
    }

    for i, val in enumerate(x):
        if i in [5, 6, 11, 12]:
            x[i] = str(round(CONVERSION_FACTORS[COL_NAMES[i]](float(val)), 3))

    return x

# x is list of strings
def parse_data(x):
    strout = ""
    for i in x[0:-1]:
        strout = strout+i+", "
    
    strout = strout+x[-1]+"\n"
    return strout

with serial.Serial() as ser:
    ser.baudrate = 115200
    # check_devices bash script identifies which port it's on
    #ser.port = '/dev/ttyUSB1'
    ser.port = '/dev/ttyUSB0'
    ser.rts = 0
    ser.dtr = 0
    ser.xonxoff = 1
    ser.timeout = 1.0 # 1s timeout
    ser.open()
    print("beginning logging")

    f = open("data-out.csv", "a")
    for i in range(30):
        x = ser.readline().decode("utf-8")
        print(x)
        f.write(x)

    while True:
        try:
            x = ser.readline().decode("utf-8").strip("\n").split(",")
            x = convert_data(x)
            x = parse_data(x)
            f.write(x)
            #write_data(f, x)
            print(x)
            #print('\n')
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(x)
            print(e)
            #print("errored in read/write loop")


#import serial
#ser = serial.Serial()
#ser.baudrate = 115200
## check_devices bash script identifies which port it's on
##ser.port = '/dev/ttyUSB1'
#ser.port = '/dev/ttyUSB0'
#ser.rts = 0
#ser.dtr = 0
#ser.xonxoff = 1
#ser.timeout = 1.0 # 1s timeout
#ser.open()
#
#COL_NAMES = [
       #'DAQ Temp',
       #'Tc1: run tank',
       #'Tc2: Feed system pre injection',
       #'Tc3: PreCCTemp',
       #'Tc4: detached',
       #'PTD_1', # pressure transducer 1
       #'UPSTREAM_PTD',
       #'unknown8',
       #'unknown9',
       #'unknown10',
       #'unknown11',
       #'RunTank', # mass of run tank
       #'Thrust',
       #'unknown14',
       #'unknown15'
#]
#CONVERSION_FACTORS = {
        #'DAQ Temp':lambda x: x, # 0
        #'Tc1: run tank':lambda x: x, # 1
        #'Tc2: Feed system pre injection':lambda x: x, # 2
        #'Tc3: PreCCTemp':lambda x: x, # 3
        #'Tc4: detached':lambda x: x, # 4
        #'PTD_1':lambda x: x/50.35 - 5.2, # pressure transducer 1 # 5
        #'UPSTREAM_PTD':lambda x: x/50.35 - 5.2, # 6
        #'unknown8':lambda x: x/50.35 - 5.2, # 7 
        #'unknown9':lambda x: x, # 8
        #'unknown10':lambda x: x, # 9
        #'unknown11':lambda x: x, # 10
        #'RunTank':lambda x: 1.53e-4 * x - 7.67, # mass of run tank # 11
        #'Thrust':lambda x: -x/90436.0, # 12
        #'unknown14':lambda x: x, # 13
        #'unknown15':lambda x: x # 14
#}
#for i in range(30):
    #ser.readline()
#
#x = ser.readline().decode("utf-8").strip("\n").split(",")
#for i, val in enumerate(x):
    #if i in [0, 1, 2, 3, 5, 6, 11, 12]:
        #x[i] = str(round(CONVERSION_FACTORS[COL_NAMES[i]](float(val)), 3))
#
#f = open("data-out.csv", "a")
#strout = ""
#for i in x[0:-1]:
    #strout = strout+i+", "
#
#strout = strout+x[-1]+"\n"
#f.write(strout)
