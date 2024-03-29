import os
import pandas as pd
from math import nan, isnan

LOCATION = str(os.path.dirname(os.path.abspath(__file__)) + "/Yggdrasil Resource.xlsx")
CURRENT_SHEET = 'October 2022'
OLD_SHEET = 'September 2022'
CURRENT_LAST_ROW=518-1 #-1 because the first row is header row
OLD_LAST_ROW=508-1

def getNewData():
    global LOCATION, CURRENT_SHEET
    MEM=[]
    ATTEMPTS=[]
    DMG=[]
    temp1=[]
    temp2=[]
    temp3=[]

    #get non repeated member list
    wb=pd.read_excel(LOCATION, sheet_name=CURRENT_SHEET, nrows=CURRENT_LAST_ROW)
    MEM=list(set(wb['Player'].values))
    MEM.sort()

    #clone sheet's data
    temp1=wb['Player'].values
    temp2=wb['Damage'].values
    temp3=wb['OvK'].values

    #find out actual number of attempts (doesn't count carried-over attempts)
    for name in MEM:
        ATTEMPTS.append(0)
        DMG.append(0)
    for i in range(len(temp1)):
        for j in range(len(MEM)):
            if (MEM[j]==temp1[i]): #player name matches the current member's count search
                DMG[j]+=temp2[i]
                if(temp3[i]=='y'):
                    pass
                else:
                    ATTEMPTS[j]+=1
    
    return MEM, DMG, ATTEMPTS

def getOldData():
    global LOCATION, OLD_SHEET
    MEM_OLD=[]
    ATTEMPTS_OLD=[]
    DMG_OLD=[]

    #get non repeated member_old list
    wb_old=pd.read_excel(LOCATION, sheet_name=OLD_SHEET, nrows=OLD_LAST_ROW)
    MEM_OLD=list(set(wb_old['Player'].values))
    MEM_OLD.sort()

    #clone sheet's data
    temp1=wb_old['Player'].values
    temp2=wb_old['Damage'].values
    temp3=wb_old['OvK'].values

    #find out actual number of ATTEMPTS_OLD (doesn't count carried-over ATTEMPTS_OLD)
    for name in MEM_OLD:
        ATTEMPTS_OLD.append(0)
        DMG_OLD.append(0)
    for i in range(len(temp1)):
        for j in range(len(MEM_OLD)):
            if (MEM_OLD[j]==temp1[i]): #player name matches the current MEM_OLDber's count search
                DMG_OLD[j]+=temp2[i]
                if(temp3[i]=='y'):
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

def printResult(MEM, RESULT_AVG, RESULT_TOTAL):
    #print result
    print("\nComparing average damage")
    for i in range(len(MEM)):
        print(MEM[i],':', RESULT_AVG[i])

    print("\nComparing total damage")
    for i in range(len(MEM)):
        print(MEM[i],':', RESULT_TOTAL[i])

def printVerify(MEM, MEM_OLD):
    print('\nOLD:', len(MEM_OLD), 'CURRENT:', len(MEM),'\n')
    print('OLD MEM')
    for i in range(len(MEM_OLD)):
        print(MEM_OLD[i])
    print('\nCURRENT MEM')
    for i in range(len(MEM)):
        print(MEM[i])

################################################################################################################################

#get data
MEM, DMG, ATTEMPTS = getNewData()
MEM_OLD, DMG_OLD, ATTEMPTS_OLD = getOldData()

#process data
AVG = calcAvgDmg(ATTEMPTS, DMG)
AVG_OLD = calcAvgDmg(ATTEMPTS_OLD, DMG_OLD)

RESULT_AVG=compareResults(MEM_OLD, MEM, AVG_OLD, AVG, DMG_OLD, DMG, type="AVERAGE")
RESULT_TOTAL=compareResults(MEM_OLD, MEM, AVG_OLD, AVG, DMG_OLD, DMG, type="TOTAL")

#print result
printVerify(MEM,MEM_OLD)
printResult(MEM, RESULT_AVG, RESULT_TOTAL)
