import os
import pandas as pd
LOCATION = str(os.path.dirname(os.path.abspath(__file__)) + "/Yggdrasil Clan Resource Spreadsheet.xlsx")
CURRENT_SHEET = 'February 2022 Battle Log'
OLD_SHEET = 'February 2022 Battle Log'

def getNewData():
    global LOCATION, CURRENT_SHEET
    MEM=[]
    ATTEMPTS=[]
    DMG=[]
    temp1=[]
    temp2=[]

    #get non repeated member list
    wb=pd.read_excel(LOCATION, sheet_name=CURRENT_SHEET)
    MEM=list(set(wb['Player Name'].values))
    MEM.sort()

    #clone sheet's data
    temp1=wb['Player Name'].values
    temp2=wb['Damage Dealt'].values
    temp3=wb['Note'].values

    #find out actual number of attempts (doesn't count carried-over attempts)
    for name in MEM:
        ATTEMPTS.append(0)
        DMG.append(0)
    for i in range(len(temp1)):
        for j in range(len(MEM)):
            if (MEM[j]==temp1[i]): #player name matches the current member's count search
                DMG[j]+=temp2[i]
                if(temp3[i]=='overkill'):
                    pass
                else:
                    ATTEMPTS[j]+=1
    
    return MEM, DMG, ATTEMPTS

def getOldData():
    global LOCATION, OLD_SHEET
    MEM_OLD=[]
    ATTEMPTS_OLD=[]
    DMG_OLD=[]
    temp1=[]
    temp2=[]

    #get non repeated MEM_OLDber list
    wb_old=pd.read_excel(LOCATION, sheet_name=OLD_SHEET)
    MEM_OLD=list(set(wb_old['Player Name'].values))
    MEM_OLD.sort()

    #clone sheet's data
    temp1=wb_old['Player Name'].values
    temp2=wb_old['Damage Dealt'].values
    temp3=wb_old['Note'].values

    #find out actual number of ATTEMPTS_OLD (doesn't count carried-over ATTEMPTS_OLD)
    for name in MEM_OLD:
        ATTEMPTS_OLD.append(0)
        DMG_OLD.append(0)
    for i in range(len(temp1)):
        for j in range(len(MEM_OLD)):
            if (MEM_OLD[j]==temp1[i]): #player name matches the current MEM_OLDber's count search
                DMG_OLD[j]+=temp2[i]
                if(temp3[i]=='overkill'):
                    pass
                else:
                    ATTEMPTS_OLD[j]+=1
    
    return MEM_OLD, DMG_OLD, ATTEMPTS_OLD

def calcAvgDmg(ATTEMPTS, DMG):
    AVG=[]
    for i in range(len(ATTEMPTS)):
        AVG.append(round(DMG[i]/ATTEMPTS[i]))
    return AVG

def compareResults(MEM_OLD, MEM, AVG_OLD, AVG, DMG_OLD, DMG, type="AVERAGE"):
    RESULT=[]
    for i in range(len(MEM)):
        RESULT.append('N/A')

        for j in range(len(MEM_OLD)):
            if(MEM[i]==MEM_OLD[j]): #check if member exists in both list to compare
                if(type=="AVERAGE"):
                    percent = abs(AVG[i] - AVG_OLD[j]) / AVG_OLD[j] * 100
                    if(AVG[i]>=AVG_OLD[j]):
                        RESULT[i]='Increased by ' + str(round(percent)) + '%'
                    else:
                        RESULT[i]='Decreased by ' + str(round(percent)) + '%'
                else:
                    percent = abs(DMG[i] - DMG_OLD[j]) / DMG_OLD[j] * 100
                    if(DMG[i]>=DMG_OLD[j]):
                        RESULT[i]='Increased by ' + str(round(percent)) + '%'
                    else:
                        RESULT[i]='Decreased by ' + str(round(percent)) + '%'
            else:
                pass
    return RESULT

#only for Feb CB
# AVG_OLD = [1182328,1315201,596946,998331,1245677,1040863,438701,1477537,1923116,716683,1489071,1050596,1878995,848699,1164543,1778727,1234709,879743,1787895,1266997,2015631,827070,1122113,1984612,962522,499892,1602814,974992,1853755,1455754]
# MEM_OLD = ['Aeongie','Anjelly','Aused','Easan','FLus','Glacel','Half','Hirako','Hironnad','IAMvne','Ivy','Izaku','Kako','Kokkoro','Lucas','Mumrik','Nefaerien','NiR','Nyara☆','RCA','Raz','Rezael','Tatsumi','TomX204','Yukiito','Yuuki','kcireu','pat1413','⬛⬛ Mya ⬛⬛','紫shino']

#get data
MEM, DMG, ATTEMPTS = getNewData()
MEM_OLD, DMG_OLD, ATTEMPTS_OLD = getOldData()

#process data
AVG = calcAvgDmg(ATTEMPTS, DMG)
AVG_OLD = calcAvgDmg(ATTEMPTS_OLD, DMG_OLD)

RESULT_AVG=compareResults(MEM_OLD, MEM, AVG_OLD, AVG, DMG_OLD, DMG, type="AVERAGE")
RESULT_TOTAL=compareResults(MEM_OLD, MEM, AVG_OLD, AVG, DMG_OLD, DMG, type="TOTAL")

#print result
print("Comparing average damage")
for i in range(len(MEM)):
    print(MEM[i],':', RESULT_AVG[i])

print("\nComparing total damage")
for i in range(len(MEM)):
    print(MEM[i],':', RESULT_TOTAL[i])