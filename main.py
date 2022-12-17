from kaitaistruct import KaitaiStream
from io import BytesIO
import glob, os, sys, json, re
import subprocess

sys.path.append("./py")
from textmap import Textmap

# Change TextMapLanguage
TextMapLanguage = "KR"
'''
    01/26692920 => 
    02/27251172 => 
    03/25181351 => 
    04/25776943 => EN
    05/20618174 => 
    06/25555476 => 
    07/30460104 => 
    08/32244380 => 
    09/22299426 => KR
    10/23331191 => 
    11/21030516 => 
    12/32056053 => 
    13/34382464 => 
'''

def GetAllTextmaps():
    global TextMapLanguage
    output = dict()

    total = len(glob.glob('./bin/TextMap_' + TextMapLanguage + '/*.bin'))
    cnt = 0

    for file in glob.glob('./bin/TextMap_' + TextMapLanguage + '/*.bin'):

        cnt += 1
        print("Parsing in progress [" + str(cnt) + "/" + str(total) + "]")

        with open(file, 'rb') as f:
            stream = KaitaiStream(BytesIO(f.read()))
            obj = Textmap(stream)

            for block in obj.textmap:
                output[str(block.hash.value)] = block.string.data

    with open("./json/TextMap_" + TextMapLanguage + ".json", "w", encoding='utf-8') as json_file:
        json.dump(output, json_file, indent=4, ensure_ascii=False)
