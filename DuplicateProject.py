# -*- coding: utf-8 -*-
import os
import re
import shutil
import codecs

listexts = ("cpp", "h", "c", "cc", "tlh", "tli", "dsw", "dsp", "txt", "hpp", "rc", "rc2", "def", "sln", "vcproj", "vcxproj", "filters")
encs = ("gbk", "utf-8", "utf-16-le", "utf-16-be")

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
    RenameFileFolder(newprjpath, newprjname, oriprjname)

    ReplaceInFile(newprjpath, newprjname, oriprjname)
    return

def RenameFileFolder(path, newprjname, oriprjname):
    names = os.listdir(path)
    for name in names:
        srcname = os.path.join(path,name)
        if os.path.isdir(srcname):
            RenameFileFolder(srcname, newprjname, oriprjname)
            if name == oriprjname:
                dstdirname = os.path.join(path, newprjname)
                srcdirname = os.path.join(path, name)
                os.rename(srcdirname, dstdirname)
        else:
            if name.find(oriprjname) != -1:
                ofi = name.replace(oriprjname, newprjname)
                dstname = os.path.join(path, ofi)
                os.rename(srcname, dstname)
            #sp = os.path.splitext(name)
            #fn = sp[0]#fn的前面也可能包含oriprjname
            #ext = sp[1]
            #if fn == oriprjname:
            #    ofi = newprjname + ext
            #    dstname = os.path.join(path,ofi)
            #    os.rename(srcname, dstname)
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
            for ex in listexts:
                if ex == ext:
                    bisaneed_rep_file = True

            if bisaneed_rep_file:
                en = ""
                for e in encs:
                    try:
                        fh = codecs.open(srcname, 'r', encoding=e)
                        fh.readline()
                        fh.close()
                    except UnicodeDecodeError:
                        print('got unicode error with', e, 'trying different encoding')
                    else:
                        print('opening', name, 'with encoding: ', e)
                        en = e
                        break
                
                fp = codecs.open(srcname, 'r', en)
                text = fp.read()
                fp.close()  

                #ost = re.sub(oriprjname, newprjname, text)
                ost = lowre.sub(newprjname, text)
                ost = upperre.sub(newprjname.upper(), ost)
                ost2 = codecs.encode(ost)
                fp = open(srcname, 'wb')
                fp.write(ost2)
                fp.close()
    return


DuplicateProject()
