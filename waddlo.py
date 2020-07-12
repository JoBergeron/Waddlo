import impl
import utils
import shutil
import io

oatbwadname = "oatb.wad"
doom2wadname = "DOOM2.WAD"
printmaps = False

oatbWad = utils.Wad(oatbwadname)
oatbLumps = oatbWad.GetGraphicLumps()

iwad = utils.Wad(doom2wadname)
iwadLumps = iwad.GetGraphicLumps()

dupes = []

for oatblump in oatbLumps:
    for iwadlump in iwadLumps:

        if oatblump.data == iwadlump.data:
            print("================ dupe found! ==================")
            print("from iwad: " + iwadlump.directoryEnt.name.decode("UTF-8"))
            print("from oatb: " + oatblump.directoryEnt.name.decode("UTF-8"))
            dupes.append(oatblump.directoryEnt.name)

print ("dupes: " + str(dupes))
sideDefLumps = oatbWad.GetSideDefLumps()

i = 1
for sideDefLump in sideDefLumps:
    sideDefLumpByteReader = io.BytesIO(sideDefLump.data)
    size = utils.GetFileSize(sideDefLumpByteReader)
    sideDefLumpByteReader.seek(0)

    textures = []

    while sideDefLumpByteReader.tell() < size:
        sideDefLumpByteReader.read(2) # x offset
        sideDefLumpByteReader.read(2) # y offset

        upper = sideDefLumpByteReader.read(8)
        if upper.decode("ascii")[0] != "-":
            textures.append(upper)
            if upper in dupes:
                print("map{:02d} contains dupe: ".format(i) + upper.decode("UTF-8"))

        lower = sideDefLumpByteReader.read(8)
        if lower.decode("ascii")[0] != "-":
            textures.append(lower)
            if lower in dupes:
                print("map{:02d} contains dupe: ".format(i) + lower.decode("UTF-8"))
                
        middle = sideDefLumpByteReader.read(8)
        if middle.decode("ascii")[0] != "-":
            textures.append(middle)
            if middle in dupes:
                print("map{:02d} contains dupe: ".format(i) + middle.decode("UTF-8"))

        sideDefLumpByteReader.read(2) # Sector
    
    if printmaps:
        print ("==== map{:02d} =======".format(i))
        textureList = set(textures)
        print(*textureList, sep="\n")
    i += 1
