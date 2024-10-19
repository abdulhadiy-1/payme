from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from a import pul_otkazish

class PaymeUI(QWidget):
    def __init__(self):
        super().__init__()
        self.wallet = 100000.0  
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Payme")
        self.showMaximized()

        layout = QVBoxLayout()

        self.wallet_lbl = QLabel(f"Sizning hisobingizda {self.wallet} so'm bor")
        self.wallet_lbl.setStyleSheet("font-size: 25px; font-weight: bold")
        layout.addWidget(self.wallet_lbl)

        self.hist_label = QLabel("", self)
        self.hist_label.setStyleSheet("font-size: 18px; color: #2c3e50;")
        layout.addWidget(self.hist_label)

        logo_label = QLabel("PAYME", self)
        logo_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #3498db;")
        layout.addWidget(logo_label)
        layout.addStretch()

        self.amount_label = QLabel("Summa kiriting:", self)
        self.amount_label.setStyleSheet("font-size: 18px; color: #2c3e50;")
        self.amount_edit = QLineEdit(self)
        self.amount_edit.setPlaceholderText("Masalan, 100000 so'm")
        self.amount_edit.setStyleSheet("font-size: 24px; padding: 10px;")
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_edit)
        layout.addStretch()

        self.CARD_label = QLabel("Karta raqamini kiriting:", self)
        self.CARD_label.setStyleSheet("font-size: 18px; color: #2c3e50;")
        self.CARD_edit = QLineEdit(self)
        self.CARD_edit.setPlaceholderText("XXXX-XXXX-XXXX-XXXX")
        self.CARD_edit.setStyleSheet("font-size: 24px; padding: 10px;")
        layout.addWidget(self.CARD_label)
        layout.addWidget(self.CARD_edit)
        layout.addStretch()

        btn_layout = QHBoxLayout()

        self.pay_button = QPushButton("To'lash", self)
        self.pay_button.setStyleSheet("font-size: 24px;background-color: #3498db;color: white;padding: 15px;border-radius: 10px;")
        self.pay_button.clicked.connect(self.process_payment)
        btn_layout.addWidget(self.pay_button)

        self.history_button = QPushButton("Tarixni ko'rish", self)
        self.history_button.setStyleSheet("font-size: 24px;background-color: #e74c3c;color: white;padding: 15px;border-radius: 10px;")
        self.history_button.clicked.connect(self.show_history)
        btn_layout.addWidget(self.history_button)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def process_payment(self):
        amount = self.amount_edit.text()
        CARD = self.CARD_edit.text()

        if not amount or not CARD:
            self.show_message("Iltimos, barcha maydonlarni to'ldiring.", "Xatolik")
            return

        

        result = pul_otkazish(amount, CARD, self.wallet)

        self.show_message(result, "Natija")

        if result == "Money transferred successfully":
            self.wallet -= int(amount)
            self.wallet_lbl.setText(f"Sizning hisobingizda {self.wallet} so'm bor")

    def show_message(self, message, title):
        self.amount_edit.clear()
        self.CARD_edit.clear()

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def show_history(self):
        self.CARD_edit.hide()
        self.amount_edit.hide()
        self.CARD_label.hide()
        self.amount_label.hide()
        self.pay_button.hide()
        self.history_button.hide()

        
        with open("history.txt", "r") as file:
            history = file.read()
        if not history:
            history = "Tarix mavjud emas."

        self.hist_label.setText(history)

        self.back_button = QPushButton("Ortga", self)
        self.back_button.setStyleSheet("font-size: 24px;background-color: #2ecc71;color: white;padding: 15px;border-radius: 10px;")
        self.back_button.clicked.connect(self.go_back)
        self.layout().addWidget(self.back_button)

    def go_back(self):
        self.hist_label.setText("")
        self.CARD_edit.show()
        self.amount_edit.show()
        self.CARD_label.show()
        self.amount_label.show()
        self.pay_button.show()
        self.history_button.show()
        self.back_button.hide()


app = QApplication([])
window = PaymeUI()
window.show()
app.exec_()
