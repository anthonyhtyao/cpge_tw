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
