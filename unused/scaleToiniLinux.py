import configparser

config = configparser.ConfigParser()
config.read('config.ini',encoding='utf-8')
config['general']['scale']=str(1.0)
config['general']['sendimagepossibility']=str(0)
config.write(open('config.ini', 'w',encoding='utf-8'))
