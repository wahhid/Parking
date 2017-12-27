import ConfigParser
import os.path

class Read_Config:
    
    def __init__(self):
        self.config_status = False                
        self.read_config()                
                        

    def read_config(self):
        if os.path.exists("parking.cfg"):            
            self.config_status = True
            
        if self.config_status:                            
            self.config = ConfigParser.ConfigParser()        
            self.config.read("parking.cfg")                
            self.serverip = self._ConfigSectionMap("General")['serverip']
            self.serverport = self._ConfigSectionMap("General")['serverport']
            self.dbname = self._ConfigSectionMap("General")['dbname']
            self.boothcode = self._ConfigSectionMap("General")['boothcode'] 
            self.boothtype = self._ConfigSectionMap("General")['boothtype']
            self.manless = self._ConfigSectionMap("General")["manless"]
            self.mqttenable = self._ConfigSectionMap("General")["mqttenable"]
            self.mqttserverip = self._ConfigSectionMap("General")["mqttserverip"]
            self.mqttserverport = self._ConfigSectionMap("General")["mqttserverport"]
                                                
    def _ConfigSectionMap(self, section):
        dict1 = {}
        options =  self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
            except:
                dict1[option] = None
        return dict1
