import datetime
import configparser
import os
import sys
import argparse

def loadConfig(path,radio,chas,data):

    now = datetime.datetime.now()
    hh = 0 
    log = ""
    if data == '0':
        name_file = now.strftime("%Y-%m-%d")+".txt"
    else:
        name_file = data+".txt"
       
    if chas == "now":
        chas = now.strftime("%H")
    elif chas == "0":
        hh = 1

    if radio == "":
        nf = ""
    else:
        nf = radio+"\\"
            
           
    for key in config["radio"]:
        if hh == 1:
            chas = config[key]["time"]
        if radio == "" and config["radio"][key] == "1":
            log += parser_log(config[key]["path_dir"],chas,config[key]["name"],name_file)
        elif key == radio:
            log += parser_log(config[key]["path_dir"],chas,config[key]["name"],name_file)

    if namespace.analysis:
        err = analysis(log,radio)
        print(err)
    else:     
        print(log)
        if not os.path.exists(config["Setting"]["save_path"]+nf):
            os.makedirs(config["Setting"]["save_path"]+nf)        
        fs = open(config["Setting"]["save_path"]+nf+name_file, "w", encoding='utf-8')
        fs.write(log)
        fs.close()              

def analysis(log,radio):
    obraz = []
    exobraz = []
    ok = 0
    err = 0
    samp = config[radio]["sample"]
    
    for key in config[samp]:
        if key[:4] == 'incl':
            obraz.append(config[samp][key])
        elif key[:4] == 'excl':
            exobraz.append(config[samp][key])

    log = log.rstrip('\r')
    list_log = log.split("\n")
    #print(list_log)
    for st in list_log:
        for obr in obraz:
            if st.find(obr) != -1:
                ok += 1
        for exobr in exobraz:
            if st.find(exobr) != -1:
                err += 1        

            
    return '{"OK": '+str(ok)+', "ERR": '+str(err)+'}'

def parser_log(path_dir, period, radio, file_name):
    period = period.replace("-",",")
    pr = period.split(",")
    name_file = file_name
    if not namespace.noname:
        txt_log = radio+"\n"
    else:
        txt_log = ""
    prev_str_time = ""
    prev_str_time_1 = ""
    
    try:
        f = open(path_dir+name_file, "r", encoding='utf-8')
    except:
        return ""
    for line in f.readlines():
        line = line.rstrip('\r\n')   
        if line.find("Опознан") != -1:
            
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
                    
    txt_log += "\n"
    return txt_log
  
def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-r', '--radio', default='', help='Название радио как в конфиге')
    parser.add_argument ('-c', '--chas', default='0', help='Часы, которые необходимо проверить. Пример: 07,08')
    parser.add_argument ('-d', '--data', default='0', help='Дата в формате гггг-мм-дд')
    parser.add_argument ('-n', '--noname', action='store_true', default=False, help='Не добавлять название радио в лог')
    parser.add_argument ('-a', '--analysis', action='store_true', default=False, help='Анализ лога')
    parser.add_argument ('-s', '--show', action='store_true', default=False, help='Показать названия радио в конфиге')

    return parser
                    

if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args()

    pathname = os.path.dirname(sys.argv[0]) +'\\'          
   
    name_config = pathname + "settings.ini" #D:\\Обмен\\logger\\

    if not os.path.exists(name_config):
        print("не верный путь.")
        exit()
        
    config = configparser.ConfigParser()
    config.read(name_config, encoding='UTF-8')
    
    if namespace.show:
        for key in config["radio"]:
            print(key)
        exit()
    
    loadConfig(name_config,namespace.radio,namespace.chas,namespace.data)
    exit()
