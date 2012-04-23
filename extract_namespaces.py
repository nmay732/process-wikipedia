#Takes target Wikipedia files and organizes them by namespace in dirs
#Usage: python extract_namespaces.py WikipediaDir outdir

import sys
import os
import shutil

#make all destination folders
indir = sys.argv[1]
outdir = sys.argv[2]
if outdir[-1] is not "/":
    outdir += "/"
outdirs = {"Wikipedia:", "Portal:", "User:", "File:", "MediaWiki:", "Template:", "Category:", "Book:", "Help:", "Special:", "Media:", "Main:", "Talk:", 
           "Wikipedia Talk:", "Portal Talk:", "User Talk:", "File Talk:", "MediaWiki Talk:", "Template Talk:", "Category Talk:", "Book Talk:", "Help Talk:"}
for string in outdirs:
    try: #try making each directory
        os.mkdir(outdir + string)
    except: #if dir is already created
        pass

#make talk dirs

#scan each file in indir
for dummie1, dummie2, files in os.walk(indir):
    for f in files:
        filepath = indir + "/" + f
        basename = os.path.basename(filepath)
        
        flag = False
        #Which namespace is it in? Move it there
        for string in outdirs:
            if basename.startswith(string):
                shutil.move(filepath, outdir + string + "/" + basename)
                print "MOVED " + filepath + " -> " + outdir + string + "/" + basename
                flag = True
                break
        #If it's not in a tagged namespace, move it to Main:
        if flag is False:
            shutil.move(filepath, outdir + "Main:" + "/" + basename)
        flag = False #reset flag
    