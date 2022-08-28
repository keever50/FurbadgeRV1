import math

class bitmap:
    def __init__(self, path):
        self.data = bytearray(open(path,"rb").read())
        
        #Header
        self.header = bitmap_header(self.data)
        if self.header.size == -1:
            print("[BMP]Bitmap header generation failed")
            return
        
        #DIB
        self.DIB = bitmap_DIB(self.data)
        if self.DIB.size == -1:
            print("[BMP]Bitmap DIB generation failed")        
            return
        
        #Color table
        self.color_palette_offset = self.header.size + self.DIB.size + 1
        self.color_palette = bitmap_color_palette(self.data,self.DIB.palette_entries,self.color_palette_offset)
        
        #Pixel array
        self.pixel_array = bitmap_pixel_array(self.data, self.DIB, self.header.pixelarray_offset )
 
    #Get RGB pixel
    def getPixel(self, index):
        colorindex = self.pixel_array.index_array[index]
        return self.color_palette.palette[colorindex]

    #Generate black/white array
    def generate1bit_array(self):
        array = []
        size = self.pixel_array.pixel_array_size
        rowsize = self.pixel_array.row_size
        height = self.DIB.height
        
        for y in range(height):
            for x in range(rowsize):
                colorindex = self.pixel_array.index_array[((height-y-1)*rowsize)+x]
                RGBA = self.color_palette.palette[colorindex]
                T = RGBA[0]+RGBA[1]+RGBA[2]
                if T > 128:
                    array.append(False)
                else:
                    array.append(True)
                
        return array
                
class bitmap_header:
    def __init__(self, data):
        
        #Check if bitmap ID is BM. This is a windows format.
        self.ID = data[0:2].decode()
        if self.ID == "BM":
            #Build the header
            self.size = 13
            self.image_size = int.from_bytes(data[2:7],"little")
            self.pixelarray_offset = int.from_bytes(data[10:14],"little")     
        else:
            #Return failed
            print("[BMP]Unsupported bitmap type. Only type BM supported.")
            self.size = -1
            return
            
class bitmap_DIB:
    def __init__(self, data):
        
        #Check if compression method is supported
        self.compression_method = data[30]
        if self.compression_method != 0:
            print("[BMP]Unsupported compression. Only uncompressed is supported.")
            self.size = -1
            return
        
        #Build DIB
        self.size = data[0X0E]
        self.width = int.from_bytes(data[18:22],"little")
        self.height = int.from_bytes(data[22:26],"little")
        self.bits_per_pixel = int.from_bytes(data[28:30],"little")
        if self.bits_per_pixel != 8:
            print("[BMP]This bitmap does contain 8 bit colors. Only 8 bit is supported")
            self.size = -1
            return
        self.image_size = int.from_bytes(data[34:38],"little")
        self.colors = int.from_bytes(data[46:50],"little")
        
        self.palette_entries = 2**self.bits_per_pixel

class bitmap_color_palette:
    def __init__(self, data, entries, offset):
        
        self.palette = []
        #Go through each entry
        for x in range(entries):
            #One entry
            RGBA = data[offset+(x*4):offset+(x*4)+4]
            self.palette.append(RGBA)

class bitmap_pixel_array:
    def __init__(self, data, DIB, offset):
        self.index_array = []
        self.row_size = math.ceil( ( DIB.width * 8 ) / 32 ) * 4
        self.pixel_array_size = self.row_size * abs(DIB.height)
        for x in range(self.pixel_array_size):
            self.index_array.append(data[offset+x])


