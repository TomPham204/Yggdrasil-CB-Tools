import copy
import os
import pytesseract
import PIL.Image
import glob
import os

myconfig1 = r"--psm 11 --oem 3"
myconfig2 = r"--psm 6 --oem 3"
root=os.path.dirname(os.path.abspath(__file__))
location=[]
dump=[]
bosses=[]

result_name=[]
result_number=[]


mem=["Aused","c cruz 2","Easan","Eiwaz","Gudako","Hirako","Hironnad","IAMvne","Izaku","JonathanR5","Kako","kcireu","Kokkoro","Kuo","Light","Marin","masterhand","Muzo","Nefaerien","Noon","Nyara☆","Raz","Rezael","Screened","Tatsumi","TomX204","Yukiito","Yuuki","Yuusha","紫shino"] #change mem list to the current respective list every month

def processData(temp):
   global result_name
   global result_number
   global dump
   names=[]
   dmgs=[]

   for word in temp:
      if(word in mem):
         names.append(word)
      else:
         try:
            word=int(word)
            if(word>=60):
               dmgs.append(word)
         except:
            mostMatchedName=getMostMatched(word, mem)
            if(mostMatchedName in mem):
               names.append(mostMatchedName)
            else: 
               dump.append(word)

   #flip the lists to make it chronological
   names=names[::-1]
   dmgs=dmgs[::-1]

   for i in names:
      result_name.append(i)
   for i in dmgs:
      result_number.append(i)

def getMostMatched(name1, pickedFrom):
   mostMatchedName='Not found'
   highestMatchCount=3
   
   if(len(name1)<5):
      highestMatchCount=3
   else:
      highestMatchCount=4

   for name2 in pickedFrom:
      characterMatchCount=0
      startingPoint1=0
      startingPoint2=0

      for i in range(startingPoint1, len(name1)):
         for j in range(startingPoint2, len(name2)):
            if(name1[i]==name2[j]):
               startingPoint2=j+1
               startingPoint1=i+1
               characterMatchCount+=1
               break
               
      if(characterMatchCount >= highestMatchCount and abs(len(name2)-len(name1)) < 3):
         mostMatchedName=copy.deepcopy(name2)
         highestMatchCount=copy.deepcopy(characterMatchCount)
   return mostMatchedName

def getOCRDataAndProcess(currentConfig):
   imgDirs=glob.glob(root + "/screenshots/*.png")

   for item in imgDirs:
      try:
         text = pytesseract.image_to_string(PIL.Image.open(item), config=currentConfig) 
         temp = text.strip().rstrip('\n').split()
         processData(temp)
      except:
         print("Error at " + item)
         pass
   
   if(len(result_name)==len(result_number)):
      for item in imgDirs:
         try:
            os.remove(item)
         except:
            pass

   print("\n","#name: ", len(result_name), ", #dmg: ", len(result_number))
   for i in result_name:
      print(i)
   print()
   for i in result_number:
      print(i)

def cleanup():
   global dump, result_number, result_name, location
   dump=[]
   result_name=[]
   result_number=[]
   location=[]

getOCRDataAndProcess(myconfig1)
cleanup()
getOCRDataAndProcess(myconfig2)

for item in location:
   try:
      os.remove(item)
   except:
      pass
