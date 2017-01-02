import subprocess

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
    ltx = open('tmp/tmp.tex','w',encoding='utf-8')
    ltx.write(contentLtx)
    ltx.close()
    subprocess.run(['hevea','tmp/tmp.tex','-o','tmp/tmp.html'])
    subprocess.run(['hevea','tmp/tmp.tex','-o','tmp/tmp.html'])
    if title:
        subprocess.call('mv tmp/tmp.tex tmp/'+title+'.tex',shell=True)
    simplifyHevea('tmp/tmp.html','tmp/tmpS.html')

def latexToPdf(title):
    subprocess.call('xelatex -output-directory=media/pdf tmp/'+title+'.tex',shell=True)
    subprocess.call('xelatex -output-directory=media/pdf tmp/'+title+'.tex',shell=True)
    subprocess.call('rm media/pdf/*.log',shell=True)
    subprocess.call('rm media/pdf/*.out',shell=True)
    subprocess.call('rm media/pdf/*.toc',shell=True)
    subprocess.call('rm media/pdf/*.aux',shell=True)
