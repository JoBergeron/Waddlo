def SideDefsString():
    return "SIDEDEFS"

def GetInt32(x):
    return int.from_bytes(x, byteorder = 'little', signed = False)

def GetFileSize(file):
    x = 0
    file.seek(0, 2)
    x = file.tell()
    file.seek(0)
    return x

class Header:
    def __init__(self, file):
        file.seek(0)
        self.type = file.read(4)
        self.nbLumps = file.read(4)
        self.directoryLocation = file.read(4)

    def GetTypeUTF8(self): return self.type.decode("UTF-8")
    def GetNbLumpsInt32(self): return GetInt32(self.nbLumps)
    def GetDirectoryLocationInt32(self): return GetInt32(self.directoryLocation)

    def Print(self):
        print("wad of type: " + self.GetTypeUTF8())
        print("Number of lumps: " + str(self.GetNbLumpsInt32()))
        print("Location of directory: " + str(self.GetDirectoryLocationInt32()))

class Lump:
    def __init__(self, location, length, name, file):
        self.name = name
        file.seek(location)
        self.data = file.read(length)

class Wad:
    def __init__(self, path):
        self.wadFile = open(path, 'rb')
        self.fileSize = self.GetSize()
        self.header = Header(self.wadFile)
        self.lumps = []
        
        currentLocation = self.header.GetDirectoryLocationInt32()
        
        while currentLocation < self.fileSize:
            self.wadFile.seek(currentLocation)
            
            lumpLocation = GetInt32(self.wadFile.read(4))
            lumpLength = GetInt32(self.wadFile.read(4))
            lumpName = self.wadFile.read(8)
            
            lump = Lump(lumpLocation, lumpLength, lumpName, self.wadFile)
            self.lumps.append(lump)
            
            currentLocation += 16

    
    def __del__(self):
        self.wadFile.close()

    def GetSize(self): return GetFileSize(self.wadFile)
    def GetNbLumps(self): return len(self.lumps)

    def GetSideDefsLump(self):
        for lump in self.lumps:
            if lump.name.decode("UTF-8") == SideDefsString():
                return lump
