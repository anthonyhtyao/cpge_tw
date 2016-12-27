import subprocess

def simplifyHevea(inputFile, outputFile):
    passLst = ['<!DOC','<html','<meta','<head','<titl','</tit','</hea','<body']
    breakLst = ['<!--F']
    inputf = open(inputFile,'r')
    outputf = open(outputFile,'w')
    for line in inputf:
        s = line[:5]
        if s in passLst:
            pass
        elif s in breakLst:
            break
        else:
            outputf.write(line)
    inputf.close()
    outputf.close()

def latexToHtml(contentLtx):
    ltx = open('tmp/tmp.tex','w')
    ltx.write(contentLtx)
    ltx.close()
    subprocess.run(['hevea','tmp/tmp.tex','-o','tmp/tmp.html'])
    subprocess.run(['hevea','tmp/tmp.tex','-o','tmp/tmp.html'])
    simplifyHevea('tmp/tmp.html','tmp/tmpS.html')
