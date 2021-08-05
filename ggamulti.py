import sys
import os
import platform
from pprint import pprint
from functools import reduce

def get_nmea_checksum(msg):
    byte_list = [ord(x) for x in msg]
    byte_list = byte_list[1:]
    return reduce(lambda i, j: i ^ j, byte_list)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Not enough arguments!')
        print('Example of usage: python3 ggamulti.py \$GPGGA,125956,4807.038,N,01131.000,E,1,08,,545.440,M,,,,*3D 125')
        exit()
        
    nmea_list=sys.argv[1].split(',')
    time_sec=sys.argv[2]
    if time_sec[-1].isdigit() != True:
        if time_sec[-1] == 's':
            time_sec = int(time_sec[:-1])
        elif time_sec[-1] == 'm':
            time_sec = int(time_sec[:-1])*60
        elif time_sec[-1] == 'h':
            time_sec = int(time_sec[:-1])*3600
    else:
        time_sec=int(time_sec)

    if len(sys.argv) == 4:
        result_txt_file_name = sys.argv[3]
    else:
        result_txt_file_name = "result.txt"
    
    nmea_time=nmea_list[1]
    hour=int(nmea_time[0:2])
    min_=int(nmea_time[2:4])
    sec=int(nmea_time[4:6])
   # print(hour)
   # print(min_)
   # print(sec)
    min_ *= 60
    hour *= 3600
    full_time_sec = hour + min_ + sec
   # print(full_time_sec)
    end_time = full_time_sec + time_sec
    result_text = []
    while full_time_sec < end_time:
        full_time_sec += 1
        full_time_sec %= 86400
        res_hours = full_time_sec // 3600
        res_min = (full_time_sec % 3600) // 60
        res_sec = full_time_sec % 60
        res_nmea_time='%02d%02d%02d' %(res_hours, res_min, res_sec)
    #    print(res_nmea_time)
        nmea_list[1]=res_nmea_time
        clear_new_nmea_msg = nmea_list[0:-1]
        result_nmea_msg = ','.join(clear_new_nmea_msg)
        result_nmea_msg += ','
        result_nmea_msg = "%s*%02X\n" % (result_nmea_msg, get_nmea_checksum(result_nmea_msg))
        result_text.append(result_nmea_msg)
    #    print(result_nmea_msg)

   # pprint(result_text)
    with open(result_txt_file_name, "w") as file:
        for txt in result_text:
            file.write(txt)

    path = os.getcwd()
    if platform.system() == 'Windows':
        path += "\\"
    else:
        path += "/"
    path += result_txt_file_name
    
    print("Done!!! Result saved at %s\n" % path)
    
    

