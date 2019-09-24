import datetime
import configparser
import os
import sys

def loadConfig(path,radio,chas,data):
    if not os.path.exists(path):
        print("не верный путь.")
        exit()
    config = configparser.ConfigParser()
    config.read(path, encoding='UTF-8')
    now = datetime.datetime.now()
    if data == 0:
        name_file = now.strftime("%Y-%m-%d")+".txt"
    else:
        name_file = data+".txt"
    hh = 0    
    if chas == "now":
        chas = now.strftime("%H")
    elif chas == "0":
        hh = 1
    #print(chas)    
    
    for key in config["radio"]:
        if hh == 1:
            chas = config[key]["time"]
        if radio == "" and config["radio"][key] == "1":
            parser_log(config[key]["path_dir"],chas,config["Setting"]["save_path"],config[key]["name"],name_file)
        elif key == radio:
            parser_log(config[key]["path_dir"],chas,config["Setting"]["save_path"],config[key]["name"],name_file)

def parser_log(path_dir, period, save_path,radio,file_name):

    pr = period.split(",")
    name_file = file_name
    txt_log = radio+"\n"
    prev_str_time = ""
    prev_str_time_1 = ""
    
    try:
        f = open(path_dir+name_file, "r", encoding='utf-8')
    except:
        exit()
    for line in f.readlines():
        line = line.rstrip('\r\n')   
        if (line.find("Опознан") != -1):
            
            hour_period = False
            for hr in pr:                
                if hr == line[11:13]:
                    hour_period = True
                
            if hour_period:       
                str_time = line[11:16]
                if (prev_str_time != str_time)&(prev_str_time_1 != str_time):            
                    pos_end = line.find(", Ошибок")                   
                    txt_log += line[11:16]+" "+ line[29:pos_end]+"\n"
                    prev_str_time_1  = line[11:14]+str(int(line[14:16])+1)
                    prev_str_time = str_time
                    
    print (txt_log)
    txt_log += "\n"                
    fs = open(save_path+name_file, "a", encoding='utf-8')
    fs.write(txt_log)
    fs.close()    
                    

if __name__ == "__main__":

    if len(sys.argv) > 3:
        radio = sys.argv[1]
        chas = sys.argv[2]
        data = sys.argv[3]
    elif len(sys.argv) > 2:
        radio = sys.argv[1]
        chas = sys.argv[2]
        data = 0
    elif len(sys.argv) > 1:
        radio = sys.argv[1]
        chas = "0"
        data = 0
    else:
        radio = ""
        chas = "0"
        data = 0

    pathname = os.path.dirname(sys.argv[0])          
   
    name_config = pathname + "\\settings.ini" #D:\\Обмен\\logger\\
    loadConfig(name_config,radio,chas,data)    
    #exit()
