import math
import random
import os
import time

example_of_chunkedfile = {
	"ID": {
		"filename":"",
		"filedir":"",
		"filesize":0,
		"chunksize":0,
		"parts":[
			["chunk_{id}",0] # chunk part name , cunk part size
		]
	}
}

size_table = {
	"b":1,
	"kb":10,
	"mb":20,
	"gb":30,
	"tb":40
}

# clustering mathod
class ChunkTools:
	def __init__(self):
		self.files = {}

	def __serial(self,numbs):
		hashs = 'abcdefghihklmnopqrstuv1234567890'.upper()
		output = [hashs[random.randint(0,len(hashs)-1)] for x in range(numbs)]
		return ''.join(output)
	
	def getCompParts(self,path:str,chunksize:str):
		tls = time.time()
		fhb,chsize,chlist,idxs = None,None,[],0
		try:
			with open(path,"rb") as fs:
				fhb = fs.read()
				fs.close()
		except Exception as EXP: return False,EXP
		else:
			chsize = float(chunksize.split("|")[0]) * (2**size_table[chunksize.split("|")[1]])
			chsize = round(chsize)

			if len(fhb)//chsize > 0:
				for x in range(len(fhb)//chsize):
					chlist.append(fhb[chsize*idxs:chsize*(idxs+1)])
				if len(fhb)%chsize:
					chlist.append(fhb[chsize*idxs:])
			else:
				if len(fhb)%chsize:
					chlist.append(fhb)

			yield chlist
			del fhb,chsize,chlist,chlist

	def compFile(self,path:str,chunksize:str,progress_checker=None):
		tls = time.time()
		fhb,chsize,fserial,chlist,idxs = None,None,None,[],0
		try:
			with open(path,"rb") as fs:
				fhb = fs.read()
				fs.close()
		except Exception as EXP: return False,EXP
		else:
			chsize = float(chunksize.split("|")[0]) * (2**size_table[chunksize.split("|")[1]])
			chsize = round(chsize)

			if progress_checker:
				progress_checker(0)

			fserial = self.__serial(10)

			if len(fhb)//chsize > 0:
				for x in range(len(fhb)//chsize):
					with open(f"chunks/{fserial}_chunk_{idxs+1}.sxach","wb") as fs:
						fs.write(fhb[chsize*idxs:chsize*(idxs+1)])
						fs.close()
					chlist.append([f"chunks/{fserial}_chunk_{idxs+1}.sxach",chsize])
					idxs += 1
					if progress_checker:
						progress_checker(round((idxs / len(fhb)) * 100))
				if len(fhb)%chsize:
					with open(f"chunks/{fserial}_chunk_{idxs+1}.sxach","wb") as fs:
						fs.write(fhb[chsize*idxs:])
						fs.close()
					chlist.append([f"chunks/{fserial}_chunk_{idxs+1}.sxach",len(fhb[chsize*idxs:])])
					if progress_checker:
						progress_checker(100)
			else:
				if len(fhb)%chsize:
					with open(f"chunks/{fserial}_chunk_{idxs+1}.sxach","wb") as fs:
						fs.write(fhb)
						fs.close()
					chlist.append([f"chunks/{fserial}_chunk_{idxs+1}.sxach",len(fhb)])
					if progress_checker:
						progress_checker(100)

			
			self.files[fserial] = {
				"filename":path.split('/')[-1],
				"filedir":os.getcwd().replace("\\","/") + "/" + path,
				"filesize":len(fhb),
				"chunksize":chsize,
				"parts": chlist
			}

			print(f"File [{self.files[fserial]['filename']}] Compressed With Serial[{fserial}]|ChunkSize[{chsize}]|Length[{len(chlist)}]|Time[{time.time()-tls:.04f}-s]")

			del fhb,chsize,chlist,idxs

			return fserial,self.files[fserial]
		
	def decompFile(self,path:str,fserial:str,removeolds:bool = False):
		tls = time.time()
		try:
			fbuff = self.files[fserial]
			clbuff = b''
		except Exception as EXP: return False,EXP
		else:
			for x in fbuff['parts']:
				with open(x[0],"rb") as fs:
					clbuff += fs.read()
					fs.close()
			
			with open(path,"wb") as fs:
				fs.write(clbuff)
				fs.close()
			
			print(f"File [{fbuff['filename']}] Decompress To Path [{path}] Time[{time.time()-tls}-ms]")