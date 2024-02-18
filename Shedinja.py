import os
import sys
import pygame
import time
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QMovie, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QTimer, pyqtSlot

class Shedinja(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Shedinja')
        self.setGeometry(100, 100, 480, 250)

        icon = QIcon("src/shedinja.ico")
        self.setWindowIcon(icon)

        self.already_executed()
        
        QFontDatabase.addApplicationFont("src/pokemon-dp-pro.otf")
        custom_font = QFont("Pokémon DP Pro", 16)
        QApplication.setFont(custom_font)

        pygame.mixer.init()
        trilha_sonora = pygame.mixer.music.load("src/OST-BeachAtDusk.mp3")
        volume = 0.3
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

        self.sound_effect = pygame.mixer.Sound("src/ASound.mp3")
        volume_effect = 0.2
        self.sound_effect.set_volume(volume_effect)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        background_label = QLabel(self)
        background_label.setGeometry(0, 0, 512, 360)
        background_label.setScaledContents(True)
        background_label.setMovie(QMovie("src/background.gif"))
        background_label.movie().start()
        background_label.setAlignment(Qt.AlignCenter)

        content_layout = QVBoxLayout()

        shedinja_label = QLabel(self)
        shedinja_movie = QMovie('src/shedinja.gif')
        shedinja_label.setMovie(shedinja_movie)
        shedinja_label.setAlignment(Qt.AlignCenter)
        shedinja_movie.start()
        content_layout.addWidget(shedinja_label)

        layout.addLayout(content_layout)

        dialog_label = QLabel(self)
        dialog_pixmap = QPixmap('src/dialog.png')
        dialog_pixmap = dialog_pixmap.scaledToWidth(self.width()) 
        dialog_label.setPixmap(dialog_pixmap)

        self.dialog_text_label = QLabel(self)
        self.dialog_text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.dialog_text_label.setWordWrap(True)  
        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(self.dialog_text_label)
        dialog_layout.setContentsMargins(20, 10, 35, 2)
        dialog_label.setLayout(dialog_layout)

        layout.addWidget(dialog_label)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_text)
        self.current_text = ""
        self.texts = [
            "Olá, humano. Eu sou Shedinja, um Pokémon que vive à sombra da fragilidade.",
            "Imagine-me como um anjo com apenas uma vida, uma história efêmera a ser contada.",
            "Em meu breve tempo aqui, gostaria de compartilhar contigo uma narrativa. A minha narrativa.",
            "Numa tranquila floresta, sob a luz suave do luar, emergi da casca de um Ninjask. Minha vida é um sopro, um conto que se desenrola em capítulos breves.",
            "Ao longo de minha jornada solitária, descobri o significado de existir num mundo onde o tempo é implacável.",
            "Ao longo desse percurso, encontrei outros seres, todos compartilhando histórias efêmeras.",
            "Não delimitados por seu tempo de vida, mas sim pela sua passagem, como flocos de neve que desaparecem ao tocar o chão.",
            "Conectei-me a criaturas passageiras, sentindo o calor de amizades que brilhavam intensamente, mas cuja luz se apagava rapidamente.",
            "Ao contemplar o horizonte, compreendi que minha existência é como um suspiro no grande espetáculo da vida. Mas, mesmo com uma vida tão efêmera, eu encontrei propósito.",
            "A cada encontro, a cada paisagem, eu deixava uma pequena parte de mim, uma lembrança gravada no tecido do tempo.",
            "Neste breve encontro contigo, é mais uma página desse livro efêmero que compartilho.",
            "Quero transmitir a lição que aprendi: a beleza da vida está na apreciação dos momentos fugazes.",
            "Em tua jornada, permita-te viver plenamente, amar profundamente e deixar uma marca indelével no coração do mundo. Infelizmente, essa é a minha última página.",
            "Será a última vez que nos veremos.",
            "À medida que nossas palavras se despedem, recorda que a efemeridade da vida não diminui seu valor, mas realça sua preciosidade.",
            "Adeus, ser passageiro, que tua jornada seja repleta de significado, e que a eternidade encontre expressões em cada batida do teu coração, humano.",
            "..."
        ]
        self.text_index = 0
        self.animation_in_progress = False

        self.start_text_animation()

    def already_executed(self):
        path_folder = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Shed")

        path_file = os.path.join(path_folder, "verify.txt")
        if os.path.exists(path_file):
            # Abre o arquivo e lê seu conteúdo
            with open(path_file, 'r') as arquivo:
                conteudo = arquivo.read()

            # Verifica se o conteúdo é igual a 1
            if conteudo.strip() == "E = 1":
                print("Conteúdo já é E = 1. O programa não será executado.")
                sys.exit()

        else:
            # Cria o arquivo verify.md se não existir
            os.makedirs(path_folder, exist_ok=True)
            with open(path_file, 'w') as arquivo:
                arquivo.write("E = 1")


    def start_text_animation(self):
        self.current_text = ""
        self.animation_in_progress = True
        self.timer.start(0
                         )  

    @pyqtSlot()
    def animate_text(self):
        if len(self.current_text) < len(self.texts[self.text_index]):
            self.current_text += self.texts[self.text_index][len(self.current_text)]
            self.dialog_text_label.setText("Shedinja: " + self.current_text)
        else:
            self.timer.stop()
            self.animation_in_progress = False
            if self.text_index == len(self.texts) - 1:  
                sys.exit()



    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Z or event.key() == Qt.Key_Return:
            if not self.animation_in_progress:
                self.sound_effect.play()
                self.text_index = (self.text_index + 1) % len(self.texts)
                self.start_text_animation()
            

    def set_dialog_text(self, text):
        self.dialog_text_label.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Shedinja()
    window.show()
    sys.exit(app.exec_())
