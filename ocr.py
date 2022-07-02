import pytesseract
import PIL.Image
import subprocess

myconfig = r"--psm 3 --oem 3"
location =[]
numbers=[]
names=[]
mem=["Aused","Easan","Eiwaz","Gudako","Hirako","Hironnad","IAMvne","Izaku","Kako","kcireu","Kokkoro","Kuo","Light","Lucas","Marin","masterhand","Muzo","Nefaerien","Noon","Nyara☆","pat1413","Raz","RCA","Rezael","Tatsumi","TomX204","Yuuki","Yukiito","Yuusha","紫shino"]

def getData(temp):
   for word in temp:
      if(word=='lAMvne' or word=='1AMvne'):
         names.append('IAMvne')
      elif(word in mem):
         names.append(word)
      else:
         try:
            word=int(word)
            numbers.append(word)
         except ValueError:
            pass

for i in range(10):
   location.append( "./temp/test"+str(i)+".png")

for item in location:
   try:
      text = pytesseract.image_to_string(PIL.Image.open(item), config=myconfig)
      temp = text.strip().rstrip('\n').split()
      print(temp)
      getData(temp)
      names=names[::-1]
      numbers=numbers[::-1]
      print("\n")
      for item in names:
         print(item)
      print("\n")
      for item in numbers:
         print(item)
   except:
      print('Image not found at location')
      pass