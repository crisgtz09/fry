from PIL import Image

def pack(filename, data):

   # file name
   for char in filename:
      for bit in  bin(ord(char))[2:].zfill(8):
         yield bit

   for char in "(*rtl*)":
      for bit in bin(ord(char))[2:].zfill(8):
         yield bit

   # data
   for char in data:
      for bit in  bin(ord(char))[2:].zfill(8):
         yield bit

   for char in "(*rtl*)-":
      for bit in bin(ord(char))[2:].zfill(8):
         yield bit

def encode(img_obj, img_pix, filename, data):

   data_pack = pack(filename, data)

   new_img_obj = Image.new("RGB", img_obj.size, "white")
   new_img_pix = new_img_obj.load()

   for x in range(0, img_obj.size[0]):
      for y in range(0, img_obj.size[1]):

         rgb_pixel = img_pix[x,y]
         new_pixel = ()

         for byte in rgb_pixel:
            try:
               new_pixel = new_pixel + (int(bin(byte)[:-1] + data_pack.next(), 2), )
            except StopIteration:
               new_pixel = rgb_pixel + (byte, )

         try:
            new_img_pix[x, y] = new_pixel
         except:
            return False

   return new_img_obj

def decode(img_obj, img_pix):
   data = ""
   _byte = ""

   bits_counter = 0

   for x in range(0, img_obj.size[0]):
      for y in range(0, img_obj.size[1]):
         pixel = img_pix[x,y]
         for byte in pixel:
            _byte += bin(byte)[-1:]

            bits_counter += 1

            if bits_counter == 8:

               data += chr(int(_byte, 2))
               _byte  = ""

               bits_counter = 0

   data = data.split("(*rtl*)")

   if len(data) < 3:
      return False, False

   return data[0], data[1]