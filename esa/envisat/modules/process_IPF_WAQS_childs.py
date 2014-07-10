#!/usr/bin/env python
# -*- coding: latin-1 -*-
# file: process_IPF_WAQS_childs.py

import os
import os.path
import sys
import time

print("\n************************************************")
print(" Script \'process_IPF_WAQS_childs.py\' at work... ")
print("************************************************\n")

def ensurePathExists(_path):
    if not os.path.exists(_path):
        os.makedirs(_path)

thetime   = time.localtime()
year_str  = str(thetime[0]) + "/"

# directories
baseDir = '/fs14/EOservices/InputPool/MERIS/RR/'
srcDir  = baseDir + 'waqs_child_temp/'
destDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-IPF/daily/'
ensurePathExists(destDir)

# tools config
pconvertTool    = '/home/uwe/tools/pconvert/pconvert.sh'
bandarithTool   = '/home/uwe/tools/BandArithBatch/BandArithBatch.sh'
bandarithParams = ' algal_12 \"l2_flags.WATER and !l2_flags.PCD_15 ? algal_1 : (l2_flags.WATER and !l2_flags.PCD_16 ? algal_2 : 0.00)\"'

# Inputliste holen
src_list = os.listdir(srcDir)
list_size = len(src_list)

# Liste bereinigen um die Dateien, die keine MERIS-L2-Produkte sind:
for a in range(list_size):
    for item in src_list:
        if not item.startswith('MER_RR__2') or not item.endswith('.N1'):
            print("Removing " + item + " from list.")
            src_list.remove(item)

if not len(src_list):
    print("No input found. Cancelling...")
    sys.exit(1)

src_list.sort()

# Jetzt geht's los:
for meris_file in src_list:
    
    # MER_RR__1PNPDE20051126_053458_000011252042_00463_19555_0425.N1
    # 0         1         2         3         4         5         6
    # 01234567890123456789012345678901234567890123456789012345678901   

    # pconvert syntax: ./pconvert.sh -f dim -o ./ -b 17,18 <product>
    meris_file_path = srcDir + meris_file
    pconvertCommand = pconvertTool + ' -f dim -o ' + destDir + ' -b 16,17,18,33 ' + meris_file_path
    print(pconvertCommand)
    print("Processing file " + meris_file + " ...")
    os.system(pconvertCommand)
    
    pconvertOutputProduct = destDir + meris_file[0:60] +'dim'
    print(pconvertOutputProduct)
    # bandarith batch syntax:
    #<productName> [-d <destProductName>]<bandName> <expression> [<bandName> <expression>]

    bandarithCommand = bandarithTool + ' ' + meris_file_path + ' -d ' + pconvertOutputProduct + bandarithParams
    print(bandarithCommand)
    os.system(bandarithCommand)

print("\n************************************************")
print(" Script \'process_IPF_WAQS_childs.py\' finished. ")
print("************************************************\n")

# EOF