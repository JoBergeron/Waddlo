import utils

def GetTextureNamesFromWad(path, mapwadName):
    
    textureNames = []
    
    mapWad = utils.Wad(path + mapwadName)
    mapWad.header.Print()
    
    sideDefLump = mapWad.GetSideDefsLump()
    if sideDefLump is not None:
        print("Found sidedefs lump")

    if foundSideDefs == True:
        currentLocation = sideDefsStart
        mapWadFile.seek(currentLocation)

        while currentLocation < sideDefsSize:
            mapWadFile.read(2) # x offset
            mapWadFile.read(2) # y offset
        
            upper = mapWadFile.read(8)
            if upper.decode("ascii")[0] != "-":
                if upper not in textureNames:
                    textureNames.append(upper)
    
            lower = mapWadFile.read(8)
            if lower.decode("ascii")[0] != "-":
                if lower not in textureNames:
                    textureNames.append(lower)

            middle = mapWadFile.read(8)
            if middle.decode("ascii")[0] != "-":
                if middle not in textureNames:
                    textureNames.append(middle)
        
            mapWadFile.read(2) # Sector
            currentLocation = currentLocation + 30
                
        for tex in textureNames:
            print(tex.decode("UTF-8"))

    mapWadFile.close()
    return textureNames


def GetTextureLumpsFromTexWad(path, texWad):

    texLumps = []

    texWadFile = open(path + texWad, 'rb')
    print("Opening texture wad: " + texWad)


