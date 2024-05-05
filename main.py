#создай тут фоторедактор Easy Editor!
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QFileDialog
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import Qt
from PIL import Image
import os
from PIL.ImageFilter import(
    BLUR, SHARPEN
)

extensions = ['jpg', 'png', 'bmp']
workdir = ''

class ImageProcessor():
    def __init__(self):
        self.saveDir = 'editedImages'
        self.image = None
        self.filename = None
    def loadImage(self, filename):
        self.filename = filename
        file_path = os.path.join(workdir, filename)
        self.image = Image.open(file_path)
    def showImage(self, path):
        lblImage.hide()
        pixMapImage = QPixmap(path)
        w, h = lblImage.width(), lblImage.height()
        pixMapImage = pixMapImage.scaled(w, h, Qt.KeepAspectRatio)
        lblImage.setPixmap(pixMapImage)
        lblImage.show()
    def bw(self):
        self.image = self.image.convert("L")
        self.postProcess()
    def rotateL(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.postProcess()
    def rotateR(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.postProcess()
    def mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.postProcess()
    def blur(self):
        self.image = self.image.filter(BLUR)
        self.postProcess()
    def sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.postProcess()
    def postProcess(self):
        self.saveImage()
        imgPath = os.path.join(workdir, self.saveDir, self.filename)
        self.showImage(imgPath)
    def saveImage(self):
        path = os.path.join(workdir, self.saveDir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        path = os.path.join(path, self.filename)
        self.image.save(path)


def filter(files, extensions):
    result = list()
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def openFolder():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    if workdir != '':
        files = os.listdir(workdir)
        files = filter(files, extensions)
        lwImages.clear()
        lwImages.addItems(files)
        disableButtons()

def showChosenImage():
    if lwImages.currentRow() >= 0:
        filename = lwImages.currentItem().text()
        workImage.loadImage(filename)
        imagePath = os.path.join(workdir, workImage.filename)
        workImage.showImage(imagePath)
        enableButtons()
        
def disableButtons():
    pbtnBlur.setDisabled(True)
    pbtnBW.setDisabled(True)
    pbtnClear.setDisabled(True)
    pbtnLeft90.setDisabled(True)
    pbtnMirror.setDisabled(True)
    pbtnRight90.setDisabled(True)
def enableButtons():
    pbtnBlur.setDisabled(False)
    pbtnBW.setDisabled(False)
    pbtnClear.setDisabled(False)
    pbtnLeft90.setDisabled(False)
    pbtnMirror.setDisabled(False)
    pbtnRight90.setDisabled(False)
app = QApplication([])
mw = QWidget()
mw.setWindowTitle('Супер редактор изображений')
mw.resize(1024, 768)
workImage = ImageProcessor()
l1 = QHBoxLayout()#главный лайаут
l2 = QVBoxLayout()#здесь кнопка "Папка" и список картинок из папки
l3 = QVBoxLayout()#здесь картинка и l4 с кнопками
l4 = QHBoxLayout()#здесь будут кнопки редактирования картинки
pbtnFolder = QPushButton('Папка')
pbtnLeft90 = QPushButton('Влево')
pbtnRight90 = QPushButton('Вправо')
pbtnMirror = QPushButton('Отразить')
pbtnClear = QPushButton('Резкость')
pbtnBlur = QPushButton('Размытие')
pbtnBW = QPushButton('Ч/Б')
lblImage = QLabel()
lwImages = QListWidget()
l4.addWidget(pbtnLeft90)
l4.addWidget(pbtnRight90)
l4.addWidget(pbtnMirror)
l4.addWidget(pbtnClear)
l4.addWidget(pbtnBlur)
l4.addWidget(pbtnBW)

l3.addWidget(lblImage)
l3.addLayout(l4)

l2.addWidget(pbtnFolder)
l2.addWidget(lwImages)

l1.addLayout(l2, stretch=30)
l1.addLayout(l3, stretch=70)

mw.setLayout(l1)
pbtnFolder.clicked.connect(openFolder)
lwImages.currentRowChanged.connect(showChosenImage)
pbtnBW.clicked.connect(workImage.bw)
pbtnLeft90.clicked.connect(workImage.rotateL)
pbtnRight90.clicked.connect(workImage.rotateR)
pbtnMirror.clicked.connect(workImage.mirror)
pbtnBlur.clicked.connect(workImage.blur)
pbtnClear.clicked.connect(workImage.sharpen)
disableButtons()
mw.show()
app.exec_()