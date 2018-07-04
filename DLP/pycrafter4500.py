# -*- coding: utf-8 -*-
"""
Created on Mon Jan 08 10:17:19 2018

@author: Administrateur
Generate command for DLPC3500 (DLP4500 LightCrafter)
"""

import usb.core
import usb.util
import time
import numpy
import sys

##function that converts a number into a bit string of given length

def convlen(a,l):
    b=bin(a)[2:]
    padding=l-len(b)
    b='0'*padding+b

    return b

##function that converts a bit string into a given number of bytes

def bitstobytes(a):
    bytelist=[]
    if len(a)%8!=0:
        padding=8-len(a)%8
        a='0'*padding+a
    for i in range(len(a)/8):
        bytelist.append(int(a[8*i:8*(i+1)],2))

    bytelist.reverse()

    return bytelist

class dmd():
    def __init__(self):
        self.dev=usb.core.find(idVendor=0x0451 ,idProduct=0x6401 )

        self.dev.set_configuration()

        self.ans=[]

## standard usb command function

    def command(self, mode, sequencebyte, com2, com3, data=None):
        buffer = []
        if mode == 'r':
            flag = 0xC0 #'1100' reply from host is expected
        else:
            flag = 0x00
            
        buffer.append(flag)
        buffer.append(sequencebyte)
        temp = bitstobytes(convlen(len(data)+2, 16))
        buffer.append(temp[0])
        buffer.append(temp[1])
        buffer.append(com3)
        buffer.append(com2)

        if len(buffer)+len(data)<65:
        
            for i in range(len(data)):
                buffer.append(data[i])

            for i in range(64-len(buffer)):
                buffer.append(0x00)


            self.dev.write(1, buffer)

        else:
            
            for i in range(64-len(buffer)):
                buffer.append(data[i])

            self.dev.write(1, buffer)

            buffer = []

            j=0
            while j<len(data)-58:
                buffer.append(data[j+58])
                j=j+1
                if j%64==0:
                    self.dev.write(1, buffer)

                    buffer = []

            if j%64!=0:

                while j%64!=0:
                    buffer.append(0x00)
                    j=j+1


                self.dev.write(1, buffer)                
                

        if mode =='r':
            self.ans=self.dev.read(0x81,64)


## function printing all of the dlp answer

    def readreply(self):
        for i in self.ans:
            print(hex(i))


## functions for power management

    def standby(self):
        # Power Control command
        self.command('w',0x00,0x02,0x00,[int('00000001',2)])
        

    def wakeup(self):
        # Power Control command
        self.command('w',0x00,0x02,0x00,[int('00000000',2)])
        

    def reset(self):
        # Software Reset command
        self.command('w',0x00,0x08,0x02,[int('00000001',2)])
        

## test write and read operations, 

    def testread(self):
        # LED driver current control
        self.command('r',0xff,0x0b,0x01,[])
        self.readreply()

    def testwrite(self):
        # Display curtain control
        self.command('w',0x22,0x11,0x00,[0xff,0x01,0xff,0x01,0xff,0x01])
        

    def checkstatus1(self):
        # Hardware status command
        self.command('r',0xff,0x1a,0x0a,[])
        temp=bin(self.ans[4])[2:]
        if len(temp)<8:
            hstatus='0'*(8-len(temp))+temp
       
        print('Init: '+hstatus[7])
        print('DMD reset error: '+hstatus[5])
        print('Force swap error: '+hstatus[4])
        print('Sequencer abort error: '+hstatus[1])
        print('Sequencer error: '+hstatus[0])
        
        if self.ans[4]==1:
            return True
        else:
            return False
        
    def checkstatus2(self):
        # Main status command
        self.command('r',0xff,0x1a,0x0c,[])
#        a2=self.ans[2]
#        a1=self.ans[3]
#        longueur=(a2|(a1<<8))
#        print('l='+str(longueur))
        temp=bin(self.ans[4])[2:]
        if len(temp)<8:
            status='0'*(8-len(temp))+temp
        print('DMD park: '+status[7])
        print('Sequencer running: '+status[6])
        print('Frame buffer frozen: '+status[5])
        print('Gamma corr enable: '+status[4])
        
    def dispwholefield(self):
        # Input source selection command
        # Internal test pattern mode is selected
        self.command('w',0xff,0x1a,0x00,[int('00000001',2)])
        # Internal Test Patterns Select: pattern to be displayed is selected. Check table 2-20
        self.command('w',0xff,0x12,0x03,[int('00001001',2)])
        # Internal Test Patterns Color Control
        #self.command('w',0xff,0x12,0x04,[int(r[2:],16),int(r[2:],16),int(g[2:],16),int(g[2:],16),int(b[2:],16),int(b[2:],16),0,0,0,0,0,0])#color             
        
    def setPatternMode(self):
        # Display Mode Selection Command
        # Pattern Mode is chosen
        self.command('w',0x22,0x1a,0x1b,[int('00000001',2)])
        
    def controlLED(self,RGB):
        # LED Enable Outputs
        self.command('w',0xff,0x1a,0x07,[int('00001111',2)])
        r=int((1-RGB[0])*255)
        g=int((1-RGB[1])*255)
        b=int((1-RGB[2])*255)
        if r>255:
            r=255
        if g>255:
            g=255
        if b>255:
            b=255
#        btemp=hex(int(RGB[2]*1023))[2:]
#        if len(btemp)<4:
#            b='0'*(4-len(btemp))+btemp
        # LED Driver Current Control
        self.command('w',0xff,0x0b,0x01,[r,g,b])