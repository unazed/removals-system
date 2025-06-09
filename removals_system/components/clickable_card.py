from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap


class ClickableCard(QFrame):
    clicked = Signal()
    
    def __init__(
        self,
        title: str,
        description: str,
        icon_path: str,
        dim: tuple[int, int]
    ) -> None:
        super().__init__()
        self.setObjectName("clickable-card")

        layout = QVBoxLayout(self)
        
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(icon_path)
        icon_label.setPixmap(pixmap.scaled(
            *dim,
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        layout.addWidget(icon_label)
        layout.addSpacing(10)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Albert Sans", 16, QFont.Bold))
        layout.addWidget(title_label)
        layout.addSpacing(5)
        
        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setFont(QFont("Albert Sans", 12))
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        self.setMinimumSize(250, 300)
        self.setStyleSheet("""
            QFrame#clickable-card {
                border: 2px solid transparent;
                border-radius: 8px;
            }
            QFrame#clickable-card:hover {
                border: 2px solid #cccccc;
            }
        """)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super().leaveEvent(event)