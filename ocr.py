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
   global result_name, result_number
   numbers=[]
   names=[]
   for word in temp:
      #some special cases
      if(word=='lAMvne' or word=='1AMvne'):
         names.append('IAMvne')
      elif(word=='#shino' or word=='shino'):
         names.append('紫shino')
      elif(word=='Nyarayy' or word=='Nyara'):
         names.append('Nyara☆')
      elif(word=='Kuo' or word=='Kuo#'):
         names.append('Kuo')
         #normal case
      elif(word in mem):
         names.append(word)
      #if not name of player
      else:
         try:
            word=int(word) #if is a number -> dmg number
            if(word>=60): #make sure if number is not a time indicator 
               numbers.append(word)
         except ValueError:
            pass #if not a number, skip that value

   #flip the lists to make it chronological
   names=names[::-1]
   numbers=numbers[::-1]
   result_name+=names
   result_number+=numbers
   # return names, numbers

def printResult():
   global result_name, result_number
   print("\n")
   for item in result_name:
      print(item) #print list of names line by line in order
   print("\n")
   for item in result_number:
      print(item) #print list of dmg numbers line by line in order


for i in range(10):
   location.append( "./screenshots/log"+str(i)+".png") #a list of addresses of image files

for item in location:
   try:
      text = pytesseract.image_to_string(PIL.Image.open(item), config=myconfig) #invoke OCR engine
      temp = text.strip().rstrip('\n').split() #unprocessed text
      processData(temp) #get processed names and numbers lists
   except:
      print("\n")
      print('Error at: '+item) #if image not found, notify
      pass

printResult()
