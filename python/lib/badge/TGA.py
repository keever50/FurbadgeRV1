def getInfo(file):
    IDLength = file[0]
    ColorMapType = file[1]
    ImageType = file[2]
    
    ColorMapSpec=[]
    ColorMapSpec = [0 for i in range(4)]
    for i in range(4):
        ColorMapSpec[i]=file[3+i]
    ImageSpecs=[]
    ImageSpecs = [0 for i in range(9)]        
    for i in range(9):
        ImageSpecs[i]=file[8+i]    