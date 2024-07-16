from PySide6.QtWidgets import QMainWindow
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QUrl

from cursed_resourses import final_cock,virus

class CockroachWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowTransparentForInput | Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)

        self.video_widget = QVideoWidget()

        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setSource(QUrl.fromLocalFile(final_cock))
        self.media_player.setLoops(QMediaPlayer.Loops.Infinite)

        self.audio_output = QAudioOutput()
        self.audio_player = QMediaPlayer()
        self.audio_player.setAudioOutput(self.audio_output)
        self.audio_player.setLoops(QMediaPlayer.Loops.Infinite)
        self.audio_player.setSource(QUrl.fromLocalFile(virus))

        self.showFullScreen()
        self.setWindowOpacity(0.6)
        self.setCentralWidget(self.video_widget)

    def start_video(self):
        self.media_player.play()
        
    def start_audio(self):
        self.audio_player.play()

    def start(self):
        self.start_audio()
        self.start_video()


