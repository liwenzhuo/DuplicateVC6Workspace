import os
import re
import shutil

listexts = ("cpp","h","c","cc","tlh","tli","dsw","dsp","txt","hpp","rc","rc2","def")

def DuplicateProject():
	oriprjpath = input("Please input the original project path:")
	
	if not os.path.exists(oriprjpath):
		print('Not a valid path')
		return

	repprj = input("Please input the new name of project:")

	sp = os.path.split(oriprjpath)
	higherdir = sp[0]
	oriprjname = sp[1]

	newprjpath = os.path.join(higherdir, repprj)

	if os.path.exists(newprjpath):
		shutil.rmtree(newprjpath)

	shutil.copytree(oriprjpath, newprjpath)

	newprjname = os.path.split(newprjpath)[1]
	RenameFile(newprjpath, newprjname, oriprjname)

	ReplaceInFile(newprjpath, newprjname, oriprjname)
	return

def RenameFile(newprjpath, newprjname, oriprjname):
	names = os.listdir(newprjpath)
	for name in names:
		srcname = os.path.join(newprjpath,name)
		if os.path.isdir(srcname):
			RenameFile(srcname, newprjname, oriprjname)
		else:
			if name.find(oriprjname) != -1:
				ofi = name.replace(oriprjname, newprjname)
				dstname = os.path.join(newprjpath, ofi)
				os.rename(srcname, dstname)
			#sp = os.path.splitext(name)
			#fn = sp[0]#fn的前面也可能包含oriprjname
			#ext = sp[1]
			#if fn == oriprjname:
			#	ofi = newprjname + ext
			#	dstname = os.path.join(newprjpath,ofi)
			#	os.rename(srcname, dstname)
	return

def ReplaceInFile(newprjpath, newprjname, oriprjname):
	names = os.listdir(newprjpath)
	lowre = re.compile(oriprjname)
	upperre = re.compile(oriprjname.upper())
	for name in names:
		srcname = os.path.join(newprjpath, name)
		if os.path.isdir(srcname):
			ReplaceInFile(srcname, newprjname, oriprjname)
		else:
			bisaneed_rep_file = False
			ext = os.path.splitext(srcname)[1][1:]
			for e in listexts:
				if e == ext:
					bisaneed_rep_file = True

			if bisaneed_rep_file:
				fp = open(srcname)
				text = fp.read()
				fp.close()  

				#ost = re.sub(oriprjname, newprjname, text)
				ost = lowre.sub(newprjname, text)
				ost = upperre.sub(newprjname.upper(), ost)
				fp = open(srcname, 'w')
				fp.write(ost)
				fp.close()
	return


DuplicateProject()