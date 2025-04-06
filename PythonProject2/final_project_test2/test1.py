from PyQt6.QtWidgets import QApplication, QWidget, QDialog
from ui.dialogs.admin_sign_up_dialog import AdminSignUpDialog

if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    dialog = AdminSignUpDialog(window)
    result = dialog.exec()
    window.show()
    if result == QDialog.DialogCode.Accepted:
        signup_data = dialog.get_signup_info()
        if signup_data:
            print("Admin signed up with:")
            print(f"Username: {signup_data['username']}")
            print(f"Password: {signup_data['password']}") #never store password in real code!
        else:
            print("Signup data not available.")
    else:
        print("Admin sign up canceled")

    app.exec()