import subprocess
from django.conf import settings

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
        subprocess.call('mv '+settings.BASE_DIR+'/tmp/tmp.tex '+settings.BASE_DIR+'/tmp/'+title+'.tex',shell=True)
    simplifyHevea(settings.BASE_DIR+'/tmp/tmp.html',settings.BASE_DIR+'/tmp/tmpS.html')

def latexToPdf(title):
    subprocess.call('xelatex -output-directory='+settings.BASE_DIR+'/media/pdf '+settings.BASE_DIR+'/tmp/'+title+'.tex',shell=True)
    subprocess.call('xelatex -output-directory='+settings.BASE_DIR+'/media/pdf '+settings.BASE_DIR+'/tmp/'+title+'.tex',shell=True)
    subprocess.call('rm '+settings.BASE_DIR+'/media/pdf/*.log',shell=True)
    subprocess.call('rm '+settings.BASE_DIR+'/media/pdf/*.out',shell=True)
    subprocess.call('rm '+settings.BASE_DIR+'/media/pdf/*.toc',shell=True)
    subprocess.call('rm '+settings.BASE_DIR+'/media/pdf/*.aux',shell=True)
