# read WCNSS_qcom_cfg.ini and check specific parameter exists
# if not, add it

fn = 'WCNSS_qcom_cfg.ini'
param_list = [['gEnableBmps','gEnableImps'],['gDot11Mode'],['BandCapability'],['gTxBFEnable','gEnableMuBformee'],['FastRoamEnabled','gEnableFWRssiMonitoring','FastTransitionEnabled','gEnableDFSChnlScan']]
value_list = [['0','0'],['0'],['0'],['0','0'],['0','0','0','0']]
paramExist_list=[['0','0'],['0'],['0'],['0','0'],['0','0','0','0']]
mode = 0

###########################
# Menu & Input
###########################
print("\rPlease select which item you want to run :\n")
type = int(input ("(1)Disable power save (2)Change STA network mode (3)Set band capability (4)Disable TX beamforming/MU-MIMO (5)Disable Roaming....\n"))
if type == 1:
    print("Disable power save...\n")
elif type == 2:
    mode = input("1 = 11abg, 2 = 11b, 3 = 11g, 4 = 11n, 5 = 11g only, 6 = 11n only 7 = 11b only 8 = 11ac only, 9 = 11ac, 12 = 11ax....\n")
    if int(mode) > 12:
        print("Wrong mode")
        exit()
elif type == 3:
    mode = input("0=all,1=2.4G only,2=5G only....\n")
    if int(mode) > 2:
        print("Wrong mode")
        exit()
elif type == 4:
    print("Disable TX beamforming/MU-MIMO...\n")
elif type == 5:
    print("Disable Roaming...\n")    
else :
    exit()

###########################
# File Read
###########################

with open(fn) as file_obj:
    obj_list = file_obj.readlines()

###########################
# Modify exist parameter
###########################

index = 0
type = type-1
for line in obj_list:
    index_param = 0
    if line == '\n':
        #print("Blank line...")
        obj_list.pop(index)  
    if  (line != '\n') and ('=' not in line):
        if ('#' not in line) :
            if('END' not in line):
                print(line)
                print("File type error in line ",index)
                exit()
    for param in param_list[type]:
        if (param in line) and ('#' not in line):
            if type == 1:
                value = mode
            elif type == 2:
                value = mode
            else :
                value = value_list[type][index_param]
            print('param: ', param)
            print('value: ', value)
            obj_list[index] = param + '=' + value + '\n'
            paramExist_list[type][index_param] = '1'
            break
        index_param += 1    
    index += 1    

###########################
# Insert non exist parameter
###########################

index_param = 0
new_line_insert = 0
for paramExist in paramExist_list[type]:
    if paramExist == '0':
        param = param_list[type][index_param]
        if type == 1:
            value = mode
        elif type ==2:
            value = mode
        else :
            value = value_list[type][index_param]
        print('param: ', param)
        print('value: ', value)
        obj_list.insert(0,param + '=' + value + '\n')
        new_line_insert = 1
    index_param += 1

if new_line_insert == 1:
    obj_list.insert(0,'# New ini parameter added here'+'\n')

################
# Write to file
################

with open(fn, 'w') as file_obj:
    file_obj.writelines(obj_list)
    file_obj.close()


