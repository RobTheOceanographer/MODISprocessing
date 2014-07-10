#!/usr/bin/env python
# -*- coding: latin-1 -*
# file: reprocess_MC_weekly_L3_binning.py


import os
import os.path
import sys
import time
from shutil import rmtree

def printUsage():
    print("Usage: reprocess_MC_weekly_L3_binning.py start_date end_date")
    print("where start_date end_date are strings representing a day:")
    print("e.g. 20070710")
    print("and start_date has to be before or equal to end_date")
    print("Each date in the interval [start_date; end_date] results in an array")
    print("of dates to be processed.")
    print("NOTE: start_date and end_date represent the last date")
    print("included in the weekly mean!")

def make_date_array(start_tupel):
    print("start_tupel", start_tupel)
    float_start_date = time.mktime(start_tupel)
    #print "float_start_date", time.mktime(float_start_date)
    result=[]
    result.append(str(start_tupel[0]) + str(start_tupel[1]).rjust(2,'0') + str(start_tupel[2]).rjust(2,'0'))
    print("start_tupel_str", result)
    for i in range(6):
        print(i)
        date_tupel=time.gmtime(float_start_date - i*24*60*60)
        #date_tupel=time.gmtime(float_start_date + 2*60*60 - i*24*60*60)
        print("date_tupel_schleife", date_tupel)
        date_str = str(date_tupel[0]) + str(date_tupel[1]).rjust(2,'0') + str(date_tupel[2]).rjust(2,'0')
        result.append(date_str)
        print("date_str", date_str)
    return result

try:
    argc=len(sys.argv)
    if (argc < 3):          # the program was called incorrectly
        print("\nToo few parameters passed!")
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        start_date = sys.argv[1]
        end_date   = sys.argv[2]
        if (int(start_date) <= int(end_date) ):
            # do something
            print("\nReprocessing products from " + start_date + " to " + end_date + "...\n")
        else:               # incorrect parameters
            print("Wrong parameters!")
            printUsage()
            sys.exit(1)
except:
    print("\nError in parameters. Now exiting...\n")
    sys.exit(1)    

print("\n*******************************************************")
print(" Script \'reprocess_MC_weekly_L3_binning.py\' at work... ")
print("*******************************************************\n")


# Verzeichnisse
srcDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/daily-merged/'
destDir = '/fs14/EOservices/OutputPool/MERIS/RR/WAQS-MC/weekly/'

# tools config
l3binningHome   = '/home/uwe/tools/beam-4.5.1_01/bin/'
l3binningScript = l3binningHome + 'binning.sh'
grid_cell_size = '1.2'


for date_int in range(int(start_date), int(end_date)+1):
    date = str(date_int)
    _year  = int(date[0:4])
    _month = int(date[4:6])
    _day   = int(date[6:len(date)])
    _date_struct = (_year, _month, _day, 1, 0, 0, 0, 0, 1)
    

    # Wir wollen 7 zurueckliegende Tage prozessieren:
    days= make_date_array(_date_struct)
    
   # for region in ['NorthSea', 'Estonia', 'Baltic']:
    for region in ['NorthSea', 'Baltic']:
        if region=='NorthSea':
            regionSrcID = 'NSEA'
            regiondestID= '_nos_'
            lat_min = '49.0'
            lat_max = '63.0'
            lon_min = '-5.0'
            lon_max = '13.0'
            l3binningConf   = l3binningHome + 'l3binningConfMcNorthsea_reproc.xml'
            l3binningDatabase = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_northsea_reproc.bindb'
        elif region=='Estonia':
            regionSrcID = 'ESTONIA'
            regiondestID= '_est_'
            lat_min = '57.058884'
            lat_max = '60.57032'
            lon_min = '21.702216'
            lon_max = '30.225435'
            l3binningConf   = l3binningHome + 'l3binningConfMcEstonia_reproc.xml'
            l3binningDatabase = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_estonia_reproc.bindb'
        else:
            regionSrcID = 'BALTIC'
            regiondestID= '_bas_'
            lat_min = '53.0'
            lat_max = '66.0'
            lon_min = '9.0'
            lon_max = '31.0'
            l3binningConf   = l3binningHome + 'l3binningConfMcBalticSea_reproc.xml'
            l3binningDatabase = '/fs14/EOservices/Repositories/MERIS/RR/.l3binning/l3_database_mc_balticsea_reproc.bindb'
            
        # konstante xml-bausteine fuer request
        request_init_block =      "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n"
        request_init_block     += "<RequestList>\n"
        request_init_block     += "    <Request type=\"BINNING\">\n"
        request_init_block     += "        <Parameter name=\"process_type\" value=\"init\" />\n"
        request_init_block     += "        <Parameter name=\"database\" value=\""+l3binningDatabase+"\" />\n"
        request_init_block     += "        <Parameter name=\"lat_min\" value=\""+lat_min+"\" />\n"
        request_init_block     += "        <Parameter name=\"lat_max\" value=\""+lat_max+"\" />\n"
        request_init_block     += "        <Parameter name=\"lon_min\" value=\""+lon_min+"\" />\n"
        request_init_block     += "        <Parameter name=\"lon_max\" value=\""+lon_max+"\" />\n"
        request_init_block     += "        <Parameter name=\"log_prefix\" value=\"l3\" />\n"
        request_init_block     += "        <Parameter name=\"log_to_output\" value=\"false\" />\n"
        request_init_block     += "        <Parameter name=\"resampling_type\" value=\"binning\" />\n"
        request_init_block     += "        <Parameter name=\"grid_cell_size\" value=\""+grid_cell_size+"\" />\n"
        request_init_block     += "        <Parameter name=\"band_name.0\" value=\"chlorophyll_concentration_in_sea_water\" />\n"
        request_init_block     += "        <Parameter name=\"bitmask.0\" value=\"chlorophyll_concentration_in_sea_water != -999.0\" />\n"
        request_init_block     += "        <Parameter name=\"binning_algorithm.0\" value=\"Arithmetic Mean\" />\n"
        request_init_block     += "        <Parameter name=\"weight_coefficient.0\" value=\"1.0\" />\n"
        request_init_block     += "        <Parameter name=\"band_name.1\" value=\"sea_suspended_matter\" />\n"
        request_init_block     += "        <Parameter name=\"bitmask.1\" value=\"sea_suspended_matter != -999.0\" />\n"
        request_init_block     += "        <Parameter name=\"binning_algorithm.1\" value=\"Arithmetic Mean\" />\n"
        request_init_block     += "        <Parameter name=\"weight_coefficient.1\" value=\"1.0\" />\n"
        request_init_block     += "        <Parameter name=\"band_name.2\" value=\"yellow_substance\" />\n"
        request_init_block     += "        <Parameter name=\"bitmask.2\" value=\"yellow_substance != -999.0\" />\n"
        request_init_block     += "        <Parameter name=\"binning_algorithm.2\" value=\"Arithmetic Mean\" />\n"
        request_init_block     += "        <Parameter name=\"weight_coefficient.2\" value=\"1.0\" />\n"
        request_init_block     += "        <Parameter name=\"band_name.3\" value=\"transparency\" />\n"
        request_init_block     += "        <Parameter name=\"bitmask.3\" value=\"transparency != -999.0\" />\n"
        request_init_block     += "        <Parameter name=\"binning_algorithm.3\" value=\"Arithmetic Mean\" />\n"
        request_init_block     += "        <Parameter name=\"weight_coefficient.3\" value=\"1.0\" />\n"
        request_init_block     += "    </Request>\n"
        
        request_update_block    = "    <Request type=\"BINNING\">\n"
        request_update_block   += "        <Parameter name=\"process_type\" value=\"update\" />\n"
        request_update_block   += "        <Parameter name=\"database\" value=\""+l3binningDatabase+"\" />\n"
        request_update_block   += "        <Parameter name=\"log_prefix\" value=\"l3\" />\n"
        request_update_block   += "        <Parameter name=\"log_to_output\" value=\"false\" />\n"
        
        input_prefix =            "        <InputProduct URL=\"file:"
        input_delimiter =         "\" />\n"
        block_close=              "    </Request>\n"
        
        request_finalize_block  = "    <Request type=\"BINNING\">\n"
        request_finalize_block += "       <Parameter name=\"process_type\" value=\"finalize\" />\n"
        request_finalize_block += "        <Parameter name=\"database\" value=\""+l3binningDatabase+"\" />\n"
        request_finalize_block += "        <Parameter name=\"delete_db\" value=\"true\" />\n"
        request_finalize_block += "        <Parameter name=\"log_prefix\" value=\"l3\" />\n"
        request_finalize_block += "        <Parameter name=\"log_to_output\" value=\"false\" />\n"
        request_finalize_block += "        <Parameter name=\"tailoring\" value=\"false\" />\n"
        request_finalize_block += "        <OutputProduct URL=\"file:"
        
        request_closer =         "\" format=\"BEAM-DIMAP\" />\n    </Request>\n</RequestList>\n"
        
        # Inputliste holen
        src_list = os.listdir(srcDir)
        list_size = len(src_list)
        
        # Liste bereinigen um die Datendirectories:
        for a in range(list_size):
            for item in src_list:
                if item.endswith('.data'):
                    src_list.remove(item)

        src_list.sort()
        list_size = len(src_list)
        #KS: added from wew_weekly BSH indicator
        num_days  = len(days)
        print("num_days", num_days)
        print("liste days", days)
        
        # Jetzt nehmen wir nur die Produkte, die in der Liste days sind:
        #old, exchanged with script from WEW with the subsequent block
        #proc_list  = {}
        #proc_count = 0
        #for item in src_list:
       
        #changed range(7) to range(6)! also change for IPF!!! don't know if this is the correct place to change...
        #    for d in range(6):
        #        if item.find(days[d])>0 and item.find(regionSrcID)>0:
        #            print "Adding ", item, "to proc_list"
        #            proc_list[proc_count]=item
        #            proc_count=proc_count+1
        #            break
        proc_list  = {}
        proc_count = 0
        for item in src_list:
            for d in range(num_days):
                #if item.startswith(days[d])==1:    
                if item.find(days[d])>0 and item.find(regionSrcID)>0: 
                    print(days[d]+" found in "+ item)
                    print("Adding ", item, "to proc_list")
                    proc_list[proc_count]=item
                    proc_count=proc_count+1
                    break
        
        entry={}
        for item in proc_list:
            entry[item] = input_prefix + srcDir + proc_list[item] + input_delimiter
        
        output_filename= destDir + days[6]+"_"+days[0]+ regiondestID + "wac_acr_1200.dim"
        print("outpu_filename", output_filename)
        outputDataDir = output_filename[0:len(output_filename)-2] + "ata"
        # Das Produkt soll komplett neu geschrieben werden:
        if os.path.exists(output_filename):
            os.remove(output_filename)
        if os.path.exists(outputDataDir):
            rmtree(outputDataDir)

        # Requestfile soll noch nicht existieren, bzw. altes loeschen:
        if os.path.exists(l3binningConf):
            os.remove(l3binningConf)
        # Erst jetzt wird es erzeugt:
        requestfile = open(l3binningConf, 'a')
        requestfile.write(request_init_block)
        requestfile.write(request_update_block)
        for line in range(len(entry)):
            requestfile.write(entry[line])
        
        requestfile.write(block_close)
        requestfile.write(request_finalize_block+output_filename)
        requestfile.write(request_closer)
        requestfile.close()
        
        l3binningCommand = l3binningScript + " " + l3binningConf
        print(l3binningCommand)
        print("Processing L3...\n")
        os.system(l3binningCommand)

print("\n******************************************************")
print(" Script \'reprocess_MC_weekly_L3_binning.py\' finished. ")
print("******************************************************\n")

# EOF