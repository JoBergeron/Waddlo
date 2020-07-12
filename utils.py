def SideDefs(): return b"SIDEDEFS"

def GraphicMarkerStart(): return b"PP_START"
def GraphicMarkerEnd(): return b"PP_END\x00\x00"

def GraphicMarkerStart2(): return b"P_START\x00"
def GraphicMarkerEnd2(): return b"P_END\x00\x00\x00"

def Sectors(): return b"SECTORS\x00"

def GetInt32(x): return int.from_bytes(x, byteorder = 'little', signed = False)

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

class DirectoryEntry:
    def __init__(self, location, length, name):
        self.name = name
        self.location = location
        self.length = length

class Lump:
    def __init__(self, directoryEnt, data):
        self.directoryEnt = directoryEnt
        self.data = data

class Wad:
    def __init__(self, path):
        self.wadFile = open(path, 'rb')
        self.fileSize = self.GetSize()
        self.header = Header(self.wadFile)
        self.lumps = []
        
        currentLocation = self.header.GetDirectoryLocationInt32()
        
        while currentLocation < self.fileSize:
            self.wadFile.seek(currentLocation)
            directoryEnt = DirectoryEntry(GetInt32(self.wadFile.read(4)),  GetInt32(self.wadFile.read(4)), self.wadFile.read(8))
            
            self.wadFile.seek(directoryEnt.location)
            lump = Lump(directoryEnt, self.wadFile.read(directoryEnt.length))
            
            self.lumps.append(lump)
            currentLocation += 16

    def __del__(self):
        self.wadFile.close()

    def GetSize(self): return GetFileSize(self.wadFile)
    def GetNbLumps(self): return len(self.lumps)

    def GetLump(self, name):
        for lump in self.lumps:
            if lump.directoryEnt.name == name:
                return lump
        return None

    def GetLumpIndex(self, name):
        x = 0
        for lump in self.lumps:
            if lump.directoryEnt.name == name:
                return x
            x += 1
        return -1

    def GetLumpsWithTag(self, tag):
        lumps = []
        for lump in self.lumps:
            if lump.directoryEnt.name == tag:
                lumps.append(lump)
        return lumps

    def GetLumpsBetweenTags(self, tagStart, tagEnd):
        indexStart = self.GetLumpIndex(tagStart)
        if indexStart == -1:
            return None
        indexEnd = self.GetLumpIndex(tagEnd)
        if indexEnd == -1:
            return None
        return self.lumps[indexStart + 1: indexEnd]


#shortcuts

    def GetSideDefLumps(self): return self.GetLumpsWithTag(SideDefs())

    def GetGraphicLumps(self):
        lumps = self.GetLumpsBetweenTags(GraphicMarkerStart(), GraphicMarkerEnd())
        if lumps is None:
            lumps = self.GetLumpsBetweenTags(GraphicMarkerStart2(), GraphicMarkerEnd2())
        return lumps
