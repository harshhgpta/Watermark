import multiprocessing as mp
import os
import shutil
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tqdm import tqdm
import PIL.Image
# from progressbar import ProgressBar
# pbar = ProgressBar()
from functools import partial


# import time


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Aaruush Watermark")
        self.minsize(300, 100)
        # self.wm_iconbitmap('icon.ico')

        self.labelFrame1 = ttk.LabelFrame(self, text="Open Folder")
        self.labelFrame1.grid(column=0, row=1, padx=20, pady=20)
        # self.labelFrame2 = ttk.LabelFrame(self, text="Enter Names of individuals with commas")
        # self.labelFrame1.grid(column=0, row=1, padx=40, pady=20)
        # self.labelFrame2.grid(column=0, row=1, padx=20, pady=20)
        # textBox = Text(self, height=2, width=10)
        # # textBox.pack()
        # buttonCommit = Button(self, height=1, width=10, text="Commit",
        #                       command=lambda: self.retrieve_input())
        # self.textBox()
        self.btn()

    def btn(self):
        self.button = ttk.Button(self.labelFrame1, text="Browse to Folder", command=self.fileDialog)
        self.button.grid(column=1, row=1)

    def fileDialog(self):
        self.filename = filedialog.askdirectory(initialdir="/", title="Select Folder")
        if self.filename != '/':
            Files.dirName = self.filename.replace('/', '\\')
        self.destroy()


def ig_f(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]


def createDirectories():
    dirtree = Files.dirName.split('\\')
    foldername = dirtree.pop(-1)
    Files.newDir = '\\'.join(dirtree) + '\\Watermarked_' + foldername
    print(Files.newDir)
    try:
        if not os.path.exists(Files.newDir):
            shutil.copytree(Files.dirName, Files.newDir, ignore=ig_f)
    except:
        print('Already Present')


class Files:
    listOfFiles = list()
    dirName = ''
    newDir = ''
    mark1 = PIL.Image.open('a19.png')
    mark2 = PIL.Image.open('ac.png')


def watermark(im, mark, mark2):
    """Adds a watermark to an image."""
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = PIL.Image.new('RGBA', im.size, (0, 0, 0, 0))
    if im.size[0] >= im.size[1]:
        w1 = int(im.size[0] * 0.2)
        w2 = int(im.size[0] * 0.14)
    else:
        w1 = int(im.size[1] * 0.2)
        w2 = int(im.size[1] * 0.14)
    scale1 = float(w1 / mark.size[0])
    scale2 = float(w2 / mark2.size[0])
    mark = mark.resize((int(mark.size[0] * scale1), int(mark.size[1] * scale1)))
    mark2 = mark2.resize((int(mark2.size[0] * scale2), int(mark2.size[1] * scale2)))
    layer.paste(mark, (int(im.size[0] * 0.01), int(im.size[1] * 0.01)))
    layer.paste(mark2, (
    im.size[0] - mark2.size[0] - int(im.size[0] * 0.01), im.size[1] - mark2.size[1] - int(im.size[1] * 0.01)))

    # composite the watermark with the layer
    return PIL.Image.composite(layer, im, layer)


def main():
    # start = time.time()
    # Files.newDir = '\\'.join(Files.dirName.replace().split('//').pop())

    Files()
    root = Root()
    root.mainloop()
    createDirectories()
    Files.dirName = Files.dirName.replace('//', '\\')
    # Get the list of all files in directory tree at given path
    for (dirpath, dirnames, filenames) in os.walk(Files.dirName):
        Files.listOfFiles += [os.path.join(dirpath, file) for file in filenames if
                              file.lower().endswith('jpg') or file.lower().endswith('jpeg')]
    # Add watermarks to these files:
    # for i in tqdm(Files.listOfFiles):
    #     watermark_images_temp(i)
    '''TRIED WITH MULTIPROCESSING'''
    '''!!!SHARED MEMORY PROBLEM!!!'''
    # print(mp.cpu_count())
    p = mp.Pool(int(mp.cpu_count() / 2))
    func = partial(watermark_images, Files.dirName, Files.newDir)
    for _ in tqdm(p.imap_unordered(func, Files.listOfFiles), total=len(Files.listOfFiles)):
        pass
    # p.map(func, Files.listOfFiles)  # range(0,1000) if you want to replicate your example
    p.close()
    p.join()
    # end = time.time()
    # print(end - start)
    # watermark_images()
    # Print the files
    # for elem in Files.listOfFiles:
    #     print(elem)


# def watermark_images_temp(dirName, newDir, file):
#     # print(file)
#     save_dir = file.replace(dirName, newDir)
#     print(save_dir)

def watermark_images(dirName, newDir, file):
    # file.replace()
    # print(file)
    im = PIL.Image.open(file)
    final = watermark(im, Files.mark1, Files.mark2)
    save_dir = file.replace(dirName, newDir)
    # print(save_dir)
    final.convert('RGB').save(save_dir, format=None, quality=95)
    im.close()


if __name__ == '__main__':
    main()

# pyinstaller --onefile Watermark.py