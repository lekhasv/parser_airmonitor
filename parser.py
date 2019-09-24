import datetime
import configparser
import os


def loadConfig(path):
    if not os.path.exists(path):
        exit()
    config = configparser.ConfigParser()
    config.read(path, encoding='UTF-8')
    
    for key in config["radio"]:
        if config["radio"][key] == "1":
           # print("\r\n"+config[key]["name"])
            parser_log(config[key]["path_dir"],config[key]["time"],config["Setting"]["save_path"],config[key]["name"])

def parser_log(path_dir, period, save_path,radio):
    now = datetime.datetime.now()
    pr = period.split(",")
    name_file = now.strftime("%Y-%m-%d")+".txt"
    txt_log = radio+"\n"
    prev_str_time = ""
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
                str_time = line[11:15]
                if (prev_str_time != str_time):            
                    pos_end = line.find(", Ошибок")
                    txt_log += line[11:16]+" "+ line[29:pos_end]+"\n"
                    prev_str_time = str_time
                    #print (txt_log)
    txt_log += "\n"                
    fs = open(save_path+name_file, "a", encoding='utf-8')
    fs.write(txt_log)
    fs.close()    
                    

if __name__ == "__main__":
    name_config = "settings.ini"
    loadConfig(name_config)
    exit()
