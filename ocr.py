from os import name
import pytesseract
import PIL.Image
import subprocess

myconfig = r"--psm 3 --oem 3"
location =[]
mem=["Aused","Easan","Eiwaz","Gudako","Hirako","Hironnad","IAMvne","Izaku","Kako","kcireu","Kokkoro","Kuo","Light","Lucas","Marin","masterhand","Muzo","Nefaerien","Noon","Nyara☆","pat1413","Raz","RCA","Rezael","Tatsumi","TomX204","Yuuki","Yukiito","Yuusha","紫shino"]

def processData(temp):
   # global names,numbers
   numbers=[]
   names=[]
   for word in temp:
      if(word=='lAMvne' or word=='1AMvne'):
         names.append('IAMvne')
      elif(word=='#shino' or word=='shino'):
         names.append('紫shino')
      elif(word=='Nyarayy' or word=='Nyara'):
         names.append('Nyara☆')
      elif(word=='Kuo' or word=='Kuo#'):
         names.append('Kuo')
      elif(word in mem):
         names.append(word)
      else:
         try:
            word=int(word)
            numbers.append(word)
         except ValueError:
            pass
   names=names[::-1]
   numbers=numbers[::-1]
   return names, numbers

for i in range(10):
   location.append( "./screenshots/log"+str(i)+".png")

for item in location:
   try:
      text = pytesseract.image_to_string(PIL.Image.open(item), config=myconfig)
      temp = text.strip().rstrip('\n').split() #unprocessed text
      names, numbers = processData(temp) #get processed names and numbers lists

      print("\n")
      for item in names:
         print(item)
      print("\n")
      for item in numbers:
         print(item)
      pass
   except:
      print("\n")
      print('Image not found: '+item)
      pass

