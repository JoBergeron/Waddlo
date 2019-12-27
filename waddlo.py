import impl
import shutil

path   = "/Users/jonathan/Waddlo/"
mapwad = "Refinery.wad"
texwad = "cc4-tex.wad"
mergedwad = "RefineryV2.wad"

print("=============")
textureNames = impl.GetTextureNamesFromWad(path, mapwad)
print("=============")
textureLumps = impl.GetTextureLumpsFromTexWad(path, texwad, textureNames)
print("=============")
impl.AddTexturesToWad(path, mapwad, mergedwad, textureLumps)
