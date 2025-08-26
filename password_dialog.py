from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFrame, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap


class PasswordDialog(QDialog):
    def __init__(self, parent=None, mode="verify", attempts=1):
        super().__init__(parent)
        self.mode = mode  # "create" or "verify"
        self.attempts = attempts
        self.password = ""
        
        self.setWindowTitle("SecureJournal - Authentication")
        self.setModal(True)
        
        # Adjust dialog size based on mode and error state
        if self.mode == "verify":
            if self.attempts > 1:
                self.setFixedSize(480, 500)  # Larger for error messages and warning
            else:
                self.setFixedSize(480, 420)  # Smaller for single password field
        else:
            self.setFixedSize(480, 520)  # Larger for password creation
            
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.MSWindowsFixedSizeDialogHint)
        
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header section
        header = QFrame()
        header.setObjectName("header")
        
        # Adjust header height based on error state
        if self.mode == "verify" and self.attempts > 1:
            header.setFixedHeight(140)  # More space for error message
            header_layout = QVBoxLayout(header)
            header_layout.setContentsMargins(40, 25, 40, 25)
            header_layout.setSpacing(12)  # More spacing for error
        else:
            header.setFixedHeight(120)
            header_layout = QVBoxLayout(header)
            header_layout.setContentsMargins(40, 25, 40, 25)
            header_layout.setSpacing(8)
        
        header_layout.setAlignment(Qt.AlignCenter)
        
        # App icon and title
        app_title = QLabel("🐘 SecureJournal")
        app_title.setObjectName("appTitle")
        app_title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        app_title.setAlignment(Qt.AlignCenter)
        
        # Subtitle based on mode
        if self.mode == "create":
            subtitle = QLabel("Create your master password")
            subtitle.setObjectName("subtitle")
        else:
            if self.attempts > 1:
                subtitle = QLabel(f"Incorrect password. Attempt {self.attempts} of 3")
                subtitle.setObjectName("subtitleError")
            else:
                subtitle = QLabel("Enter your master password")
                subtitle.setObjectName("subtitle")
        
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(app_title)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header)
        
        # Content section
        content = QFrame()
        content.setObjectName("content")
        content_layout = QVBoxLayout(content)
        
        # Adjust spacing based on mode and error state
        if self.mode == "verify":
            if self.attempts > 1:
                # More space needed for error state with warning
                content_layout.setContentsMargins(50, 30, 50, 30)
                content_layout.setSpacing(20)
            else:
                # Compact for normal verification
                content_layout.setContentsMargins(50, 25, 50, 25)
                content_layout.setSpacing(18)
        else:
            # Normal spacing for password creation
            content_layout.setContentsMargins(50, 40, 50, 40)
            content_layout.setSpacing(25)
        
        if self.mode == "create":
            # Password creation fields
            password_section = QFrame()
            password_layout = QVBoxLayout(password_section)
            password_layout.setSpacing(15)
            
            # Password field
            password_label = QLabel("Password")
            password_label.setObjectName("fieldLabel")
            password_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            
            self.password_input = QLineEdit()
            self.password_input.setObjectName("passwordInput")
            self.password_input.setEchoMode(QLineEdit.Password)
            self.password_input.setMinimumHeight(45)
            self.password_input.setPlaceholderText("Enter a secure password...")
            self.password_input.setFont(QFont("Segoe UI", 12))
            
            # Confirm password field
            confirm_label = QLabel("Confirm Password")
            confirm_label.setObjectName("fieldLabel")
            confirm_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            
            self.confirm_input = QLineEdit()
            self.confirm_input.setObjectName("passwordInput")
            self.confirm_input.setEchoMode(QLineEdit.Password)
            self.confirm_input.setMinimumHeight(45)
            self.confirm_input.setPlaceholderText("Confirm your password...")
            self.confirm_input.setFont(QFont("Segoe UI", 12))
            
            password_layout.addWidget(password_label)
            password_layout.addWidget(self.password_input)
            password_layout.addWidget(confirm_label)
            password_layout.addWidget(self.confirm_input)
            
        else:
            # Single password field for verification
            password_section = QFrame()
            password_layout = QVBoxLayout(password_section)
            password_layout.setSpacing(15)
            
            password_label = QLabel("Password")
            password_label.setObjectName("fieldLabel")
            password_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            
            self.password_input = QLineEdit()
            self.password_input.setObjectName("passwordInput")
            self.password_input.setEchoMode(QLineEdit.Password)
            self.password_input.setMinimumHeight(45)
            self.password_input.setPlaceholderText("Enter your password...")
            self.password_input.setFont(QFont("Segoe UI", 12))
            
            password_layout.addWidget(password_label)
            password_layout.addWidget(self.password_input)
        
        # Show password checkbox
        self.show_password_cb = QCheckBox("Show password")
        self.show_password_cb.setObjectName("showPassword")
        self.show_password_cb.setFont(QFont("Segoe UI", 10))
        self.show_password_cb.stateChanged.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.show_password_cb)
        
        content_layout.addWidget(password_section)
        
        # Warning for verification mode
        if self.mode == "verify" and self.attempts > 1:
            warning = QLabel("⚠️ All data will be permanently deleted after 3 failed attempts!")
            warning.setObjectName("warningLabel")
            warning.setFont(QFont("Segoe UI", 10, QFont.Bold))
            warning.setAlignment(Qt.AlignCenter)
            warning.setWordWrap(True)
            content_layout.addWidget(warning)
        
        layout.addWidget(content, 1)
        
        # Button section
        button_section = QFrame()
        button_section.setObjectName("buttonSection")
        button_section.setFixedHeight(80)
        button_layout = QHBoxLayout(button_section)
        button_layout.setContentsMargins(50, 20, 50, 20)
        button_layout.setSpacing(15)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.setMinimumSize(110, 45)
        self.cancel_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.cancel_btn.clicked.connect(self.reject)
        
        if self.mode == "create":
            self.ok_btn = QPushButton("Create Password")
        else:
            self.ok_btn = QPushButton("Sign In")
        
        self.ok_btn.setObjectName("okButton")
        self.ok_btn.setMinimumSize(150, 45)
        self.ok_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.ok_btn.setDefault(True)
        self.ok_btn.clicked.connect(self.accept_password)
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.ok_btn)
        
        layout.addWidget(button_section)
        
        # Set focus and enter key handling
        self.password_input.returnPressed.connect(self.accept_password)
        if self.mode == "create":
            self.confirm_input.returnPressed.connect(self.accept_password)
        self.password_input.setFocus()
    
    def toggle_password_visibility(self, state):
        """Toggle password visibility"""
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
            if self.mode == "create":
                self.confirm_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            if self.mode == "create":
                self.confirm_input.setEchoMode(QLineEdit.Password)
    
    def accept_password(self):
        """Validate and accept password"""
        password = self.password_input.text().strip()
        
        if not password:
            self.show_error("Please enter a password.")
            return
        
        if self.mode == "create":
            # Validate password creation
            confirm_password = self.confirm_input.text().strip()
            
            if len(password) < 4:
                self.show_error("Password must be at least 4 characters long.")
                return
            
            if password != confirm_password:
                self.show_error("Passwords do not match.")
                return
        
        self.password = password
        self.accept()
    
    def show_error(self, message):
        """Show error message"""
        from PyQt5.QtWidgets import QMessageBox
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Invalid Input")
        msg_box.setText(message)
        msg_box.setStyleSheet(self.get_message_box_style())
        msg_box.exec_()
        
        self.password_input.setFocus()
        self.password_input.selectAll()
    
    def get_password(self):
        """Return the entered password"""
        return self.password
    
    def get_message_box_style(self):
        return """
            QMessageBox {
                background-color: #1a1a1a;
                color: #e0e0e0;
            }
            QMessageBox QLabel {
                color: #e0e0e0;
                font-size: 12px;
            }
            QMessageBox QPushButton {
                background-color: #6366f1;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #5b21b6;
            }
        """
    
    def apply_styles(self):
        """Apply modern dark theme"""
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                color: #e2e8f0;
                border: 1px solid #334155;
            }
            
            QFrame#header {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #3b82f6, stop: 1 #1d4ed8);
                border: none;
                border-radius: 0;
            }
            
            QLabel#appTitle {
                color: #ffffff;
                background: transparent;
                font-weight: 700;
            }
            
            QLabel#subtitle {
                color: rgba(255, 255, 255, 0.95);
                background: transparent;
                font-weight: 500;
            }
            
            QLabel#subtitleError {
                color: #ffffff;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #ef4444, stop: 1 #dc2626);
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
                border: 1px solid #f87171;
                margin: 5px 0px;
            }
            
            QFrame#content {
                background-color: #0f172a;
                border: none;
            }
            
            QLabel#fieldLabel {
                color: #cbd5e1;
                background: transparent;
                font-weight: 600;
                margin-bottom: 6px;
            }
            
            QLineEdit#passwordInput {
                background-color: #1e293b;
                color: #e2e8f0;
                border: 2px solid #475569;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                font-weight: 500;
            }
            
            QLineEdit#passwordInput:focus {
                border-color: #3b82f6;
                background-color: #334155;
                outline: none;
            }
            
            QLineEdit#passwordInput:hover {
                border-color: #64748b;
                background-color: #334155;
            }
            
            QLineEdit#passwordInput::placeholder {
                color: #94a3b8;
                font-style: italic;
            }
            
            QCheckBox#showPassword {
                color: #cbd5e1;
                font-size: 11px;
                font-weight: 500;
                spacing: 10px;
            }
            
            QCheckBox#showPassword::indicator {
                width: 18px;
                height: 18px;
            }
            
            QCheckBox#showPassword::indicator:unchecked {
                background-color: #1e293b;
                border: 2px solid #475569;
                border-radius: 4px;
            }
            
            QCheckBox#showPassword::indicator:unchecked:hover {
                border-color: #64748b;
                background-color: #334155;
            }
            
            QCheckBox#showPassword::indicator:checked {
                background-color: #3b82f6;
                border: 2px solid #3b82f6;
                border-radius: 4px;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNCA5TDIgNyIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
            }
            
            QCheckBox#showPassword::indicator:checked:hover {
                background-color: #1d4ed8;
                border-color: #1d4ed8;
            }
            
            QLabel#warningLabel {
                color: #ffffff;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #dc2626, stop: 1 #991b1b);
                border: 1px solid #f87171;
                border-radius: 8px;
                padding: 14px 18px;
                margin: 15px 0;
                font-weight: 600;
            }
            
            QFrame#buttonSection {
                background-color: #1e293b;
                border-top: 1px solid #475569;
                border-radius: 0;
            }
            
            QPushButton#okButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #3b82f6, stop: 1 #1d4ed8);
                color: #ffffff;
                border: none;
                border-radius: 8px;
                font-weight: 700;
                font-size: 12px;
            }
            
            QPushButton#okButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #1d4ed8, stop: 1 #1e40af);
            }
            
            QPushButton#okButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #1e40af, stop: 1 #1e3a8a);
            }
            
            QPushButton#cancelButton {
                background-color: #475569;
                color: #e2e8f0;
                border: 1px solid #64748b;
                border-radius: 8px;
                font-weight: 600;
                font-size: 12px;
            }
            
            QPushButton#cancelButton:hover {
                background-color: #64748b;
                border-color: #94a3b8;
                color: #ffffff;
            }
            
            QPushButton#cancelButton:pressed {
                background-color: #334155;
                border-color: #475569;
            }
        """)