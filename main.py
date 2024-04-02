import sys
import os

from PIL import Image
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
from pylibdmtx.pylibdmtx import encode
from ui_app import Ui_MainWindow


class App(QMainWindow, Ui_MainWindow):

    def open_file_dialog(self):  # a function to open the dialog window
        result = str(QFileDialog.getExistingDirectory())
        self.dirPath.setText('{}'.format(result))
        print(result)
        return result

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setPath.clicked.connect(self.open_file_dialog)
        self.dtnStart.clicked.connect(self.start)
        # self.dirPath.setEnabled(False)
        self.show()

    def start(self):
        self.result.clear()
        self.result.append("Генерация запущена...\n")
        path = self.dirPath.text()
        self.openDir(path)
        self.result.append("Генерация завершена...\n")

    def openDir(self, path):
        listDir = os.listdir(path)
        for i in listDir:
            if os.path.isfile(path + "/" + i):
                if i.split(".")[len(i.split("."))-1] == "txt":
                    self.qr_gen(path + "/" + i)
            elif os.path.isdir(path + "/" + i):
                self.openDir(path + "/" + i)

    def qr_gen(self, file):

        savePath = file.strip(".txt")
        fileName = file.split('/')[len(file.split('/'))-1].split('.')[0]
        self.result.append(f"Файл {file} запущен...\n")
        print(savePath, fileName)
        cods = []
        with open(file, 'r') as fileData:
            for line in fileData:
                cods.append(line.strip("\n"))

        for i in range(0, len(cods)):
            encoded = encode(cods[i].encode('utf8'))
            img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
            img.save(savePath + f'_{i+1}' +'.jpg')
        self.result.append(f"Файл {file} завершон...\n")



def main():
    code = '0104814207723329212YrbX3bXA5y2j91000592FPwpFQdnpPvsvrn5vpUCmEEDefdQm7y5ee72vHvtmgYi'
    encoded = encode(code.encode('utf8'))
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    img.save('dmtx.jpg')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()

