from urllib.request import Request, urlopen
from random import randint as r
from bs4 import BeautifulSoup
from rich import print as rprint
import threading
import time
from rich.progress import Progress
import sys,os
import cv2




a = "azertyuiopqsdfghjklmwxcvbn01234456789"
def g(strlen):
	txt = ""
	for _ in range(strlen):
		txt += a[r(0,len(a)-1)]
	return txt

# Var
opt = ["-v","-c"]



def startSearch(verbos,nb):
	cpt = 0
	ended = False
	face_cascade = cv2.CascadeClassifier('face_detector.xml')
	url="https://prnt.sc/"
	with Progress() as progress:

		task1 = progress.add_task("[red]Searching img...", total=100)
		task1_step = 100/nb_img

		# NB
		while not ended:
			#code = "ios201"
			code = g(r(4,6))
			if not code in seen:
				myUrl = url + code
				if verbos :
					task2 = progress.add_task("[yellow]Request URL ...", total=100)
				req = Request(myUrl, headers={'User-Agent': 'Mozilla/5.0'})
				if verbos :
					progress.update(task2, advance=25)
				seen.append(code)
				web_byte = urlopen(req).read()
				if verbos :
					progress.update(task2, advance=25)
				webpage = web_byte.decode('utf-8')
				soup = BeautifulSoup(webpage ,features="html.parser")
				if verbos :
					progress.update(task2, advance=25)
				data = soup.find_all("img",class_="screenshot-image")
				if len(data)>0:
					data = data[0]
					if verbos :
						progress.update(task2, advance=25)
					if data['src'] != "//st.prntscr.com/2022/09/11/1722/img/0_173a7b_211be8ff.png":
						cpt +=1
						progress.update(task1, advance=task1_step)
						ended = cpt == nb_img
						urlImg = data['src']
						req2 = Request(urlImg, headers={'User-Agent': 'Mozilla/5.0'})
						try :
							web_byte = urlopen(req2).read()
							open('image/'+code+'.png','wb').write(web_byte)
							img = cv2.imread('image/'+code+'.png')
							faces = face_cascade.detectMultiScale(img, 1.1, 4)
							if len(faces) >0:
								if verbos :
									rprint('[white]Found Faces')
								open('image/face/'+code+'.png','wb').write(open('image/'+code+'.png','rb').read())
								os.remove('image/'+code+'.png')
						except Exception as e:
							if verbos :
								rprint(e)

def checkUpdate():
	pass


if __name__ == '__main__':
	checkUpdate()
	# Load memory
	seen = open("memory.txt","r").read().split(";")
	#Check Opt
	nb_img = int(input("Nb of images : "))
	verbos = False
	for option in sys.argv:
		if option in opt :
			data = option[1:]
			if data == "c":
				for path,dirs,files in os.walk("."):
					for file in files:
						if file.endswith(".png"):
							os.remove(path+"/"+file)
				rprint('[green] Successfully clean !')
			if data == "v":
				verbos = True	
	startSearch(verbos,nb_img)
	#Save memory
	open("memory.txt","w").write(";".join(seen))