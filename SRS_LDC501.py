
import visa
import time


class SRS_LDC501():
    
    def __init__(self):
        self.connected = False

    def __del__(self):
        if self.connected:
            self.disconnect()
    def connect(self,visaAddr):    
        self.rm = visa.ResourceManager()
        self.instrument = self.rm.get_instrument(visaAddr)        
        print(self.instrument.ask("*IDN?")) #Requests the device for identification
        self.connected = True
        
    def disconnect(self):
        self.instrument.close()
    
    # temperature control settings
    def setTemperature(self, temp):
        self.instrument.write('TEMP %g'%temp)
        
    def getTemperature(self):
        res = self.instrument.ask('TTRD?')
        #print('LD temperature: %g degC'%float(res))
        return(float(res))

    def sync(self):
        self.instrument.write('SYNC 5')
        self.instrument.ask('SYND?')
        
    def scan(self, I_step, num_steps, step_time):
        self.instrument.write('SCAN %g,%g,%g' %(float(I_step),float(num_steps), float(step_time)))
        self.instrument.ask('SCAN?')

    def tecON(self):
        self.instrument.write('TEON ON')
  
    def tecOFF(self):
        self.instrument.write('TEON OFF')
    
    # laser limits
    def setLDVlimit(self,Vlim): # set voltage limit
        self.instrument.write('SVLM %g'%Vlim)
        
    def getLDVlimit(self):
        res=self.instrument.ask('SVLM?')
        print('LD voltage limit: %g V'%float(res))
        
    def setLDIlimit(self,Ilim):
        self.instrument.write('SILM %g'%Ilim)   
            
    def getLDIlimit(self):
        res=self.instrument.ask('SILM?')    
        print('LD current limit: %g mA'%float(res))
    
    # laser settings
    def LDturnON(self): # turn current on
        self.instrument.write('SILD 0')# set current to 0 first
        self.instrument.write('LDON ON')

    def LDturnOFF(self): # turn current on
        self.instrument.write('SILD 0')# set current to 0 first
        time.sleep(1)
        self.instrument.write('LDON OFF')
        
    def getLDturnSTATUS(self):
        res=self.instrument.ask('LDON?')
        if float(res)==1:
            print('LD is ON')
        elif float(res)==0:
            print('LD is OFF')

    def setLDcurrent(self, Iset):  # current setpoint in mA
            self.instrument.write('SILD %g' % Iset)

    def setLDvoltage(self,Vset): # voltage setpoint in V
        self.instrument.write('SVLD %g'%Vset)
    
    # laser monitor
    def getLDcurrent(self): # read current in mA
        res=self.instrument.ask('RILD?')
        return(float(res))
#        print('LD current: %g'%float(res))
        
    def getLDvoltage(self): # read voltage
        res=self.instrument.ask('RVLD?')
        return(float(res))
#        print('LD voltage: %g'%float(res))
    
    # laser configuration
    def setLDIrange(self,toggle): # range
        if toggle==1:
            self.instrument.write('RNGE HIGH')
        elif toggl==0:
            self.instrument.write('RNGE LOW')
        else:
            print("the range should either be 1 or 0 for high or low")