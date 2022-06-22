from time import sleep
import serial

DATA_ACQUISITION_MILISECOND = 1000 * 10
DELAY = 50


class data_sample:
    def __init__(self, id, sex=None, age=None, weight=None, length=None, region=None, vegetarian=None, device_data = None):
        self.id = id
        self.sex = sex #M:male F:female
        self.age = age #number
        self.weight = weight #F:fat N:normal S:skinny
        self.length = length #T:tall N:normal S:short
        self.region = region #M:marmara A:Aegeean M:mediterranian B:blacksea C:centralanatolia E:easternanatolia SE:southeastearnanatolia
        self.vegetarian = vegetarian #T:true F:false
        self.device_data = device_data #filepath
    
    def to_file(self, filepath):
        with open(filepath, 'a') as f:
            f.write(str(self.id) + ',' + str(self.sex) + ',' + str(self.weight) + ',' + str(self.length) + ',' + str(self.region) + ',' + str(self.device_data) + '\n')
            f.close()


#while True:
#    print(ser.readline()) # write a string

fd = open('data/data_info', 'r')
id = int(fd.readline())
fd.close()

data = data_sample(id)

while True:
    print('Male(M) or Female(F): ')
    inp = input()
    if inp=='M' or inp=='F':
        data.sex = inp
        break
    else:
        print('Wrong input')

while True:
    print('F:fat N:normal S:skinny')
    inp=input()
    if inp=='F' or inp=='N' or inp=='S':
        data.weight = inp
        break


while True:
    print('T:tall N:normal S:short')
    inp=input()
    if inp=='T' or inp=='N' or inp=='S':
        data.length = inp
        break

while True:
    print('M:marmara A:Aegeean ME:mediterranian B:blacksea C:centralanatolia E:easternanatolia SE:southeastearnanatolia')
    inp=input()
    if inp=='M' or inp=='A' or inp=='ME' or inp=='B' or inp=='C' or inp=='E' or inp=='SE':
        data.region  = inp
        break

while True:
    print('Vegetarian? T:true F:false')
    inp = input()
    if inp == 'T' or inp == 'F':
        data.vegetarian = inp
        break

liked_count = 0
notliked_count = 0

  # open serial port

sleep(.5)
for i in range(4):

    ser = serial.Serial('/dev/cu.usbserial-0001', 115200)
    print(ser.isOpen())         # check which port was really used
    
    device_fd = open('data/device_data/'+str(id)+'_'+str(i), 'w+')
    sleep(1)
    ser.flushInput()
    sleep(1)
    for t in range(DATA_ACQUISITION_MILISECOND//DELAY):
        device_data_str = str(ser.readline())
        device_data_str = device_data_str.replace("b'", '')
        device_data_str = device_data_str.replace("\\r\\n'", '')
        device_data_str = device_data_str.split('\\')[0]
        device_data_list = device_data_str.split(' ')
        sensor_num = device_data_list[0]
        if(sensor_num == ''):
            continue
        sensor_num = int(sensor_num)
        if len(device_data_list) > 1:
            sensor_val = float(device_data_list[1])
        else:
            sensor_val = 0
        sensor_num_ind = sensor_num
        while(sensor_num_ind > 0):
            sensor_num_ind -= 1
            device_fd.write(str(sensor_val) + ',')
            
        for sensor_num_ind in range(4 - sensor_num - 1):
            device_fd.write(str(sensor_val) + ',')
            device_data_str = str(ser.readline())
            device_data_str = device_data_str.replace("b'", '')
            device_data_str = device_data_str.replace("\\r\\n'", '')
            device_data_str = device_data_str.split('\\')[0]
            device_data_list = device_data_str.split(' ')
            sensor_val = float(device_data_list[1])
        device_fd.write(str(sensor_val) + '\n')
        
    while(True):
        liked = input('Liked?(y/n): ')
        if liked == 'y' and liked_count == 0:
            data.device_data = 'data/device_data/'+str(id)+'_'+str(i)
            data.to_file('data/liked_dataset')
            liked_count += 1
            break
        elif liked == 'n':
            data.device_data = 'data/device_data/'+str(id)+'_'+str(i)
            data.to_file('data/notliked_dataset')
            notliked_count += 1
            break
    ser.flushInput()
    ser.close()

fd = open('data/data_info', 'w')
fd.write(str(id+1))


