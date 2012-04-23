#Usage: python wikixml2txt.py [wiki.xml]
#NOTE: place this script in dir you want to contain all articles. xml can be elsewhere
#Download Wikpedia articles from en.wikipedia.org/wiki/Wikipedia:Database_download, unpack the xml

#TODO:

import sys
import string

title = ""
article = []
catchTitle = False
catchText = False
redirect = False
totalCount = 0
noRedirCount = 0

#takes in a string title and array of article text. Writes lines of array to file "title.txt" in working dir
def writeArticle(title, article):
    global noRedirCount
    
    #if title is >255 bytes cut the last char off till it's small enough to fit in ext3 fileSystem
    while sys.getsizeof(str(title + ".txt")) > 255:
        title = title[:-1]
    
    filename = title + ".txt"
    filename = filename.replace("/","\\") #titles with "/" don't export as files well. replace with "\"
    try:
        output = open(filename, "w")
        for line in article:
            print >>output, line
            #exit(0) #write one article and QUIT TESTING ONLY
    except:
        print "Unexpected error: ", sys.exc_info()[0]
    noRedirCount += 1

#might be issues if tables use these objects eg { table stuff, {{object}} \n ...
#returns text without one line wiki encoded objects: {{object}}    
def parseJunk(line):
    global redirect
    
    #catch redirects
    if string.find(line, "#REDIRECT") is not -1:
        redirect = True
        return line
    
    #is the whole line an internal page link?
    if line[:2] == "[[" and line[-2:] == "]]":
        return None
    #Does the line even contain object braces?
    if string.find(line, "{{") is -1:
        return line
    
    #Is the object COMPLETED in this line? (if not leave it there eg. tables)
    braceCount = 0
    for char in line:
        if char is '{':
            braceCount += 1
        if char is '}':
            braceCount -= 1
    if braceCount is not 0:
        return line
    
    #the object is completed in one line, remove it
    text = ""
    braceCount = 0
    flag = True
    for char in line:
        if char is '{':
            braceCount += 1
            flag = False
        if flag:
            text += char
        if char is '}':
            braceCount -= 1
            if braceCount == 0:
                flag = True
    return text

def appendToArticle(line):
    global article
    
    line = line.replace("\n","")
    line = parseJunk(line)
    if line is not None:
        article.append(line)

def main():
    global title
    global article
    global catchTitle
    global catchText
    global redirect
    global totalCount
    
    print ""
    print "Parsing..."
    for line in open(sys.argv[1]):
        #Title parsing
        if(catchTitle and (string.find(line, "<title>") is not -1) and (string.find(line, "</title>") is not -1)):
            catchTitle = False #Set the next line to NOT be a new article
            flag = False  #don't record chars yet
            for char in line:
                if char is '<':  #ENDS title eg ...TITLE</title>
                    flag = False
                if flag:    #In between tags?
                    title += char
                if char is '>':  #START title eg <title>TITLE...
                    flag = True
            title = title.replace("\n","")  #get rid of line break from end of tag  </title>_  <---
            totalCount += 1  #increment counter for #of articles
            
        #save article text to array
        if catchText and string.find(line, "</text>") is not -1: #reached the text end tag
            catchText = False
            lastLine = ""
            for char in line: #record this line NOT the tag
                if char is '<': #ENDS text eg ...article text.</text>
                    break
                else:  
                    lastLine += char
            appendToArticle(lastLine)
            if not redirect: #this article doesn't redirect to something else 
                writeArticle(title, article)  #writes to individual .txt file
            title = ""
            article = []
            redirect = False
        
        if catchText:
            appendToArticle(line)
        
        if string.find(line, "<text xml:space=\"preserve\">") is not -1: #found text start tag
            catchText = True
            firstLine = ""
            record = False
            for char in line: #record this line NOT the tag
                if record:  
                    firstLine += char
                if char is '>': #ENDS tag eg <text xml:space=\"preserve\">Start text...
                    record = True
            appendToArticle(firstLine)
        
        if string.find(line, "<page>") is not -1: #start of new article
            catchTitle = True
    
    print "Done."
    print "Articles in dump: " + str(totalCount)
    print "Redirects: " + str(totalCount - noRedirCount)
    print "Articles exported: " + str(noRedirCount)
    print ""

if __name__ == "__main__":
    main()
