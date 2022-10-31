import copy
import pytesseract
import PIL.Image

myconfig = r"--psm 3 --oem 3" #don't change, config for OCR engine
location=[]
names=[]
dmgs=[]
dump=[]
bosses=[]

result_name=[]
result_number=[]
result_boss=[]


mem=["Aused","Easan","Eiwaz","Gudako","Hirako","Hironnad","IAMvne","Izaku","Kako","kcireu","Kokkoro","Kuo","Light","Lucas","Marin","masterhand","Muzo","Nefaerien","Noon","Nyara☆","pat1413","Raz","RCA","Rezael","Tatsumi","TomX204","Yuuki","Yukiito","Yuusha","紫shino"] #change mem list to the current respective list every month

boss=["Goblin", "Rai-Rai", "Needle", "Cyclops", "Lesathapult", "Wyvern", "Gryphon", "Prisma", "Ulfhedinn", "Medusa", "Wraithlord", "Gargoyle", "Glutton", "Sloth", "Orc", "Titanoturtle", "Orleon", "Torpedon", "Mushussu", "Night", "Mesarthim", "Lapahn", "Bear", "Minotaurus", "Raiden", "Pigs", "Tritem", "Drake", "Nepterion", "Karkinos", "Horn", "Sagittarius", "Algedi", "Aquarius", "Valkyrie"]

def processData(temp):
   global mem, names, bosses, dmgs, dump, result_number, result_name, result_boss

   for word in temp:
      if(word in mem):
         names.append(word)
      elif(word in boss):
         bosses.append(word)
      else:
         #if last character of word is not a number -> try comparing letter by letter
         if not(word[-1].isnumeric()):
            mostMatchedName=getMostMatched(word, len(word), mem)
            if(mostMatchedName in mem):
               names.append(mostMatchedName)
            else:
               mostMatchedBoss=getMostMatched(word, len(word), boss)
               if(mostMatchedBoss in boss):
                  bosses.append(mostMatchedName)
               if(mostMatchedBoss=='0'):
                  dump.append(word)
               else:
                  bosses.append(word)
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
   bosses=bosses[::-1]
   bosses[:]=(value for value in bosses if value!='0')

   result_name+=names
   result_number+=dmgs
   result_boss+=bosses

   names=[]
   dmgs=[]
   bosses=[]

def getMostMatched(name1, length, pickedFrom):
   mostMatchedName='0'
   highestMatchCount=4
   
   if(length<5):
      highestMatchCount=2
   else:
      highestMatchCount=4

   for name2 in pickedFrom:
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
   global result_number, result_name, result_boss

   print('\n',len(result_name),'names', ' ',len(result_number),'dmgs',' ',len(result_boss), 'bosses')
   
   print("\n")
   for item in result_name:
      print(item) #print list of names line by line in order
   print("\n")
   for item in result_number:
      print(item) #print list of dmgs line by line in order
   print("\n")
   for item in result_boss:
      print(item) #print list of bosses line by line in order
   
def printDump():
   print("\n")
   print('Dump: ',dump)

def getOCRDataAndProcess():
   for i in range(15):
      location.append( "./screenshots/log"+str(i)+".png") #a list of addresses of image files

   for item in location:
      try:
         text = pytesseract.image_to_string(PIL.Image.open(item), config=myconfig) #invoke OCR engine
         temp = text.strip().rstrip('\n').split() #unprocessed text
         processData(temp) #to get processed names and dmgs lists
      except:
         print('Not found: ' + item) #if image not found, notify
   
      try: 
         result_boss.remove("Wild")
      except:
         pass

def cleanup():
   global mem, names, dmgs, bosses, dump, result_number, result_name, result_boss
   del mem, names, dmgs, bosses, dump, result_number, result_name, result_boss

getOCRDataAndProcess()
printResult()
# printDump()
cleanup()
