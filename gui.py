import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QStackedWidget, QFileDialog,
    QMessageBox, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import tempfile
from docx import Document
import os

# Import epa
from epa import embed_message_epa, extract_message_epa

# Import us
from us import embed_message_us, extract_message_us

class MethodSelectionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Steganografia - Cyberbezpieczeństwo 25/26")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(30)

        buttons_layout = QVBoxLayout()

        row1 = QHBoxLayout()
        self.method1_btn = QPushButton("Method 1")
        self.method2_btn = QPushButton("Method 2")
        self.method3_btn = QPushButton("Method 3")

        for btn in [self.method1_btn, self.method2_btn, self.method3_btn]:
            btn.setMinimumSize(150, 80)
            btn.setFont(QFont("Arial", 12))
            row1.addWidget(btn)

        row2 = QHBoxLayout()
        self.method4_btn = QPushButton("Method 4")
        self.method5_btn = QPushButton("Method 5")
        self.method6_btn = QPushButton("Method 6")

        for btn in [self.method4_btn, self.method5_btn, self.method6_btn]:
            btn.setMinimumSize(150, 80)
            btn.setFont(QFont("Arial", 12))
            row2.addWidget(btn)

        buttons_layout.addLayout(row1)
        buttons_layout.addSpacing(20)
        buttons_layout.addLayout(row2)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)


class EmbedWidgetEPA(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("CHARACTER PAIR TEXT STEGANOGRAPHY BASED ON THE ENHANCED PARAGRAPH APPROACH\n[EMBED]")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        cover_label = QLabel("Cover Text:")
        cover_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(cover_label)

        cover_btn_layout = QHBoxLayout()
        self.load_cover_btn = QPushButton("Select file")
        self.load_cover_btn.clicked.connect(self.load_cover_text)
        cover_btn_layout.addWidget(self.load_cover_btn)
        cover_btn_layout.addStretch()
        layout.addLayout(cover_btn_layout)

        self.cover_text = QTextEdit()
        self.cover_text.setPlaceholderText("Provide or load cover text...")
        self.cover_text.setMinimumHeight(150)
        layout.addWidget(self.cover_text)

        layout.addSpacing(15)

        secret_label = QLabel("Secret Message:")
        secret_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(secret_label)

        self.secret_message = QTextEdit()
        self.secret_message.setPlaceholderText("Provide secret message...")
        self.secret_message.setMinimumHeight(40)
        self.secret_message.setMaximumHeight(60)
        layout.addWidget(self.secret_message)

        layout.addSpacing(15)

        key_label = QLabel("Key:")
        key_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(key_label)

        self.stego_key_display = QTextEdit()
        self.stego_key_display.setReadOnly(True)
        self.stego_key_display.setPlaceholderText("Key...")
        self.stego_key_display.setMinimumHeight(40)
        self.stego_key_display.setMaximumHeight(60)
        layout.addWidget(self.stego_key_display)

        layout.addSpacing(20)

        buttons_layout = QHBoxLayout()

        self.back_btn = QPushButton("Return to Methods")
        self.back_btn.setMinimumSize(120, 40)
        buttons_layout.addWidget(self.back_btn)

        buttons_layout.addStretch()

        self.embed_btn = QPushButton("Embed")
        self.embed_btn.setMinimumSize(120, 40)
        self.embed_btn.clicked.connect(self.perform_embed)
        buttons_layout.addWidget(self.embed_btn)

        self.extract_btn = QPushButton("Go to Extract")
        self.extract_btn.setMinimumSize(120, 40)
        buttons_layout.addWidget(self.extract_btn)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

        self.stego_content = None
        self.stego_key = None

    def clear_fields(self):
        self.cover_text.clear()
        self.secret_message.clear()
        self.stego_key_display.clear()
        self.stego_content = None
        self.stego_key = None

    def load_cover_text(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select cover file", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.cover_text.setPlainText(f.read())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Cannot load file:\n{str(e)}")

    def perform_embed(self):
        cover = self.cover_text.toPlainText().strip()
        secret = self.secret_message.toPlainText().strip()

        if not cover:
            QMessageBox.warning(self, "Warning", "Provide cover text!")
            return

        if not secret:
            QMessageBox.warning(self, "Warning", "Provide secret message!")
            return

        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as cover_file:
                cover_file.write(cover)
                cover_path = cover_file.name

            self.stego_key = embed_message_epa(cover_path, secret)

            self.stego_key_display.setPlainText(self.stego_key)

            os.unlink(cover_path)

            QMessageBox.information(self, "Success", "Message was hidden!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error occured while trying to embed:\n{str(e)}")

class ExtractWidgetEPA(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("CHARACTER PAIR TEXT STEGANOGRAPHY BASED ON THE ENHANCED PARAGRAPH APPROACH\n[EXTRACT]")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        stego_label = QLabel("Stego File:")
        stego_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(stego_label)

        stego_btn_layout = QHBoxLayout()
        self.load_stego_btn = QPushButton("Load stego file")
        self.load_stego_btn.clicked.connect(self.load_stego_file)
        stego_btn_layout.addWidget(self.load_stego_btn)
        stego_btn_layout.addStretch()
        layout.addLayout(stego_btn_layout)

        self.stego_text = QTextEdit()
        self.stego_text.setPlaceholderText("Provide or load stego file...")
        self.stego_text.setMinimumHeight(150)
        layout.addWidget(self.stego_text)

        layout.addSpacing(15)

        key_label = QLabel("Key:")
        key_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(key_label)

        self.key_text = QTextEdit()
        self.key_text.setPlaceholderText("Provide key...")
        self.key_text.setMinimumHeight(40)
        self.key_text.setMaximumHeight(60)
        layout.addWidget(self.key_text)

        layout.addSpacing(15)

        extracted_label = QLabel("Extracted Secret Message:")
        extracted_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(extracted_label)

        self.extracted_message = QTextEdit()
        self.extracted_message.setReadOnly(True)
        self.extracted_message.setPlaceholderText("Secret Message...")
        self.extracted_message.setMinimumHeight(40)
        self.extracted_message.setMaximumHeight(60)
        layout.addWidget(self.extracted_message)

        layout.addSpacing(20)

        buttons_layout = QHBoxLayout()

        self.back_btn = QPushButton("Return to Methods")
        self.back_btn.setMinimumSize(120, 40)
        buttons_layout.addWidget(self.back_btn)

        buttons_layout.addStretch()

        self.extract_btn = QPushButton("Extract")
        self.extract_btn.setMinimumSize(120, 40)
        self.extract_btn.clicked.connect(self.perform_extract)
        buttons_layout.addWidget(self.extract_btn)

        self.embed_btn = QPushButton("Go to Embed")
        self.embed_btn.setMinimumSize(120, 40)
        buttons_layout.addWidget(self.embed_btn)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def clear_fields(self):
        self.stego_text.clear()
        self.key_text.clear()
        self.extracted_message.clear()

    def load_stego_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choose stego file", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.stego_text.setPlainText(f.read())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Cannot load stego file:\n{str(e)}")

    def perform_extract(self):
        stego = self.stego_text.toPlainText().strip()
        key = self.key_text.toPlainText().strip()

        if not stego:
            QMessageBox.warning(self, "Warning", "Provide stego text!")
            return

        if not key:
            QMessageBox.warning(self, "Warning", "Provide key!")
            return

        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as stego_file:
                stego_file.write(stego)
                stego_path = stego_file.name

            secret_message = extract_message_epa(stego_path, key)

            self.extracted_message.setPlainText(secret_message)

            os.unlink(stego_path)

            QMessageBox.information(self, "Success", "Secret message extracted!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error occured while extracting secret message:\n{str(e)}")

class EmbedWidgetUS(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.input_path = None
        # self.stego_output_doc = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("UNICODE For Hiding Information In A Text Document\n[EMBED]")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        cover_label = QLabel("Cover Text:")
        cover_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(cover_label)

        self.cover_text = QTextEdit()
        self.cover_text.setPlaceholderText("Provide cover text...")
        self.cover_text.setMinimumHeight(150)
        layout.addWidget(self.cover_text)

        # cover_btn_layout = QHBoxLayout()
        # self.load_cover_btn = QPushButton("... or select file")
        # self.load_cover_btn.clicked.connect(self.load_cover_text)
        # cover_btn_layout.addWidget(self.load_cover_btn)
        # cover_btn_layout.addStretch()
        # layout.addLayout(cover_btn_layout)

        layout.addSpacing(15)

        secret_label = QLabel("Secret Message:")
        secret_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(secret_label)

        self.secret_message = QTextEdit()
        self.secret_message.setPlaceholderText("Provide secret message...")
        self.secret_message.setMinimumHeight(40)
        self.secret_message.setMaximumHeight(60)
        layout.addWidget(self.secret_message)

        layout.addSpacing(20)

        buttons_layout = QHBoxLayout()

        self.back_btn = QPushButton("Return to Methods")
        self.back_btn.setMinimumSize(120, 40)
        buttons_layout.addWidget(self.back_btn)

        buttons_layout.addStretch()

        self.embed_btn = QPushButton("Embed")
        self.embed_btn.setMinimumSize(120, 40)
        self.embed_btn.clicked.connect(self.perform_embed)
        buttons_layout.addWidget(self.embed_btn)

        self.extract_btn = QPushButton("Go to Extract")
        self.extract_btn.setMinimumSize(120, 40)
        buttons_layout.addWidget(self.extract_btn)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def clear_fields(self):
        self.cover_text.clear()
        self.secret_message.clear()

    def perform_embed(self):
        cover = self.cover_text.toPlainText().strip()
        secret = self.secret_message.toPlainText().strip()

        if not cover:
            QMessageBox.warning(self, "Warning", "Provide cover text!")
            return

        if not secret:
            QMessageBox.warning(self, "Warning", "Provide secret message!")
            return

        try:
            output_doc = embed_message_us(cover, secret)

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save stego file",
                "",
                "Word Documents (*.docx)"
            )

            if file_path:
                try:
                    if not file_path.endswith(".docx"):
                        file_path += ".docx"
                    output_doc.save(file_path)
                    QMessageBox.information(
                        self, "Success", f"File saved:\n{file_path}"
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self, "Error", f"Cannot save file:\n{e}"
                    )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error occured while trying to embed:\n{str(e)}")

class ExtractWidgetUS(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_text = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("UNICODE For Hiding Information In A Text Document\n[EXTRACT]")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        stego_label = QLabel("Stego File:")
        stego_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(stego_label)

        stego_btn_layout = QHBoxLayout()
        self.load_stego_btn = QPushButton("Load stego file")
        self.load_stego_btn.clicked.connect(self.load_stego_file)
        stego_btn_layout.addWidget(self.load_stego_btn)
        stego_btn_layout.addStretch()
        layout.addLayout(stego_btn_layout)

        self.file_path_label = QLabel("")
        stego_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(self.file_path_label)

        layout.addSpacing(15)

        extracted_label = QLabel("Extracted Secret Message:")
        extracted_label.setFont(QFont("Arial", 11))
        layout.addWidget(extracted_label)

        self.extracted_message = QTextEdit()
        self.extracted_message.setReadOnly(True)
        self.extracted_message.setPlaceholderText("Secret Message...")
        self.extracted_message.setMinimumHeight(40)
        self.extracted_message.setMaximumHeight(60)
        layout.addWidget(self.extracted_message)

        layout.addSpacing(1000)

        buttons_layout = QHBoxLayout()

        self.back_btn = QPushButton("Return to Methods")
        self.back_btn.setMinimumSize(120, 40)
        buttons_layout.addWidget(self.back_btn)

        buttons_layout.addStretch()

        self.extract_btn = QPushButton("Extract")
        self.extract_btn.setMinimumSize(120, 40)
        self.extract_btn.clicked.connect(self.perform_extract)
        buttons_layout.addWidget(self.extract_btn)

        self.embed_btn = QPushButton("Go to Embed")
        self.embed_btn.setMinimumSize(120, 40)
        buttons_layout.addWidget(self.embed_btn)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def clear_fields(self):
        self.input_text = None
        self.file_path_label.clear()
        self.extracted_message.clear()

    def load_stego_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choose stego file", "", "Word Documents (*.docx)"
        )
        if file_path:
            try:
                docx = Document(file_path)
                for p in docx.paragraphs:
                    if self.input_text is None:
                        self.input_text = p.text
                    else:
                        self.input_text += p.text
                self.file_path_label.setText(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Cannot read stego file:\n{str(e)}")

    def perform_extract(self):
        if self.input_text is None:
            QMessageBox.warning(self, "Warning", "Provide stego file!")
            return

        try:
            secret_message = extract_message_us(self.input_text)

            self.extracted_message.setPlainText(secret_message)

            QMessageBox.information(self, "Success", "Secret message extracted!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error occured while extracting secret message:\n{str(e)}")


class EmbedWidgetILSC(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.input_path = None
        # self.stego_output_doc = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Text Steganography on Sundanese Script using Improved Line Shift Coding\n[EMBED]")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        cover_label = QLabel("Cover Text:")
        cover_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(cover_label)

        self.cover_text = QTextEdit()
        self.cover_text.setPlaceholderText("Provide cover text...")
        self.cover_text.setMinimumHeight(150)
        layout.addWidget(self.cover_text)

        # cover_btn_layout = QHBoxLayout()
        # self.load_cover_btn = QPushButton("... or select file")
        # self.load_cover_btn.clicked.connect(self.load_cover_text)
        # cover_btn_layout.addWidget(self.load_cover_btn)
        # cover_btn_layout.addStretch()
        # layout.addLayout(cover_btn_layout)

        layout.addSpacing(15)

        secret_label = QLabel("Secret Message:")
        secret_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(secret_label)

        self.secret_message = QTextEdit()
        self.secret_message.setPlaceholderText("Provide secret message...")
        self.secret_message.setMinimumHeight(40)
        self.secret_message.setMaximumHeight(60)
        layout.addWidget(self.secret_message)

        layout.addSpacing(20)

        buttons_layout = QHBoxLayout()

        self.back_btn = QPushButton("Return to Methods")
        self.back_btn.setMinimumSize(120, 40)
        buttons_layout.addWidget(self.back_btn)

        buttons_layout.addStretch()

        self.embed_btn = QPushButton("Embed")
        self.embed_btn.setMinimumSize(120, 40)
        self.embed_btn.clicked.connect(self.perform_embed)
        buttons_layout.addWidget(self.embed_btn)

        self.extract_btn = QPushButton("Go to Extract")
        self.extract_btn.setMinimumSize(120, 40)
        buttons_layout.addWidget(self.extract_btn)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def clear_fields(self):
        self.cover_text.clear()
        self.secret_message.clear()

    def perform_embed(self):
        cover = self.cover_text.toPlainText().strip()
        secret = self.secret_message.toPlainText().strip()

        if not cover:
            QMessageBox.warning(self, "Warning", "Provide cover text!")
            return

        if not secret:
            QMessageBox.warning(self, "Warning", "Provide secret message!")
            return

        try:
            # TODO: replace
            output_doc = embed_message_us(cover, secret)

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save stego file",
                "",
                "Portable Document Format (*.pdf)"
            )

            if file_path:
                try:
                    if not file_path.endswith(".pdf"):
                        file_path += ".pdf"
                    # TODO: replace
                    output_doc.save(file_path)
                    QMessageBox.information(
                        self, "Success", f"File saved:\n{file_path}"
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self, "Error", f"Cannot save file:\n{e}"
                    )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error occured while trying to embed:\n{str(e)}")

class ExtractWidgetILSC(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_text = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Text Steganography on Sundanese Script using Improved Line Shift Coding\n[EXTRACT]")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        stego_label = QLabel("Stego File:")
        stego_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(stego_label)

        stego_btn_layout = QHBoxLayout()
        self.load_stego_btn = QPushButton("Load stego file")
        self.load_stego_btn.clicked.connect(self.load_stego_file)
        stego_btn_layout.addWidget(self.load_stego_btn)
        stego_btn_layout.addStretch()
        layout.addLayout(stego_btn_layout)

        self.file_path_label = QLabel("")
        stego_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(self.file_path_label)

        layout.addSpacing(15)

        extracted_label = QLabel("Extracted Secret Message:")
        extracted_label.setFont(QFont("Arial", 11))
        layout.addWidget(extracted_label)

        self.extracted_message = QTextEdit()
        self.extracted_message.setReadOnly(True)
        self.extracted_message.setPlaceholderText("Secret Message...")
        self.extracted_message.setMinimumHeight(40)
        self.extracted_message.setMaximumHeight(60)
        layout.addWidget(self.extracted_message)

        layout.addSpacing(1000)

        buttons_layout = QHBoxLayout()

        self.back_btn = QPushButton("Return to Methods")
        self.back_btn.setMinimumSize(120, 40)
        buttons_layout.addWidget(self.back_btn)

        buttons_layout.addStretch()

        self.extract_btn = QPushButton("Extract")
        self.extract_btn.setMinimumSize(120, 40)
        self.extract_btn.clicked.connect(self.perform_extract)
        buttons_layout.addWidget(self.extract_btn)

        self.embed_btn = QPushButton("Go to Embed")
        self.embed_btn.setMinimumSize(120, 40)
        buttons_layout.addWidget(self.embed_btn)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def clear_fields(self):
        self.input_text = None
        self.file_path_label.clear()
        self.extracted_message.clear()

    def load_stego_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose stego file",
            "",
            "Portable Document Format (*.pdf)",
        )

        if file_path:
            try:
                # TODO: replace
                docx = Document(file_path)
                for p in docx.paragraphs:
                    if self.input_text is None:
                        self.input_text = p.text
                    else:
                        self.input_text += p.text
                self.file_path_label.setText(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Cannot read stego file:\n{str(e)}")

    def perform_extract(self):
        if self.input_text is None:
            QMessageBox.warning(self, "Warning", "Provide stego file!")
            return

        try:
            # TODO: replace
            secret_message = extract_message_us(self.input_text)

            self.extracted_message.setPlainText(secret_message)

            QMessageBox.information(self, "Success", "Secret message extracted!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error occured while extracting secret message:\n{str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Steganografia")
        self.setMinimumSize(800, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.method_selection = MethodSelectionWidget()
        self.embed_widget_epa = EmbedWidgetEPA()
        self.extract_widget_epa = ExtractWidgetEPA()
        self.embed_widget_us = EmbedWidgetUS()
        self.extract_widget_us = ExtractWidgetUS()
        self.embed_widget_ilsc = EmbedWidgetILSC()
        self.extract_widget_ilsc = ExtractWidgetILSC()

        self.stack.addWidget(self.method_selection)
        self.stack.addWidget(self.embed_widget_epa)
        self.stack.addWidget(self.extract_widget_epa)
        self.stack.addWidget(self.embed_widget_us)
        self.stack.addWidget(self.extract_widget_us)
        self.stack.addWidget(self.embed_widget_ilsc)
        self.stack.addWidget(self.extract_widget_ilsc)

        self.method_selection.method1_btn.clicked.connect(self.show_embed_epa)
        self.method_selection.method2_btn.clicked.connect(self.show_embed_us)
        self.method_selection.method3_btn.clicked.connect(self.show_embed_ilsc)

        self.method_selection.method4_btn.clicked.connect(self.show_embed_epa)
        self.method_selection.method5_btn.clicked.connect(self.show_embed_epa)
        self.method_selection.method6_btn.clicked.connect(self.show_embed_epa)

        self.embed_widget_epa.back_btn.clicked.connect(self.show_method_selection)
        self.embed_widget_epa.extract_btn.clicked.connect(self.show_extract_epa)
        self.extract_widget_epa.back_btn.clicked.connect(self.show_method_selection)
        self.extract_widget_epa.embed_btn.clicked.connect(self.show_embed_epa)

        self.embed_widget_us.back_btn.clicked.connect(self.show_method_selection)
        self.embed_widget_us.extract_btn.clicked.connect(self.show_extract_us)
        self.extract_widget_us.back_btn.clicked.connect(self.show_method_selection)
        self.extract_widget_us.embed_btn.clicked.connect(self.show_embed_us)

        self.embed_widget_ilsc.back_btn.clicked.connect(self.show_method_selection)
        self.embed_widget_ilsc.extract_btn.clicked.connect(self.show_extract_ilsc)
        self.extract_widget_ilsc.back_btn.clicked.connect(self.show_method_selection)
        self.extract_widget_ilsc.embed_btn.clicked.connect(self.show_embed_ilsc)

        self.show_method_selection()

    def show_method_selection(self):
        self.embed_widget_epa.clear_fields()
        self.extract_widget_epa.clear_fields()
        self.extract_widget_us.clear_fields()
        self.embed_widget_us.clear_fields()
        self.stack.setCurrentWidget(self.method_selection)

    def show_embed_epa(self):
        self.stack.setCurrentWidget(self.embed_widget_epa)

    def show_extract_epa(self):
        self.stack.setCurrentWidget(self.extract_widget_epa)

    def show_embed_us(self):
        self.stack.setCurrentWidget(self.embed_widget_us)

    def show_extract_us(self):
        self.stack.setCurrentWidget(self.extract_widget_us)

    def show_embed_ilsc(self):
        self.stack.setCurrentWidget(self.embed_widget_ilsc)

    def show_extract_ilsc(self):
        self.stack.setCurrentWidget(self.extract_widget_ilsc)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
