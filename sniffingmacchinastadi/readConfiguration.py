import configparser

def openConfig(fn):
    config = configparser.ConfigParser()
    config.read(fn)
    return config

def ConfigSectionMap(fname,section):
    dict1 = {}
    config = openConfig(fname)
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
        except:
            dict1[option] = None
    return dict1

if __name__ == '__main__':
    configpath = "./config.ini"
    
    mqttconf= ConfigSectionMap(configpath,"mqtt")

    broker = mqttconf["broker"]
    port = int(mqttconf["port"])
    usr = mqttconf["user"]
    pwd = mqttconf["password"]

    print(broker)
    print(port)
    print(usr)
    print(pwd)
