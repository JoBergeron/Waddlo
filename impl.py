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
        lump = texWad.GetLump(texName)
        if lump is not None:
            texLumps.append(lump)
            print("getting data for: " + texName.decode("UTF-8"))

#    texStart = texWad.GetLump(utils.TextureMarkerStart())
#    print("start marker location: " + str(texStart.location))
#    print("start marker size: " + str(texStart.length))


#    texEnd = texWad.GetLump(utils.TextureMarkerEnd())
#    print("end marker location: " + str(texEnd.location))
#    print("end marker size: " + str(texEnd.length))

    return texLumps

def AddTexturesToWad(path, source, destination, textureLumps):

    sourceWad = utils.Wad(path + source)
    if sourceWad is None:
        return

    print("Opened wad " + source)
    sourceWad.header.Print()

    destFile = open(path + destination, 'w+b')
    if destFile is None:
        return
        
    destFile.write(sourceWad.header.type) #wad type
    destFile.write((0).to_bytes(4, byteorder = "little", signed = False))
    destFile.write((12).to_bytes(4, byteorder = "little", signed = False))

    startTextureMarkerIndex = sourceWad.GetLumpIndex(utils.TextureMarkerStart())
    if startTextureMarkerIndex == -1:
        startTxDirectoryEntry = utils.DirectoryEntry(0, 0, utils.TextureMarkerStart())
        texStartLump = utils.Lump(startTxDirectoryEntry, b'')
        sourceWad.lumps.append(texStartLump)

    endTextureMarkerIndex = sourceWad.GetLumpIndex(utils.TextureMarkerEnd())
    if endTextureMarkerIndex == -1:
        endTxDirectoryEntry = utils.DirectoryEntry(0, 0, utils.TextureMarkerEnd())
        texEndLump = utils.Lump(endTxDirectoryEntry, b'')
        sourceWad.lumps.append(texEndLump)

    for texLump in textureLumps:
        if sourceWad.GetLump(texLump.directoryEnt.name) is None:
            endTextureMarkerIndex = sourceWad.GetLumpIndex(utils.TextureMarkerEnd())
            sourceWad.lumps.insert(endTextureMarkerIndex, texLump)
            print("Adding lump: " + str(texLump.directoryEnt.name) + " at index: " + str(endTextureMarkerIndex))

    # write data + update location in directory entries
    for lump in sourceWad.lumps:
        lump.directoryEnt.location = destFile.tell()
        destFile.write(lump.data)

    directoryStart = destFile.tell().to_bytes(4, byteorder = "little", signed = False)

    # write directory entries
    for lump in sourceWad.lumps:
        dirEnt = lump.directoryEnt
        destFile.write(dirEnt.location.to_bytes(4, byteorder = "little", signed = False))
        destFile.write(dirEnt.length.to_bytes(4, byteorder = "little", signed = False))
        destFile.write(dirEnt.name)

    #update wad header
    destFile.seek(4)
    destFile.write(len(sourceWad.lumps).to_bytes(4, byteorder = "little", signed = False))
    destFile.write(directoryStart)

    destFile.close()

    




    
