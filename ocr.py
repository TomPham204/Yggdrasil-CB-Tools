import copy
import pytesseract
import PIL.Image

myconfig = r"--psm 3 --oem 3" #config for OCR engine
location=[]

names=[]
dmgs=[]
dump=[]

result_name=[]
result_number=[]

mem=["Aused","Easan","Eiwaz","Gudako","Hirako","Hironnad","IAMvne","Izaku","Kako","kcireu","Kokkoro","Kuo","Light","Lucas","Marin","masterhand","Muzo","Nefaerien","Noon","Nyara☆","pat1413","Raz","RCA","Rezael","Tatsumi","TomX204","Yuuki","Yukiito","Yuusha","紫shino"] #change mem list to the current respective list every month

def processData(temp):
   global mem, names, dmgs, dump, result_number, result_name
   for word in temp:
      if(word in mem):
         names.append(word) #normal case
      else:
         #if last character of word is not a number -> try comparing letter by letter
         if not(word[-1].isnumeric()):
            mostMatchedName=getMostMatched(word)
            if(mostMatchedName!='0'):
               names.append(mostMatchedName)
         else:
            #if word is a number, check if it's dmg
            try:
               word=int(word)
               if(word>=60): #make sure number is dmg, not a time indicator 
                  dmgs.append(word)
               else:
                  dump.append(word)
            except:
               dump.append(word) 

   #flip the lists to make it chronological
   names=names[::-1]
   dmgs=dmgs[::-1]
   result_name+=names
   result_number+=dmgs
   names=[]
   dmgs=[]

def getMostMatched(name1):
   global mem
   highestMatchCount=4
   mostMatchedName='0'

   for name2 in mem:
      matchCount=0
      startingPoint2=0
      startingPoint1=0
      for i in range(startingPoint2, len(name2)):
         for j in range(startingPoint1, len(name1)):
            if(name1[j]==name2[i]):
               startingPoint2=i+1
               startingPoint1=j+1
               matchCount+=1
               break
      if(matchCount > highestMatchCount):
         mostMatchedName=copy.deepcopy(name2)
         highestMatchCount=copy.deepcopy(matchCount)
         
   return mostMatchedName

def printResult():
   global mem, names, dmgs, result_number, result_name
   print('\n',len(result_name),'names', ' ',len(result_number),'dmgs')
   print("\n")
   for item in result_name:
      print(item) #print list of names line by line in order
   print("\n")
   for item in result_number:
      print(item) #print list of dmg dmgs line by line in order
   
def printDump():
   global dump
   print("\n")
   print('Dumps: ',dump)

def getOCRData():
   for i in range(10):
      location.append( "./screenshots/log"+str(i)+".png") #a list of addresses of image files

   for item in location:
      try:
         text = pytesseract.image_to_string(PIL.Image.open(item), config=myconfig) #invoke OCR engine
         temp = text.strip().rstrip('\n').split() #unprocessed text
         processData(temp) #to get processed names and dmgs lists
      except:
         print('Not found: '+item) #if image not found, notify

getOCRData()
printResult()
printDump()
