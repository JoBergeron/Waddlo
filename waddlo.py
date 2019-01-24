import impl
import shutil

path   = "/Users/jonathan/Waddlo/"
mapwad = "Solace_Of_Solstice.wad"
texwad = "jom5_snowtex_zdoom.wad"
mergedwad = "SolaceOfSolsticeV2.wad"

print("=============")
textureNames = impl.GetTextureNamesFromWad(path, mapwad)
print("=============")
textureLumps = impl.GetTextureLumpsFromTexWad(path, texwad, textureNames)

shutil.copyfile(path + mapwad, path + mergedwad)
print("=============")
