import os
import sys
from PIL.Image import Image

from algorithm import packer


def show_help():
    print("")
    print(" |-- Fry 1.0.2")
    print(" | -- @Author Cristopher Gtz")
    print(" |-- Simple steganography tool")
    print(" |")
    print(" |-- @license MIT")
    print("")
    print("     fry --hide, -h <destination> <file_to_hide>")
    print("")
    print("     fry --show, -s <portator>")
    print("")
    sys.exit()


try:

    if __name__ == "__main__":

        try:
            command = sys.argv[1]
        except:
            show_help()
            sys.exit()

        try:
            img_to_work = sys.argv[2]
        except:
            print(" ~ I need a image")
            sys.exit()

        img_obj = Image.open(img_to_work)
        img_pix = img_obj.load()

        img_storange = ((img_obj.size[0] * img_obj.size[1] * 3) / 8)

        if command == "--hide" or command == "-h":

            try:
                file_to_work = sys.argv[3]
            except:
                print(" ~ I need a file to hide")
                sys.exit()

            file_obj = open(file_to_work)

            data_size = os.fstat(file_obj.fileno()).st_size
            file_data = file_obj.read()

            file_obj.close()

            print(" ~ File to hide: %s" % file_to_work)
            print(" ~ Container image: %s" % img_to_work)
            print(" ~ Image size %sx%spx\n" % img_obj.size)
            print(" ~ You can hide %s Bytes of data" % img_storange)
            print(" ~ %s Bytes to hide...\n" % data_size + 14 + len(file_to_work))

            if data_size > img_storange:
                print(" ~ Error: the container image is too small")
                sys.exit()

            new_img_obj = packer.encode(img_obj, img_pix, file_to_work, file_data)

            if not new_img_obj:
                print(" ~ Are you sure that the container image is bmp or jpg?")
                sys.exit()

            output_file = os.path.splitext(img_to_work)[0] + '.png'
            new_img_obj.save(output_file)

            print("|-- Output was saved on %s" % output_file)

        elif command == "--show" or command == "-s":

            print(" ~ Analysing %s (%s Bytes)" % (img_to_work, img_storange))
            print(" ~ Image size %sx%spx\n" % img_obj.size)

            filename, filedata = packer.decode(img_obj, img_pix)

            if not filename or not filedata:
                print(" ~ This image do not have hidden files")
                sys.exit()

            print(" ~ Hidden file: %s (%s Bytes)" % (filename, len(filedata)))

            new_filename = input(" ~ Save as (enter to original name): ")

            print("")

            if not new_filename == "":
                filename = new_filename

            file_obj = open(filename, "wb")

            file_obj.write(filedata)

            file_obj.close()

            print("|-- Output was written on %s" % filename)


except KeyboardInterrupt:
    print("\n\n|-- stopped")

print("|-- bye")
