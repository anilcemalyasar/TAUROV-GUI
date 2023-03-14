from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import cv2
import sys
import time

class Thread(QThread):

    changePixmap = pyqtSignal(QImage)

    def run(self):

        cap = cv2.VideoCapture("C:/Users/anlys/OneDrive/Masaüstü/TAUV-GUI/realtime_ui/Maria_Moves_with_twin_FutureHoops.mp4")
        while True:
            ret, frame = cap.read()

            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(1280,720, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

class Window(QMainWindow):

    def __init__(self):

        super().__init__()

        self.width = 1080
        self.height = 640

        self.setWindowTitle("TAUROV GUI")
        self.setGeometry(50,100, self.width, self.height)

        self.tabWidgets()
        self.widgets()
        self.layouts()
        self.setStyle()
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()


    @pyqtSlot(QImage)
    def setImage(self, image):
        self.inputImage.setPixmap(QPixmap.fromImage(image))
    
    def tabWidgets(self):

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Object Detection")
        self.tabs.addTab(self.tab2, "Parameters")


    def widgets(self):

        #tab1 left (real-time cam stream)

        self.inputImage = QLabel(self)

        # tab1 left middle
        self.engine1 = QLabel(self)
        self.engine1.setText("Engine 1")
        self.checkEngine1 = QPushButton("Check")
        self.checkEngine1.clicked.connect(self.checkEngineFunction)
        
        self.engine2 = QLabel(self)
        self.engine2.setText("Engine 2")
        self.checkEngine2 = QPushButton("Check")
        self.checkEngine2.clicked.connect(self.checkEngineFunction)

        self.engine3 = QLabel(self)
        self.engine3.setText("Engine 3")
        self.checkEngine3 = QPushButton("Check")
        self.checkEngine3.clicked.connect(self.checkEngineFunction)

        self.engine4 = QLabel(self)
        self.engine4.setText("Engine 4")
        self.checkEngine4 = QPushButton("Check")
        self.checkEngine4.clicked.connect(self.checkEngineFunction)

        # tab right middle
        # creating progress bar
        self.progressButton = QPushButton("Mission 1")
        self.progressButton.setStyleSheet("border: 2px solid grey; border-radius: 5px; text-align: center;background-color: #00FFFF;width: 10px;margin: 0.5px;")
        self.progressButton.clicked.connect(self.progressAction)
        self.mission1 = QLabel(self)
        self.pbar = QProgressBar(self)
        self.pbar.setStyleSheet("border: 2px solid grey; border-radius: 5px; text-align: center;background-color: #CD96CD;width: 10px;margin: 0.5px;")
        self.pbar2 = QProgressBar(self)
        self.pbar2.setStyleSheet("border: 2px solid grey; border-radius: 5px; text-align: center;background-color: #CD96CD;width: 10px;margin: 0.5px;")
        

        # tab right
        self.detectedObjects = QTextEdit(self)
        self.detectedObjects.setText("Detected Objects")
        self.detectedObjects.setText("209 110 105 140")

    def setStyle(self):
        self.checkEngine1.setStyleSheet("border: 2px solid grey; border-radius: 5px; text-align: center;background-color: #CD96CD;width: 10px;margin: 0.5px;")

    def layouts(self):

        # main Layout
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QFormLayout()
        self.leftMiddleLayout = QFormLayout()
        self.rightMiddleLayout = QFormLayout()
        self.rightLayout = QFormLayout()

        # left layout and groupbox
        self.leftLayoutGroupBox = QGroupBox("Frame")
        self.leftLayout.addRow(self.inputImage)
        self.leftLayoutGroupBox.setLayout(self.leftLayout)

        # left middle layout and groupbox
        self.leftMiddleGroupBox = QGroupBox("Engines")
        self.leftMiddleLayout.addRow(self.engine1)
        self.leftMiddleLayout.addRow(self.checkEngine1)
        self.leftMiddleLayout.addRow(self.engine2)
        self.leftMiddleLayout.addRow(self.checkEngine2)
        self.leftMiddleLayout.addRow(self.engine3)
        self.leftMiddleLayout.addRow(self.checkEngine3)
        self.leftMiddleLayout.addRow(self.engine4)
        self.leftMiddleLayout.addRow(self.checkEngine4)
        self.leftMiddleGroupBox.setLayout(self.leftMiddleLayout)

        # right middle layout and groupbox
        self.rightMiddleGroupbox = QGroupBox("Missions")
        self.rightMiddleLayout.addRow(self.progressButton)
        self.rightMiddleLayout.addRow(self.mission1)
        self.rightMiddleLayout.addRow("Mission 1", self.pbar)
        self.rightMiddleLayout.addRow("Mission 2", self.pbar2)
        self.rightMiddleGroupbox.setLayout(self.rightMiddleLayout)

        # right layout and groupbox
        self.rightLayoutGroupBox = QGroupBox("Detected Objects")
        self.rightLayout.addRow(self.detectedObjects)
        self.rightLayoutGroupBox.setLayout(self.rightLayout)

        # tab1 main layout
        self.mainLayout.addWidget(self.leftLayoutGroupBox, 50)
        self.mainLayout.addWidget(self.leftMiddleGroupBox, 15)
        self.mainLayout.addWidget(self.rightMiddleGroupbox, 20)
        self.mainLayout.addWidget(self.rightLayoutGroupBox,15)
        self.tab1.setLayout(self.mainLayout)

    def checkEngineFunction(self):
        pass
    
    def progressAction(self):
        for i in range(101):

            time.sleep(0.05)
            self.pbar.setValue(i)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())