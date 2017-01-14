import subprocess
from django.conf import settings
import os
from shutil import copyfile

def simplifyHevea(inputFile, outputFile):
    passLst = ['<!DOC','<html','<meta','<head','<titl','</tit','</hea','<body']
    breakLst = ['<!--F']
    inputf = open(inputFile,'r',encoding='utf-8')
    outputf = open(outputFile,'w',encoding='utf-8')
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

def latexToHtml(contentLtx,title=''):
    ltx = open(settings.BASE_DIR+'/tmp/tmp.tex','w',encoding='utf-8')
    ltx.write(contentLtx)
    ltx.close()
    subprocess.run(['hevea',settings.BASE_DIR+'/tmp/tmp.tex','-o',settings.BASE_DIR+'/tmp/tmp.html'])
    subprocess.run(['hevea',settings.BASE_DIR+'/tmp/tmp.tex','-o',settings.BASE_DIR+'/tmp/tmp.html'])
    if title:
        copyfile((settings.BASE_DIR+'/tmp/tmp.tex').encode('utf-8'),(settings.BASE_DIR+'/tmp/'+title+'.tex').encode('utf-8'))
    simplifyHevea(settings.BASE_DIR+'/tmp/tmp.html',settings.BASE_DIR+'/tmp/tmpS.html')

def latexToPdf(title):
    subprocess.call(('xelatex -output-directory='+settings.BASE_DIR+'/media/pdf '+settings.BASE_DIR+'/tmp/'+title+'.tex').encode('utf8'),shell=True)
    subprocess.call(('xelatex -output-directory='+settings.BASE_DIR+'/media/pdf '+settings.BASE_DIR+'/tmp/'+title+'.tex').encode('utf8'),shell=True)
    subprocess.call(('rm '+settings.BASE_DIR+'/media/pdf/*.log').encode('utf8'),shell=True)
    subprocess.call(('rm '+settings.BASE_DIR+'/media/pdf/*.out').encode('utf8'),shell=True)
    subprocess.call(('rm '+settings.BASE_DIR+'/media/pdf/*.toc').encode('utf8'),shell=True)
    subprocess.call(('rm '+settings.BASE_DIR+'/media/pdf/*.aux').encode('utf8'),shell=True)
