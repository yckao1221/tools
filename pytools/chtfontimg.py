#! Python 3 
# chtfont.py
# 09/04/2018 sample created
#--------------------------
import os
from sys import argv

#==[devode_big5]=======
#= decode big5 chinese charactar and return it's index
#======================
def decode_big5_UTF8(uChtString):

    ## Convert from unicode string to big5 array
    chtword = uChtString
    chtword = chtword.encode('big5').decode('big5')
    bValue = bytes(chtword,'big5') 

    ## retrieve hi-byte and lo-byte of Chinese big-5 code.
    hi = bValue[0]
    lo = bValue[1]

    offset = 0

    if lo>=161:
        font_offset = (hi - 161) * 157 + lo - 161 + 1 + 63
        pass
    else:
        font_offset = (hi - 161) * 157 + lo - 64 + 1

    serCode = font_offset

    if (serCode >= 472) and (serCode < 5872):
        offset = (serCode - 472)
    elif (serCode >= 6281) and (serCode <= 13973):
        offset = (serCode - 6281) + 5401
    return offset

def cht_writetext_v(chtmsg,outFile):

    b_str = chtmsg;
    font = open(fontFileName,"rb")
    
    textFileName=outFile
    textFile = open(textFileName,"w")

    fontSize = 3*24

    iLen = len(b_str)
    print(iLen)
    i = 0;
    while i < iLen:
        offset = fontSize*decode_big5_UTF8(b_str[i])
        print(offset)
        font.seek(offset)
        i += 1
        for ht in range(0,24):
            for wt in range(0,3):
                showbyte = font.read(1)
                mask = 0x80
                for index in range(0,8):
                    isShow = showbyte[0] & int(mask>>index)
                    if isShow > 0 :
                        textFile.write("X")
                    else:
                        textFile.write(" ")
            textFile.write("\n")
    textFile.close()
    font.close()

def cht_writetext_h(chtmsg,outFile):

    b_str = chtmsg;
    dbmsg = ""
    font = open(fontFileName,"rb")
    
    textFileName=outFile
    textFile = open(textFileName,"w")

    fontSize = 3*24
    offset_all = [1 for n in range(20)]

    iLen = len(b_str)
    print(iLen)

    ## caculate all font index for each chinese character.
    i = 0
    while i < iLen :
        offset_all[i] = fontSize*decode_big5_UTF8(b_str[i])
        ## print(offset_all[i])
        i += 1

    ## 
    for ht in range(0,24):
        ndxWord =0
        while ndxWord < iLen :
            font.seek(offset_all[ndxWord]+ht*3)
            ndxWord += 1 
                
            for wt in range(0,3):
                showbyte = font.read(1)
                mask = 0x80
                for index in range(0,8):
                    isShow = showbyte[0] & int(mask>>index)
                    if isShow > 0 :
                        textFile.write("X")
                        dbmsg = dbmsg + "X"
                    else:
                        textFile.write(" ")
                        dbmsg = dbmsg + " "                
            textFile.write(" ") ## added dummy space
            dbmsg = dbmsg + " "

        textFile.write("\n")
        print(dbmsg)
        dbmsg = ""
    textFile.close()
    font.close()

def cht_write_arrar(chtmsg,outFile,imgFile):

    b_str = chtmsg;
    font = open(fontFileName,"rb")
    
    textFileName=outFile
    textFile = open(textFileName,"w")

    fontSize = 3*24
    iLen = len(b_str)
    print(iLen)
    
    outputString=""
    outputString += "myGraphic = [" + '\r'

    i   = 0
    idx = 0
    while i < iLen:
        offset = fontSize*decode_big5_UTF8(b_str[i])
        print(offset)
        font.seek(offset)
        i += 1
        for ht in range(0,24):
            for wt in range(0,3):
                showbyte = font.read(1)
                idx += 1
                
                byteVal = int(showbyte[0])
                #outputString += hex(byteVal) + ", "
                outputString += "{0:#0{1}x}".format(byteVal,4) + ", "
                
                if (idx % 16 == 0):
                    outputString += '\r'

                mask = 0x80
                for index in range(0,8):
                    isShow = showbyte[0] & int(mask>>index)
                    if isShow > 0 :
                        textFile.write("X")
                    else:
                        textFile.write(" ")
            textFile.write("\n")
    
    outputString = outputString[:-2]
    outputString += "]"
    print(outputString)
    textFile.close()
    font.close()

    #Write the output string to our output file
    outfile = open(imgFile,"w")
    outfile.write(outputString)
    outfile.close()

if __name__ == '__main__':
    
    msg=u"中文明體"
    ascFileName = 'chtfont.txt'
    imgFileName = "chtfntimg.txt"
    def_fontName = 'stdfont.24'
    #def_fontName = 'STDFONT.24K'
    fontFileName = 'stdfont.24'

    ####################################################
    # setup default font file name
    basedir = os.path.abspath(os.path.dirname(__file__))
    fontPath = os.path.join(basedir,ascFileName)
    imgPath = os.path.join(basedir,imgFileName)
    fontFileName = os.path.join(basedir,def_fontName)
    
    ## unmark if you like vertical text
    ## cht_writetext_v(msg,fontPath)
    ## cht_writetext_h(msg,fontPath)
    cht_write_arrar(msg,fontPath,imgPath)