import os
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
from encp3 import encrypt_message, decrypt_message, get_time_key

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, "whatsapp_logo.png").replace("\\", "/")
BG_PATH = os.path.join(BASE_DIR, "chat_background2.png").replace("\\", "/")


class ChatScreen(qtw.QWidget):
    message_sent = qtc.pyqtSignal(str)

    def __init__(self, title, chat_display=None, message_input=None, send_enabled=True):
        super().__init__()

        self.send_enabled = send_enabled

        layout = qtw.QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)

        title_label = qtw.QLabel(title)
        title_label.setFont(qtg.QFont('Helvetica', 16, qtg.QFont.Weight.Bold))
        title_label.setStyleSheet("""
            color: white;
            background-color: #128C7E;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        """)
        layout.addWidget(title_label)

        self.chat_frame = qtw.QFrame()
        self.chat_frame.setStyleSheet("""
            QFrame {
                border: 2px solid #25D366;
                border-radius: 10px;
                background-color: transparent;
            }
        """)

        frame_layout = qtw.QVBoxLayout(self.chat_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        self.chat_display = chat_display if chat_display else qtw.QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(qtg.QFont('Helvetica', 14))
        self.chat_display.setStyleSheet(f"""
            QTextEdit {{
                border-image: url('{BG_PATH}') 0 0 0 0 stretch stretch;
                border: none;
                background-color: transparent;
                padding: 10px;
                color: #075E54;
                font-family: 'Helvetica';
            }}
        """)
        frame_layout.addWidget(self.chat_display)

        layout.addWidget(self.chat_frame)

        input_layout = qtw.QHBoxLayout()
        self.message_input = message_input if message_input else qtw.QLineEdit()
        self.message_input.setPlaceholderText("Type your message...")
        self.message_input.setFont(qtg.QFont('Helvetica', 14))
        self.message_input.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: 2px solid #25D366;
                border-radius: 15px;
                padding: 8px;
                color: #075E54;
            }
            QLineEdit:focus {
                border-color: #128C7E;
            }
        """)
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)

        self.send_button = qtw.QPushButton("Send")
        self.send_button.setFont(qtg.QFont('Helvetica', 12, qtg.QFont.Weight.Bold))
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #25D366;
                color: white;
                border-radius: 15px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #128C7E;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        if self.send_enabled:
            layout.addLayout(input_layout)
        else:
            self.message_input.hide()
            self.send_button.hide()

    def send_message(self):
        if not self.send_enabled:
            return

        message = self.message_input.text().strip()
        if message:
            self.message_sent.emit(message)
            self.message_input.clear()


class MainApp(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Messages Encryption and Decryption")
        self.setWindowIcon(qtg.QIcon(ICON_PATH))
        self.setGeometry(100, 100, 1200, 400)

        main_layout = qtw.QHBoxLayout()
        self.setLayout(main_layout)

        self.chat1 = ChatScreen("Chat 1 MESSAGES", send_enabled=True)
        self.chat2 = ChatScreen("Chat 2 Encrypted messages", send_enabled=False)
        self.chat3 = ChatScreen("Chat 3 Decrypted messages", send_enabled=True)

        self.chat1.message_sent.connect(self.send_from_chat1)
        self.chat3.message_sent.connect(self.send_from_chat3)

        main_layout.addWidget(self.chat1)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.chat2)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.chat3)

        self.setStyleSheet("""
            QWidget {
                background-color: #ECE5DD;
            }
        """)
        self.show()

    def send_from_chat1(self, message):
        current_key = get_time_key()
        encrypted = encrypt_message(message, current_key)
        decrypted = decrypt_message(encrypted, current_key)

        self.chat1.chat_display.append(f"You: {message}")
        self.chat2.chat_display.append(f"Encrypted [key={current_key}]: {encrypted}")
        self.chat3.chat_display.append(f"Decrypted: {decrypted}")

    def send_from_chat3(self, message):
        current_key = get_time_key()
        encrypted = encrypt_message(message, current_key)
        decrypted = decrypt_message(encrypted, current_key)

        self.chat3.chat_display.append(f"You: {message}")
        self.chat2.chat_display.append(f"Encrypted [key={current_key}]: {encrypted}")
        self.chat1.chat_display.append(f"Decrypted: {decrypted}")


if __name__ == '__main__':
    app = qtw.QApplication([])
    main_app = MainApp()
    app.exec()