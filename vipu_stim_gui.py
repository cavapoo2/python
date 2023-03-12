import sys

from PyQt5.QtCore import (
    Qt,
    QLine,
    QPropertyAnimation,
    QSize
)
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
    QFormLayout,
    QStyleFactory,
    QProxyStyle,
    QStyle,
    QRadioButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QSpinBox,
    QFrame,
    QSplitter,
    QGraphicsLineItem,


)

from PyQt5.QtGui import (
        QFont,
        QPen,
        QColor,
        QPixmap,


)

class Heading(QLabel):
    def __init__(self,heading_name,font_size=20,font='Arial'):
        super().__init__()
        self.setText(heading_name)
        self.setAlignment(Qt.AlignCenter)
        heading_font = QFont(font, font_size, QFont.Black)
        heading_font.setStretch(QFont.ExtraExpanded)
        self.setFont(heading_font)
        self.setStyleSheet("* { \
                                    background: qradialgradient(cx: 0.3, cy: -0.4, fx: 0.3, fy: \
                                    -0.4, radius: 1.35, stop: 0 #fff, stop: 1 #888); \
                                    color: rgb(0, 0, 0); \
                                    border: 1px solid #ffffff; \
                                    }")



        # Display a simple raster image
        #logo = QPixmap('logo.png')

        #logo = logo.scaledToWidth(350, Qt.SmoothTransformation)
        #heading.setPixmap(logo)
        #self.setPixmap(logo)

        # Simple property animation
        #self.heading_animation = QPropertyAnimation(
        #    self, b'maximumSize')
        #self.heading_animation.setStartValue(QSize(10, logo.height()))
        #self.heading_animation.setEndValue(QSize(350, logo.height()))
        #self.heading_animation.setDuration(1000)
        #self.heading_animation.start()


class SelectionItem(QWidget):
    def __init__(self,name_upper,name_lower,handler):
        super().__init__()
        layout = QVBoxLayout()
        self.upper = QRadioButton(name_upper)
        self.upper.setChecked(True)
        self.upper.setStyleSheet("QRadioButton::checked { \
                                background-color:lightgreen; \
                                }")
        layout.addWidget(self.upper)

        self.lower = QRadioButton(name_lower)
        self.lower.setChecked(False)
        self.lower.setStyleSheet("QRadioButton::checked { \
                                        background-color:red; \
                                        }")

        layout.addWidget(self.lower)

        self.setLayout(layout)
        self._set_handler(handler)


    def _set_handler(self,handler):
        self.upper.toggled.connect(lambda:handler(self.upper.text(),self.upper.isChecked()))
        self.lower.toggled.connect(lambda:handler(self.lower.text(),self.lower.isChecked()))

class MessageIgnoreOrCorrupt(QWidget):
    def __init__(self,name,handler,max_count=10):
        super().__init__()
        layout = QHBoxLayout()
        label = QLabel(name)
        layout.addWidget(label)

        self.edit = QSpinBox()
        self.edit.setMinimum(0)
        self.edit.setMaximum(max_count)
        self.edit.setFixedWidth(50)
        layout.addWidget(self.edit)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        self._set_handler(handler)

    def _set_handler(self,handler):
        #self.button.clicked.connect(lambda:handler(self.edit.text()))
        self.edit.valueChanged.connect(lambda:handler(self.edit.value()))

class LineDivider(QFrame):
    def __init__(self,divider=QFrame.HLine):
        super().__init__()
        self.setFrameShape(divider)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('VIPU Stimulator    ')
        self.setFixedWidth(400)
        self.setFixedHeight(300)
        '''
        self.setStyleSheet("* { \
                            background: qradialgradient(cx: 0.3, cy: -0.4, fx: 0.3, fy: \
                            -0.4, radius: 1.35, stop: 0 #fff, stop: 1 #888); \
                            color: rgb(0, 0, 0); \
                            border: 1px solid #ffffff; \
                            }")
        '''
        form = QWidget()
        self.setCentralWidget(form)
        form.setLayout(QFormLayout())

        heading = Heading("VIPU Stimulator")
        form.layout().addRow(heading)

        div1 = LineDivider()
        form.layout().addRow(div1)

        selection_local_remote  = SelectionItem("remote","local",self.remote_local_handler)
        selection_ready = SelectionItem("vipu ready", "vipu not ready",self.ready_handler)
        form.layout().addRow(selection_local_remote,selection_ready)

        selection_bite_psu_stbd = SelectionItem("No Starboard PSU Fault", "Starboard PSU Fault", self.stbd_psu_fault)
        selection_bite_psu_port = SelectionItem("No Port PSU Fault", "Port PSU Fault", self.port_psu_fault)
        form.layout().addRow(selection_bite_psu_port, selection_bite_psu_stbd)

        div2 = LineDivider()
        form.layout().addRow(div2)

        ignore_video = MessageIgnoreOrCorrupt("Ignore Video Ctrl",self.video_ignore)
        form.layout().addRow(ignore_video)

        bad_status_message = MessageIgnoreOrCorrupt("Bad Status Message",self.bad_status_message)
        form.layout().addRow(bad_status_message)
        # End main UI code
        self.show()


    def remote_local_handler(self,name,checked):
        if name == "remote" and checked:
            print("remote was activated")
        elif name == "local" and checked:
            print("local was activated")
        else:
            pass

    def ready_handler(self, name,checked):
        if name == "vipu ready" and checked:
            print("ready was activated")
        elif name == "vipu not ready" and checked:
            print("not ready was activated")
        else:
            pass

    def stbd_psu_fault(self,name,checked):
        if name == "Starboard PSU Fault" and checked:
            print("Starboard PSU Fault")
        elif name == "No Starboard PSU Fault" and checked:
            print("Clear Starboard PSU Fault")
        else:
            pass

    def port_psu_fault(self, name, checked):
        if name == "Port PSU Fault" and checked:
            print("Port PSU Fault")
        elif name == "No Port PSU Fault" and checked:
            print("Clear Port PSU Fault")
        else:
            pass

    def video_ignore(self,count):
        print("Vid ignore:",count)

    def bad_status_message(self,count):
        print("Status_Message:",count)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())



