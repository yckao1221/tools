#! Python 3 
# drawFont.py
# 08/31/2018 sample created
#--------------------------
import os
from sys import argv
import font

def asciishow_file_v(msg,outFile):
    ilen = len(msg)
    b_str = msg;  

    textFileName=outFile
    textFile = open(textFileName,"w")

    fontSize = 8
    
    i = 0
    while i < ilen :
        hicode = b_str[i]
        offset = fontSize*ord(hicode)
        #print(offset)
        i += 1
        
        for ht in range(0,8):
            for wt in range(0,1):
                showbyte = font.fontData[offset+wt*8+ht]
                mask = 0x1
                for index in range(0,8):
                    isShow = showbyte & int(mask<<index)
                    if isShow > 0 :
                        textFile.write(hicode)
                    else:
                        textFile.write(" ")
            textFile.write("\n")
    
    textFile.close()

def asciishow_file_h(msg,outFile):
    ilen = len(msg)
    b_str = msg;  

    textFileName=outFile
    textFile = open(textFileName,"w")

    fontSize = 8
    offset_all = [1 for n in range(20)]

    i = 0
    while i < ilen :
        hicode = b_str[i]
        offset_all[i] = fontSize*ord(hicode)
        #print(offset)
        i += 1
    
    for ht in range(0,8):
        for wt in range(0,1):
            ndxWord =0
            while ndxWord < ilen :
                showbyte = font.fontData[offset_all[ndxWord]+wt*8+ht]
                showChar = b_str[ndxWord]

                mask = 0x1
                for index in range(0,8):
                    isShow = showbyte & int(mask<<index)
                    if isShow > 0 :        
                        textFile.write(showChar)
                    else:
                        textFile.write(" ")
                ndxWord += 1

            textFile.write("\n")

    textFile.close()

#=========================
# -i message string
# -f output filename
#=========================
def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            if argv[0][1] != 'v':
                opts[argv[0]] = argv[1]  # Add key and value to the dictionary
            else:
                opts[argv[0]] = "DUMMY"  # Add "DUMMY" key
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

#print(font)
if __name__ == '__main__':
    msg="WELCOME AIT!"
    ascFileName = 'ascfont.txt'

    myargs = getopts(argv)
    if '-i' in myargs or '-f' in myargs :  # Example usage.
        print(myargs['-i'])
        print(myargs['-f'])
    else:
        print("Default setting...")
        print("-i 'WELCOME TO AIT'")
        print("-f 'ascfont.txt'")

    if '-i' in myargs:    
        msg = myargs['-i']

    if '-f' in myargs:     
        ascFileName = myargs['-f']

    ####################################################
    # setup default font file name
    basedir = os.path.abspath(os.path.dirname(__file__))
    fontPath = os.path.join(basedir,ascFileName)

    if '-v' in myargs:
        asciishow_file_v(msg,fontPath)
    else:
        asciishow_file_h(msg,fontPath)
        