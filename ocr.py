import pytesseract
import PIL.Image

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
   names=names[::-1]
   numbers=numbers[::-1]

for i in range(10):
   location.append( "./temp/log"+str(i)+".png")
print(location)

for item in location:
   try:
      text = pytesseract.image_to_string(PIL.Image.open(item), config=myconfig)
      temp = text.strip().rstrip('\n').split()
      getData(temp)

      print("\n")
      for item in names:
         print(item)
      print("\n")
      for item in numbers:
         print(item)
      names=[]
      numbers=[]
   except:
      print('Image not found: '+item)
      pass