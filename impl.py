import utils
import io

def GetTextureNamesFromWad(path, mapwadName):
    
    textureNames = []
    
    mapWad = utils.Wad(path + mapwadName)
    if mapWad is None:
        return
    
    print("Opened wad " + mapwadName)
    mapWad.header.Print()
    
    sideDefLump = mapWad.GetLump(utils.SideDefs())
    if sideDefLump is not None:
        print("Found sidedefs lump!")

    sideDefLumpByteReader = io.BytesIO(sideDefLump.data)
    size = utils.GetFileSize(sideDefLumpByteReader)
    sideDefLumpByteReader.seek(0)

    while sideDefLumpByteReader.tell() < size:
        sideDefLumpByteReader.read(2) # x offset
        sideDefLumpByteReader.read(2) # y offset
    
        upper = sideDefLumpByteReader.read(8)
        if upper.decode("ascii")[0] != "-":
            if upper not in textureNames:
                textureNames.append(upper)

        lower = sideDefLumpByteReader.read(8)
        if lower.decode("ascii")[0] != "-":
            if lower not in textureNames:
                textureNames.append(lower)

        middle = sideDefLumpByteReader.read(8)
        if middle.decode("ascii")[0] != "-":
            if middle not in textureNames:
                textureNames.append(middle)
    
        sideDefLumpByteReader.read(2) # Sector

    return textureNames


def GetTextureLumpsFromTexWad(path, texWadName, textureNames):

    texLumps = []

    texWad = utils.Wad(path + texWadName)
    if texWad is None:
        return

    print("Opened wad " + texWadName)
    texWad.header.Print()

    for texName in textureNames:
        texNameUTF8 = texName.decode("UTF-8")
        lump = texWad.GetLump(texName)
        if lump is not None:
            texLumps.append(lump)
            print("getting data for: " + texNameUTF8)

    texStart = texWad.GetLump(utils.TextureMarkerStart())
    print("start marker location: " + str(texStart.location))
    print("start marker size: " + str(texStart.length))


    texEnd = texWad.GetLump(utils.TextureMarkerEnd())
    print("end marker location: " + str(texEnd.location))
    print("end marker size: " + str(texEnd.length))

    return texLumps


def AddTexturesToWad(path, wadName, textureLumps):

    wad = utils.Wad(path + wadName)
    if wad is None:
        return

    print("Opened wad " + wadName)
    wad.header.Print()

    texStart = wad.GetLump(utils.TextureMarkerStart())
