from os import name
import pytesseract
import PIL.Image
import subprocess

myconfig = r"--psm 3 --oem 3" #config for OCR engine
location=[]
result_name=[]
result_number=[]
mem=["Aused","Easan","Eiwaz","Gudako","Hirako","Hironnad","IAMvne","Izaku","Kako","kcireu","Kokkoro","Kuo","Light","Lucas","Marin","masterhand","Muzo","Nefaerien","Noon","Nyara☆","pat1413","Raz","RCA","Rezael","Tatsumi","TomX204","Yuuki","Yukiito","Yuusha","紫shino"] #change mem list to the current respective list every month

def processData(temp):
   global result_name, result_number, dump
   numbers=[]
   names=[]
   dump=[]
   for word in temp:
      if(word in mem):
         names.append(word) #normal case
      else:
         #if last character of word is not a number -> try comparing letter by letter
         if not (word[-1].isnumeric()):
            names.append(getMostMatched(word))

         #if word is a number, check if it's dmg
         try:
            word=int(word)
            if(word>=600): #make sure number is dmg, not a time indicator 
               numbers.append(word)
            else:
               dump.append(word)
         except:
            dump.append(word)
                  

   #flip the lists to make it chronological
   names=names[::-1]
   numbers=numbers[::-1]
   result_name+=names
   result_number+=numbers
   # return names, numbers

def getMostMatched(name1, name2):
   startingPoint2=0
   startingPoint1=0
   matchCount=0
   matchCountPrevious=0
   mostMatched=mem[0]
   for name2 in mem:
      for i in range(startingPoint2, len(name2)):
         for j in range(startingPoint1, len(name1)):
            if(name1[j]==name2[i]):
               startingPoint2=i+1
               startingPoint1=j+1
               matchCount+=1
               break
      if(matchCount>matchCountPrevious and matchCount>2):
         mostMatched=name2
      else:
         matchCountPrevious=matchCount
         matchCount=0
            
      return mostMatched

def printResult():
   global result_name, result_number, dump
   print('\n',len(result_name),'names', ' ',len(result_number),'dmgs')
   print("\n")
   for item in result_name:
      print(item) #print list of names line by line in order
   print("\n")
   for item in result_number:
      print(item) #print list of dmg numbers line by line in order
   
def printDump():
   global dump
   print("\n")
   print(dump)

for i in range(10):
   location.append( "./screenshots/log"+str(i)+".png") #a list of addresses of image files

for item in location:
   try:
      text = pytesseract.image_to_string(PIL.Image.open(item), config=myconfig) #invoke OCR engine
      temp = text.strip().rstrip('\n').split() #unprocessed text
      processData(temp) #to get processed names and numbers lists
   except:
      print("\n")
      print('Error at: '+item) #if image not found, notify
      pass

printResult()
printDump()
