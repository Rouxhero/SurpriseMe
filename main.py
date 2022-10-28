from urllib.request import Request, urlopen ,urlcleanup
import urllib
from random import randint as r
from bs4 import BeautifulSoup
from rich import print as rprint
import threading
import time
from rich.progress import Progress
import sys,os
import cv2
from time import perf_counter



a = "azertyuiopqsdfghjklmwxcvbn01234456789"
def g(strlen):
	txt = ""
	for _ in range(strlen):
		txt += a[r(0,len(a)-1)]
	return txt

# Var
opt = ["-v","-c"]



def startSearch(verbos,nb_img,task1,task1_step):
	cpt = 0
	ended = False
	face_cascade = cv2.CascadeClassifier('face_detector.xml')
	url="https://prnt.sc/"
	# NB
	while not ended:
		#code = "ios201"
		code = g(r(4,6))
		if not code in seen:
			myUrl = url + code
			if verbos :
				task2 = progress.add_task("[yellow]Request URL ...", total=100)
			data =[]
			try :
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
			except Exception as e:
				if verbos:
					rprint(f"[red]Error : {e}")
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
	urlcleanup()
	url = "https://raw.githubusercontent.com/Rouxhero/SurpriseMe/master/version"
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	web_byte = urlopen(req).read()
	lasted_version = int(web_byte.decode('utf-8'))
	current_version = int(open('version','r').read())
	rprint(lasted_version,current_version)
	if lasted_version > current_version:
		rprint('[green] New version available. Updating version')
		main_file = "https://raw.githubusercontent.com/Rouxhero/SurpriseMe/master/main.py"
		req = Request(main_file, headers={'User-Agent': 'Mozilla/5.0'})
		web_byte = urlopen(req).read()
		open('main.py',"w").write(web_byte.decode('utf-8'))
		open('version',"w").write(str(lasted_version))
		rprint('[green] Update Success, please restart')
		exit()



if __name__ == '__main__':
	checkUpdate()
	# Load memory
	try :
		seen = open("memory.txt","r").read().split(";")
	except Exception:
		seen = []
		open("memory.txt","a").close()
	#Check Opt
	nb_img = int(input("Nb of images : "))
	nb_thread = int(input("Num of threads : "))
	if (nb_thread>5):
		rprint('[yellow] WARNING: Over 5 threads, you should be ban ip !')
		rprint('[red] ERROR : Security failure, please enter a number of threads less than 5 !')
		exit()
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

	with Progress() as progress:
		task1 = progress.add_task("[red]Searching img...", total=100)
		task1_step = 100/nb_img
		start = perf_counter()
		if nb_thread == 1:
			startSearch(verbos,nb_img,task1,task1_step)
		else:
			myThread = []
			if verbos:
				rprint('[green] Starting ',nb_thread,' threads')
			cptt = nb_img
			for _ in range(nb_thread-1):
				if verbos:
					rprint('[green] Starting a thread for ',nb_img//nb_thread)
				cptt-= nb_img//nb_thread
				myThread.append(threading.Thread(target=startSearch,args=(verbos,nb_img//nb_thread,task1,task1_step,)))
				myThread[-1].start()
				time.sleep(0.25)
			if verbos:
				rprint('[green] Starting a thread for ',cptt)
			myThread.append(threading.Thread(target=startSearch,args=(verbos,cptt,task1,task1_step,)))
			myThread[-1].start() 
			for t in myThread:
				t.join()
		end = perf_counter()
		rprint(f"[yellow]Time taken: {(end-start)}s")
	#Save memory
	open("memory.txt","w").write(";".join(seen))