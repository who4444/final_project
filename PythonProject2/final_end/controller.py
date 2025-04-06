## Importing the necessary libraries
# Standard library imports
import sys
import resources.resources_rc as resources_rc

# Third-party imports
import matplotlib.pyplot as plt
from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QMessageBox,
    QLabel,
    QVBoxLayout,
    QPushButton
)

# Local application imports
# Resources
from resources.config import ICONS
# UI
from ui.design import Ui_Library
from ui.dialogs.style_dialog import CustomDialog
from ui.window import MainWindowControl
from ui.dialogs.aboutus_dialog import AboutUsDialog
from ui.dialogs.aboutReadiverse import AboutAppDialog
from ui.dialogs.book_dialog import BookDialog
from ui.dialogs.calendar_dialog import CalendarDialog
from ui.dialogs.delete_review_dialog import DeleteReview
from ui.dialogs.notification_dialog import NotificationDialog
from ui.readers.epub_reader import EpubReader
from ui.dialogs.profile_dialog import UserProfileDialog
from ui.dialogs.admin_sign_up_dialog import AdminSignUpDialog
from ui.dialogs.add_genre_dialog import AddGenreDialog
from ui.message_box.custom_message_box import CustomMessageBox

# Database
from database.admin import AdminManager
from database.user import UserManager
# Utils
from utils.table.table import TableWidgetManager
from utils.checker import Checker
from utils.helper_functions import toggle_echo_mode, moderate_reviews
# Configurations
from database.config import DB_CONFIG
from resources.config import BOOKS_DIR

class Ui_Library_Control(Ui_Library):
    def __init__(self):
        super().__init__()
        connection_string = DB_CONFIG['CONNECTION_STRING_1']
        ## Initialize managers
        # Database managers
        self.user_manager = UserManager(connection_string)
        self.admin_manager = AdminManager(connection_string)
        # UI managers
        self.table_manager = TableWidgetManager()
        self.current_user_id = None
        self.unhashed_password = None

    def setupUi(self, MainWindow):
        # Store main window reference and setup base UI
        self.mainwindow = MainWindow
        super().setupUi(self.mainwindow)
        # Initialize state variables
        self.pages = {}
        
        # Setup UI components
        self.populate_pages_dict()
        self.setupButton(self.Pbutton_apply_edit_user)
        self.frame_user_profile.setEnabled(False)

        # Connect signals and load data
        self.connect_all()
        self.switch_to_page("start_page")

    def setupButton(self,selected_button:QPushButton):
        selected_button.setEnabled(False)

    def connect_all(self):
        """Connect all UI signals to their respective slots"""
        # Core UI connections
        self.connect_menubar_actions()
        self.connect_navigation()
        
        # Authentication connections
        self.connect_admin_auth()
        self.connect_user_auth()
        
        # Admin management connections
        self.connect_admin_user_management()
        self.connect_admin_book_management()
        self.connect_admin_membership_management()
        self.connect_admin_review_management()
        self.connect_admin_category_management()
        self.manage_tabwidget.currentChanged.connect(self.load_admin_table)
        
        # User feature connections
        self.connect_user_profile_management()
        self.connect_user_book_management()
        self.connect_user_membership_management()
        self.connect_user_notifications_management()
        self.connect_user_password_management()
        self.user_info_page_tab.currentChanged.connect(self.load_user_table)

    def connect_menubar_actions(self):
        self.actionReturn_to_start_page.triggered.connect(self.return_start_page)
        self.actionExit.triggered.connect(self.close_window)
        self.about_us_menu.triggered.connect(self.about_us_display)
        self.about_library_menu.triggered.connect(self.about_app_display)
    def connect_navigation(self):
        self.Pbutton_admin.clicked.connect(lambda: self.switch_to_page("admin_page"))
        self.Pbutton_admin.clicked.connect(self.admin_initialize)
        self.Pbutton_user.clicked.connect(lambda: self.switch_to_page("user_page"))

    def connect_admin_auth(self):
        self.Pbutton_submit_signin_admin.clicked.connect(self.admin_sign_in)
        self.Pbutton_showpass_admin.clicked.connect(self.show_pass_admin)
        self.Pbutton_logout_admin.clicked.connect(self.admin_logout)

    def connect_admin_user_management(self):
        self.Pbutton_user_remove_admin.clicked.connect(self.remove_user_admin)
        self.Pbutton_user_view_admin.clicked.connect(self.view_selected_user)

    def connect_admin_book_management(self):
        self.Pbutton_book_remove_admin.clicked.connect(self.remove_book)
        self.Pbutton_bood_add_admin.clicked.connect(self.add_book_admin)
        self.Pbutton_book_modify_admin.clicked.connect(self.modify_book_admin)
        self.Line_search_book_admin.textChanged.connect(self.search_book_admin)
        self.Pbutton_visualize_stats_book_admin.clicked.connect(self.visualize_top_books)
    
    def connect_admin_review_management(self):
        self.Pbutton_review_delete_admin.clicked.connect(self.delete_review)

    def connect_admin_membership_management(self):
        self.Pbutton_application_approve_admin.clicked.connect(self.approve_application)
        self.Pbutton_application_reject_admin.clicked.connect(self.reject_application)
    def connect_admin_category_management(self):
        self.Pbutton_add_genre_admin.clicked.connect(self.add_genre)
        self.Pbutton_visualize_stats_category_admin.clicked.connect(self.visualize_genre_stats)

    def connect_user_auth(self):
        self.Pbutton_submit_signin_user.clicked.connect(self.user_sign_in)
        self.Pbutton_submit_signup_user.clicked.connect(self.user_sign_up)
        self.Pbutton_show_password_signin_user.clicked.connect(self.show_pass_user)
        self.Pbutton_logout_user.clicked.connect(self.user_logout)

    def connect_user_profile_management(self):
        self.Pbutton_profile_edit_user.clicked.connect(self.edit_user_profile_enable)
        self.Pbutton_apply_edit_user.clicked.connect(self.applychanges_user_profile)

    def connect_user_book_management(self):
        self.Pbutton_add_book_user.clicked.connect(self.user_borrow)
        self.Pbutton_book_read_user.clicked.connect(self.user_read)
        self.Pbutton_book_remove_user.clicked.connect(self.user_return_book)
        self.Line_search_explore_user.textChanged.connect(self.search_books_user)
        self.Pbutton_review_submit_user.clicked.connect(self.submit_review_user)
        self.Pbutton_book_reviews_see_user.clicked.connect(self.load_reviews_user)
        self.Pbutton_rank_on_review_user.clicked.connect(lambda: self.load_book_rankings_user("review_count"))
        self.Pbutton_rank_on_borrow_user.clicked.connect(lambda: self.load_book_rankings_user("borrow_count"))
    
    def connect_user_membership_management(self):
        self.Pbutton_apply_membership.clicked.connect(self.apply_membership)
    def connect_user_notifications_management(self):
        self.Pbutton_notifications_user.clicked.connect(self.show_notifications)
    def connect_user_password_management(self):
        self.Pbutton_submit_change_pass_user.clicked.connect(self.change_password_user)

    # General function
    def close_window(self):
        self.mainwindow.close()

    def closeEvent(self, event):
        
        reply = CustomMessageBox.question(
            self.mainwindow,
            "Close Application",
            "Are you sure you want to exit?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No,
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
    def populate_pages_dict(self):
        self.pages["start_page"] = self.start_page
        self.pages["admin_page"] = self.admin_page
        self.pages["user_page"] = self.user_page
        self.pages["manage_page"] = self.manage_page
        self.pages["user_info_page"] = self.user_info_page  
    def return_start_page(self):
        """
        Displays a warning message box to confirm if the user wants to return to the start page,
        BUT ONLY if the current page is NOT already the start page.

        """

        if self.current_page_name == "start_page":
            return  # Exit the function immediately if already on the start page
        # If we reach here, it means current_page_name is NOT "start_page", so proceed with warning
        reply = CustomMessageBox.question(
                self.mainwindow,
                'Confirmation',  # Title of the message box
                "Are you sure you want to return to the start page?\nAny unsaved changes may be lost.", # Warning message
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, # Buttons: Yes and No (PyQt6)
                QMessageBox.StandardButton.No  # Default button: No
            )

        if reply == QMessageBox.StandardButton.Yes:
            
            if self.current_page_name == 'user_page':
                self.clear_all_user_authentication()
            if self.current_page_name == 'admin_page':
                self.clear_all_admin_authentifications()
            if self.current_page_name == 'manage_page':
                self.clear_all_admin()
            if self.current_page_name == 'user_info_page':
                self.clear_all_user()# PyQt6
                
            self.switch_to_page("start_page")
            self.admin_manager.disconnect()
            self.user_manager.disconnect()

    def about_us_display(self):
        about_us = AboutUsDialog()  # Create the dialog instance
        about_us.exec()
    def about_app_display(self):
        about_app = AboutAppDialog()
        about_app.exec()

    def switch_to_page(self, page_name):
        page = self.pages.get(page_name)
        if page:
            self.stackedWidget.setCurrentWidget(page)
            self.current_page_name = page_name
        else:
            print(f"Page '{page_name}' not found.")   
    def load_user_table(self):
        # Connect to database
        self.user_manager.connect()
            # Load user's books
        headers, data = self.user_manager.get_books()
        self.table_manager.load_data(
            self.table_books_exploration_user, 
            data, 
            headers, 
            'books'
            )
            # Load user's inventory
        headers, data = self.user_manager.get_my_inventory()
        self.table_manager.load_data(
            self.table_books_inventory_user, 
            data,
            headers, 
            'inventory'
            )
            # Load books'ranking
        headers, data = self.user_manager.get_book_rankings("daily")
        
        self.table_manager.load_data(
            self.table_daily_ranking_user,
            data,
            headers,
            'ranking'
        )
        headers, data = self.user_manager.get_book_rankings("week")
        self.table_manager.load_data(
            self.table_weekly_ranking_user,
            data,
            headers,
            'ranking'
        )
        headers, data = self.user_manager.get_book_rankings("month")
        self.table_manager.load_data(
            self.table_monthly_ranking_user,
            data,
            headers,
            'ranking'
        )
        self.current_ranking_type = "borrow_count"
    def clear_all_user(self):
        self.load_user_table()
        # explore tab
        self.Line_search_explore_user.clear()
        self.Plain_Line_browser_reviews_user.clear()
        # inventory tab
        self.plainText_user_review.clear()
        # membership tab
        self.Line_name_membership_user.clear()
        self.Plain_Line_membership_reason_user.clear()
        # Change password tab
        self.Line_old_password_user.clear()
        self.Line_new_password_user.clear()
        self.Line_conf_new_password_user.clear()
        #profile tab
        self.applychanges_user_profile()
        
    def load_admin_table(self):
        # Connect to database
        self.admin_manager.connect()
        # Load books table
        headers, data = self.admin_manager.get_books()
        self.table_manager.load_data(
            self.table_books_admin, 
            data, 
            headers, 
            'books'
        )
        
        # Load users table
        headers, data = self.admin_manager.get_users()
        self.table_manager.load_data(
            self.table_users_list_admin, 
            data, 
            headers, 
            'users'
        )
        # Load borrowing history
        headers, data = self.admin_manager.get_borrowing_history()
        self.table_manager.load_data(
            self.table_borrow_history_admin, 
            data, 
            headers, 
            'history'
        )
        # Load membership applications
        headers, data = self.admin_manager.get_membership_applications()
        self.table_manager.load_data(
            self.table_user_application_admin, 
            data, 
            headers, 
            'membership'
        )
        # Load reviews
        headers, data = self.admin_manager.get_review()
        self.table_manager.load_data(
            self.table_review_display_admin,
            data,
            headers,
            'reviews'
        )
        headers, data = self.admin_manager.get_categories()
        self.table_manager.load_data(
            self.table_category_admin, 
            data,
            headers,
            'category'
        )
        self.load_pending_applications()
    def clear_all_admin(self):
        self.Line_search_book_admin.clear()
    def clear_all_user_authentication(self):
        # User Sign in tab
        self.Line_username_signin_user.clear()
        self.Line_password_signin_user.clear()
        self.Line_password_signin_user.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        # User Sign up tab
        self.Line_username_signup_user.clear()
        self.Line_password_signup_user.clear()
        self.Line_password_confirm_signup_user.clear()
        self.Line_name_signup_user.clear()
        self.Line_address_signup_user.clear()
        self.DateEdit_Birthday_signup_user.setDate(QDate.currentDate())
        self.Line_phone_number_signup_user.clear()
        self.Plain_Line_interest_signup_user.clear()
        self.Rbutton_female_signup_user.setChecked(False)
        self.Rbutton_male_signup_user.setChecked(False)
    def clear_all_admin_authentifications(self):
        self.Line_admin_username.clear()
        self.Line_admin_password.clear()
        self.Line_admin_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    ## General user functions
    def user_sign_in(self):
        username = self.Line_username_signin_user.text()
        password = self.Line_password_signin_user.text()
        
        login_result = self.user_manager.check_login(username, password)
        if login_result:
            # Set session data
            self.current_user_id = self.user_manager.user_id
            self.unhashed_password = password
            
            # Switch page and load data
            self.switch_to_page("user_info_page")
            self.load_user_info_profile()
            self.update_membership_status_label()
            self.load_user_table()
            self.update_notifications_icon()
            
            # Show welcome message and check overdue books
            CustomMessageBox.information(self.mainwindow, "Login Success", 
                                f"Welcome to Readiverse, {username}!")
            self.overdue_warning()
            self._clear_signin_form()
        else:
            CustomMessageBox.warning(self.mainwindow, "Login Failed", "Incorrect username or password.")
    def _clear_signin_form(self):
        self.Line_username_signin_user.clear()
        self.Line_password_signin_user.clear()

    def user_sign_up(self):
        """Handle user signup process with validation and error handling."""
        # Get input values
        username = self.Line_username_signup_user.text()
        password = self.Line_password_signup_user.text()
        conf_password = self.Line_password_confirm_signup_user.text()
        name = self.Line_name_signup_user.text()
        address = self.Line_address_signup_user.text()
        DOB = self.DateEdit_Birthday_signup_user.date().toString("yyyy-MM-dd")
        phone_number = self.Line_phone_number_signup_user.text()
        interest = self.Plain_Line_interest_signup_user.toPlainText()

        errors = {}
        checker = Checker()

        # Gender handling
        checked_button = self.button_group_gender_signup_user.checkedButton()
        gender = checked_button.text() if checked_button else None

        # Check for existing username first

        if self.user_manager.is_username_taken(username):
            CustomMessageBox.warning(
                self.mainwindow,
                "Username Error",
                "This username is already taken. Please choose another."
            )
            self.Line_username_signup_user.clear()
            self.Line_username_signup_user.setFocus()
            return
        checker = Checker()
        success, message = checker.is_password_match_valid(password, conf_password)
        if not success:
            CustomMessageBox.warning(self.mainwindow, "Password Error", message)
            return
        success, message = checker.is_password_valid(password)
        if not success:
            CustomMessageBox.warning(self.mainwindow, "Password Error", message)
            return
        success, errors = self.validate_user_info(username, password, name, address, phone_number, gender, interest)
        if not success:
            error_messages = "\n".join(errors.values())  # Just the messages
            CustomMessageBox.warning(self.mainwindow, "Validation Error", error_messages)
            return
        try:
            # Register user
            if self.user_manager.add_registered_info(
                name, gender, username, password, 
                DOB, address, phone_number, interest
            ):
                # Update UI
                self.switch_to_page("user_info_page")
                self.load_user_info_profile()
                self.load_user_table()
                # Send welcome notifications
                self.user_manager.send_welcome_notifications()
                self.update_notifications_icon()
                
                CustomMessageBox.information(
                    self.mainwindow,
                    "Welcome!",
                    "Registration successful! Check your notifications for helpful tips."
                )
        except Exception as e:
            CustomMessageBox.critical(
                self.mainwindow,
                "Registration Error",
                f"Failed to complete registration: {str(e)}"
            )
            
    def validate_user_info(self, User_name: str, Password: str, 
                       Name: str, Address: str, Phone_num: str, 
                       Gender: str, Interests: str) -> bool:
        # Validate user information.
        checker = Checker()

        validations = [
            (checker.is_username_valid(User_name), "username"),
            (checker.is_password_valid(Password), "password"),
            (checker.is_name_valid(Name), "name"),
            (checker.is_phone_number_valid(Phone_num), "phone_number"),
            (checker.is_address_valid(Address), "address"),
            (checker.is_gender_valid(Gender), "gender"),
            (checker.is_interest_valid(Interests), "interests")
        ]

        errors = {}
        for (is_valid, message), field in validations:
            if not is_valid:
                errors[field] = message

        if errors:
            return False, errors
        return True, None

    def _clear_signup_form(self):
        # Clear text inputs
        self.Line_username_signup_user.clear()
        self.Line_password_signup_user.clear()
        self.Line_password_confirm_signup_user.clear()
        self.Line_name_signup_user.clear()
        self.Line_address_signup_user.clear()
        self.DateEdit_Birthday_signup_user.setDate(QDate.currentDate())
        self.Line_phone_number_signup_user.clear()
        self.Plain_Line_interest_signup_user.clear()
        
        # Uncheck gender radio buttons
        self.Cbox_male_profile_user.setChecked(False)
        self.Cbox_female_profile_user.setChecked(False)
    def user_logout(self):
        reply = CustomMessageBox.question(
            self.mainwindow,
            "Warning",
            "Are you sure you want to logout, unsaved changes will be lost?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        # Reset user state and navigate to the start page
        self.clear_all_user()
        self.current_user_id = None
        self.switch_to_page("start_page")
        self.user_manager.logout()
    def show_pass_user(self):
        toggle_echo_mode(self.Line_password_signin_user)
    
    # User info functions
    # User profile functions

    def edit_user_profile_enable(self):
        self.frame_user_profile.setEnabled(True)
        self.Pbutton_apply_edit_user.setEnabled(True)
        self.Pbutton_profile_edit_user.setEnabled(False)
        self.Label_mode_user_profile.setText("Edit Mode")
        self.Label_mode_user_profile.setEnabled(True)

    def load_user_info_profile(self):
        user_info = self.user_manager.get_profile()
        if user_info:
            username, name, gender, address, dob, phone_num, interests = user_info
            self.Line_username_profile_user.setText(username)
            self.Line_name_profile_user.setText(name)
            
            self.Cbox_male_profile_user.setChecked(gender == "Male") if gender == "Male" else self.Cbox_female_profile_user.setChecked(gender == "Female")
            self.Line_address_profile_user.setText(address)

            dob_date = QDate.fromString(dob, "yyyy-MM-dd")
            self.DateEdit_Birthday_profile_user.setDate(dob_date)

            self.Line_phone_number_profile_user.setText(str(phone_num))
            self.Plain_Line_interest_profile_user.setPlainText(interests)

    def applychanges_user_profile(self):
        self.frame_user_profile.setEnabled(False)
        self.Pbutton_profile_edit_user.setEnabled(True)
        self.Pbutton_apply_edit_user.setEnabled(False)
        self.change_profile_user()
        self.Label_mode_user_profile.setEnabled(False)
        self.Label_mode_user_profile.setText("View Mode")
    def change_profile_user(self):
          # Get logged-in user ID
        new_username = self.Line_username_profile_user.text()
        new_name = self.Line_name_profile_user.text()
        new_dob = self.DateEdit_Birthday_profile_user.date().toString("yyyy-MM-dd")
        new_address = self.Line_address_profile_user.text()
        new_phone_number = self.Line_phone_number_profile_user.text()

        male_gender = self.Cbox_male_profile_user.isChecked()
        female_gender = self.Cbox_female_profile_user.isChecked()
        if male_gender:
            new_gender = "Male"
        elif female_gender:
            new_gender = "Female"
        else:
            new_gender = None

        new_interest = self.Plain_Line_interest_profile_user.toPlainText()

        try:
            print(f"Updating profile with: {new_username}, {new_name}, {new_address}, {new_phone_number}, {new_gender}, {new_dob}, {new_interest}")
            self.user_manager.update_profile(new_username, new_name, new_address, new_phone_number, new_gender, new_dob, new_interest)
        except Exception as e:
            print("Database update error:", e)
            CustomMessageBox.warning(self.mainwindow, "Error", "Failed to update profile.")
            return
        #Notification
        CustomMessageBox.information(
        self.mainwindow,  # Use msainwindow as parent.
        "Changes Applied",
        "Your profile changes have been applied successfully.",
        QMessageBox.StandardButton.Ok, #only have ok button.
    )
    # User book functions
    def submit_review_user(self):
        # Submit a review for the selected book.
        selected_row = self.table_books_inventory_user.currentRow()
        if selected_row < 0:
            CustomMessageBox.warning(self.mainwindow, "Review Error", 
                            "Please select a book to review.")
            return

        # Get book ID directly from column 0
        book_id_item = self.table_books_inventory_user.item(selected_row, 0)
        if not book_id_item:
            CustomMessageBox.warning(self.mainwindow, "Data Error", 
                            "Could not retrieve book information.")
            return
        
        book_id = book_id_item.text()

        # Get review text
        review = self.plainText_user_review.toPlainText().strip()
        if not review:
            CustomMessageBox.warning(self.mainwindow, "Review Error", 
                            "Please enter a review.")
            return

        # Check content
        if moderate_reviews(review):
            CustomMessageBox.warning(self.mainwindow, "Review Error", 
                            "Your review has been rejected due to inappropriate content.")
            return

        # Submit review
        self.user_manager.submit_review(book_id, review)
        CustomMessageBox.information(self.mainwindow, "Review Submitted", 
                            "Your review has been submitted successfully.")
        self.plainText_user_review.clear()
    def load_reviews_user(self):
        # Get selected book
        selected_row = self.table_books_exploration_user.currentRow()
        if selected_row < 0:
            CustomMessageBox.warning(self.mainwindow, "Selection Required", 
                              "Please select a book to view reviews.")
            return

        # Get book ID
        book_id_item = self.table_books_exploration_user.item(selected_row, 0)
        if not book_id_item:
            CustomMessageBox.warning(self.mainwindow, "Data Error", 
                              "Could not retrieve book information.")
            return
            
        book_id = book_id_item.text()

        # Fetch reviews
        column_names, reviews = self.user_manager.get_review(book_id)
        
        if not reviews:
            self.Plain_Line_browser_reviews_user.setPlainText(
                "No reviews yet. Read and be the first to leave a review!"
            )
            return

        # Format reviews using list comprehension and join
        formatted_reviews = "\n\n".join(
            f"Review #{review[0]} by {review[1]} on {review[3]}:\n{review[2]}" 
            for review in reviews
        )
        
        self.Plain_Line_browser_reviews_user.setPlainText(formatted_reviews)
    def search_books_user(self):
        # Search and display books based on search text.
        search_text = self.Line_search_explore_user.text().strip()
        headers, data = self.user_manager.get_books(search_text)
        self.table_manager.load_data(
            self.table_books_exploration_user,
            data,
            headers,
            'books'
        )
    def user_borrow(self):
        # Check for overdue books
        if self.overdue_warning():
            CustomMessageBox.warning(self.mainwindow, "Borrow Warning", "You have overdue books! Please return them before proceeding.")
            return

        # Get selected book ID
        selected_row = self.table_books_exploration_user.currentRow()
        if selected_row < 0:
            CustomMessageBox.warning(self.mainwindow, "Selection Error", "Please select a book to borrow.")
            return

        book_id_item = self.table_books_exploration_user.item(selected_row, 0)
        if not book_id_item or not book_id_item.text():
            CustomMessageBox.warning(self.mainwindow, "Data Error", "Could not retrieve book information.")
            return

        book_id = int(book_id_item.text())
        
        # Check if the user already borrowed this book
        if self.user_manager.is_book_borrowed(book_id):
            CustomMessageBox.warning(self.mainwindow, "Already Borrowed", "You have already borrowed this book.")
            return

        #  Check if the user has reached the borrowing limit
        if not self.user_manager.able_to_borrow():
            CustomMessageBox.warning(self.mainwindow, "Borrowing Denied", "You have reached your borrowing limit. Return some books before borrowing more.")
            return

        #  Open the calendar and validate return date
        calendar_dialog = CalendarDialog()
        if not calendar_dialog.exec():  # If the user cancels, stop the process
            return

        return_date = calendar_dialog.get_selected_date()
        # Processes the book borrowing request and handles user feedback.
        try:
            result = self.user_manager.add_borrow_record(book_id, return_date)

            if result is True:
                CustomMessageBox.information(self.mainwindow, "Success", f"Book borrowed! Return by {return_date}")
            else:
                CustomMessageBox.warning(self.mainwindow, "Error", "An unexpected error occurred.")
        except Exception as e:
            CustomMessageBox.critical(self.mainwindow, "Error", f"Failed to borrow book: {str(e)}")

    def user_read(self):
        # Open EPUB reader for selected book.
        selected_row = self.table_books_inventory_user.currentRow()
        if selected_row < 0:
            CustomMessageBox.warning(self.mainwindow, "Selection Required", 
                              "Please select a book to read.")
            return

        # Get Book ID directly from column 0
        book_id_item = self.table_books_inventory_user.item(selected_row, 0)
        if not book_id_item:
            CustomMessageBox.warning(self.mainwindow, "Data Error", 
                              "Could not retrieve book information.")
            return

        # Get book inventory data
        _, book_inventory = self.user_manager.get_my_inventory()
        book_id = book_id_item.text()

        # Find book link directly using book ID
        book_link = None
        for book in book_inventory:
            if str(book[0]) == book_id:  # Match book ID
                book_link = book[2]  # Get EPUB link
                break

        book_path = BOOKS_DIR / book_link
        if not book_path.exists():
            CustomMessageBox.warning(self.mainwindow, "Error", 
                                  "Could not find EPUB file for this book.")
            return
        self.read_book_window = EpubReader(book_path, parent=self.mainwindow)
        self.read_book_window.show()

    def user_return_book(self):
        selected_row = self.table_books_inventory_user.currentRow()
        if selected_row < 0:
            CustomMessageBox.warning(self.mainwindow, "Selection Required", 
                            "Please select a book to return.")
            return

        # Get book ID and title directly from columns
        book_id_item = self.table_books_inventory_user.item(selected_row, 0)  # Book_Id is in column 0
        book_title_item = self.table_books_inventory_user.item(selected_row, 1)  # Title is in column 1
        
        if not book_id_item or not book_title_item:
            CustomMessageBox.warning(self.mainwindow, "Data Error", 
                            "Could not retrieve book information.")
            return

        book_id = book_id_item.text()
        book_title = book_title_item.text()

        # Confirm return
        reply = CustomMessageBox.question(
            self.mainwindow, 
            "Return Confirmation",
            f"Are you sure you want to return '{book_title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.user_manager.return_book(book_id)
            CustomMessageBox.information(self.mainwindow, "Success", 
                                "Book returned successfully.")
    def load_book_rankings_user(self, rank_by="borrow_count"):
        # Validate rank_by input
        valid_rank_by_options = {"borrow_count", "review_count"}

        if rank_by not in valid_rank_by_options:
            print(f"Invalid rank_by value: {rank_by}. Defaulting to 'borrow_count'.")
            rank_by = "borrow_count"  # Default to Borrow_Count if invalid
        
        # Load daily rankings
        headers, data = self.user_manager.get_book_rankings(rank_by, "daily", "DESC")
        if data:
            self.table_manager.load_data(self.table_daily_ranking_user, data, headers, "ranking")

        # Load weekly rankings
        headers, data = self.user_manager.get_book_rankings(rank_by,"weekly", "DESC")
        if data:
            self.table_manager.load_data(self.table_weekly_ranking_user, data, headers, "ranking")

        # Load monthly rankings
        headers, data = self.user_manager.get_book_rankings(rank_by, "monthly","DESC")
        if data:
            self.table_manager.load_data(self.table_monthly_ranking_user, data, headers, "ranking")
        if self.current_ranking_type != rank_by:
        
            self.table_manager.rearrange_columns(self.table_daily_ranking_user, headers)
            self.table_manager.rearrange_columns(self.table_weekly_ranking_user, headers)
            self.table_manager.rearrange_columns(self.table_monthly_ranking_user, headers)
            self.current_ranking_type = rank_by

    # user membership functions
    def overdue_warning(self):
        overdue_books = self.user_manager.get_overdue_books()
        if overdue_books:
            overdue_message = ("You have overdue books, please return them:\n")
            for borrow_id, title, return_date in overdue_books:
                overdue_message += f"- {title} (Due: {return_date})\n"

            CustomMessageBox.warning(self.mainwindow, "Overdue Books", overdue_message)
            return True  # Prevent borrowing
        return False
    def apply_membership(self):
        name = self.Line_name_membership_user.text()
        reason = self.Plain_Line_membership_reason_user.toPlainText()
        self.Line_name_membership_user.clear()
        self.Plain_Line_membership_reason_user.clear()
        if name and reason:
            if self.user_manager.get_membership_status() == 'Premium':
                CustomMessageBox.warning(self.mainwindow, "Membership Premium", "You're already a premium user.")
            else:
                self.user_manager.apply_membership(reason)
                CustomMessageBox.information(self.mainwindow, "Membership Apply", "Membership applied. The admin will review your application soon")
        else:
            CustomMessageBox.warning(self.mainwindow, "Application Error", "Please enter both fields.")
    def update_membership_status_label(self):
        status = self.user_manager.get_membership_status()
        self.label_membership_status_user.setText(f"Membership Status: {status}")

        if status == "Premium":
            self.label_membership_status_user.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.label_membership_status_user.setStyleSheet("color: black;")
    # User notification functions
    def show_notifications(self):
        
        notifications = self.user_manager.get_notifications()    

        if not notifications:
            CustomMessageBox.information(self.mainwindow, "No Notifications", "You have no notifications yet")
        else:
            headers, data = notifications
            noti_dialog = NotificationDialog(self.mainwindow,data,headers)
            noti_dialog.show_notifications()
            # Mark notifications as read
            self.user_manager.mark_notifications_as_read()
            self.update_notifications_icon()  # Update icon after reading

    def update_notifications_icon(self):
        # Update notification icon based on unread notifications.
        unread_count = self.user_manager.get_unread_notification_count()
        
        # Define icon paths
        alert_icon = ICONS['notification']['alert']
        bell_icon = ICONS['notification']['bell']

        # Check if icons exist
        if not alert_icon.exists():
            print(f"Alert icon not found at: {alert_icon.absolute()}")
            return
            
        if not bell_icon.exists():
            print(f"Bell icon not found at: {bell_icon.absolute()}")
            return

        # Set icon based on unread count
        if unread_count > 0:
            self.Pbutton_notifications_user.setIcon(QIcon(str(alert_icon)))
        else:
            self.Pbutton_notifications_user.setIcon(QIcon(str(bell_icon)))
    # User password management
    def change_password_user(self):
        # Changes the user's password after verification.
        # Get logged-in user ID
        user_id = self.current_user_id
        old_password = self.Line_old_password_user.text()  # Add this line!
        new_password = self.Line_new_password_user.text()
        confirm_password = self.Line_conf_new_password_user.text()

        # Input Validation (Add these checks!)
        if not old_password:
            CustomMessageBox.warning(self.mainwindow, "Password Change", "Please enter your old password.")
            return
        if not new_password:
            CustomMessageBox.warning(self.mainwindow, "Password Change", "Please enter your new password.")
            return
        checker = Checker()
        success, message = checker.is_password_valid(new_password)
        if not success:
            CustomMessageBox.warning(self.mainwindow, "Password Change", message)
            return
        success, message = checker.is_password_match_valid(new_password, confirm_password)
        if not success:
            CustomMessageBox.warning(self.mainwindow, "Password Change", message)
            return
        # Verify old password
        print(old_password, type(old_password))
        if not self.user_manager.check_password(old_password):
            CustomMessageBox.warning(self.mainwindow, "Password Change", "Incorrect old password.")
            return
        # Change password
        if self.user_manager.update_user_password(new_password):
            CustomMessageBox.information(self.mainwindow, "Password Changed", "Password changed successfully.")
            # Clear password fields (optional)
            self.Line_old_password_user.clear()
            self.Line_new_password_user.clear()
            self.Line_conf_new_password_user.clear()
        else:
            CustomMessageBox.warning(self.mainwindow, "Password Change", "Failed to change password. Try again.")
    
    # Admin functions
    
    ## Admin authentication functions
    def admin_initialize(self):
        if self.admin_manager.is_admin_exists():
            return
        sign_up_dialog = AdminSignUpDialog(self.mainwindow)
        result = sign_up_dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            data_record = sign_up_dialog.get_signup_info()
            admin_name = data_record['username']
            admin_password = data_record['password']
            try:
                self.admin_manager.add_admin_record(admin_name,admin_password)
            except Exception as e:
                CustomMessageBox.warning(self.mainwindow, "Sign Up Failed", f"Failed to initialize admin record. Error: {str(e)}")
        
    def admin_sign_in(self):
        if not self.admin_manager.is_admin_exists():
            CustomMessageBox.information(self.mainwindow, "Admin Not Initialized", "Admin record is not initialized\nCreate a new one.")
            return
        admin_name = self.Line_admin_username.text()
        password = self.Line_admin_password.text()
        if self.admin_manager.verify_admin_login(admin_name, password):
            self.Line_admin_username.clear()
            self.Line_admin_password.clear()
            self.switch_to_page("manage_page")
            self.load_admin_table()
            CustomMessageBox.information(self.mainwindow, "Login Success", "Welcome Admin!")
        else:
            CustomMessageBox.warning(self.mainwindow, "Login Failed", "Incorrect admin username or password.")
    def admin_logout(self):
        reply = CustomMessageBox.question(
            self.mainwindow,
            "Logout Confirmation",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.switch_to_page("admin_page")
            
            # Clear tables
            self.clear_all_admin()
            self.table_books_admin.setRowCount(0)
            self.table_users_list_admin.setRowCount(0)
            self.table_user_application_admin.setRowCount(0)
            self.table_borrow_history_admin.setRowCount(0)
            # Disconnect database
            self.admin_manager.logout()
    
    def show_pass_admin(self):
        toggle_echo_mode(self.Line_admin_password)
    ## Admin User Management functions
    def remove_user_admin(self):
        # Validate selection
        selected_row = self.table_users_list_admin.currentRow()
        if selected_row < 0:
            CustomMessageBox.warning(
                self.mainwindow, 
                'Selection Required', 
                'Please select a user to remove.'
            )
            return
        # Get user ID
        user_id_item = self.table_users_list_admin.item(selected_row, 0)
        if not user_id_item:
            CustomMessageBox.warning(
                self.mainwindow, 
                'Data Error', 
                'Could not retrieve user information.'
            )
            return
        user_id = user_id_item.text()
        user_name = self.table_users_list_admin.item(selected_row, 1).text()

        # Confirm deletion
        reply = CustomMessageBox.question(
            self.mainwindow,
            "Delete Confirmation",
            f"Are you sure you want to delete user '{user_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.admin_manager.delete_user(user_id):
                self.table_users_list_admin.removeRow(selected_row)
                CustomMessageBox.information(
                    self.mainwindow,
                    "Success",
                    "User deleted successfully."
                )
                self.load_admin_table()
            else:
                CustomMessageBox.warning(
                    self.mainwindow,
                    "Error",
                    "Failed to delete user."
                )
    def view_selected_user(self):
        row = self.table_users_list_admin.currentRow()
        if row < 0:
            CustomMessageBox.warning(self.mainwindow, "Selection Required", "Please select a user to view.")
            return
        headers, data = self.admin_manager.get_specific_user(
            self.table_users_list_admin.item(row, 0).text()
        )
        
        if data:
            dialog = UserProfileDialog(headers, data[0], self.mainwindow)
            dialog.exec()
    
    
    ## Admin Book Management functions
    def search_book_admin(self):
        """Search and display books based on search text."""
        search_text = self.Line_search_book_admin.text().strip()
        headers, data = self.admin_manager.get_books(search_text)
        self.table_manager.load_data(
            self.table_books_admin,
            data,
            headers,
            'books'
        )

    def modify_book_admin(self):
        selected_row = self.table_books_admin.currentRow()
        
        if selected_row < 0:
            CustomMessageBox.warning(self.mainwindow, "Selection Required", "Please select a book to modify.")
            return
        book_id = int(self.table_books_admin.item(selected_row,0).text())
        
        book_details = self.admin_manager.get_book_detail(book_id)
        if not book_details:
            CustomMessageBox.warning(self.mainwindow, "Error", "Could not retrieve book details.")
            return
        title = book_details[0]
        genre_id = book_details[1] - 1
        author = book_details[2]
        description = book_details[3]
        cover_link = book_details[4]
        epub_link = book_details[5]
        
        # Open the AddBookDialog with existing book data pre-filled
        dialog = BookDialog(self.admin_manager, self.mainwindow)
        
        dialog.setWindowTitle('Modify Book')
        
        dialog.load_data(title,genre_id, author, description, cover_link, epub_link)
        
        # Pre-fill the dialog with book details

        if dialog.exec() == QDialog.DialogCode.Accepted:  # Proceed if the dialog was accepted
            book_data = dialog.get_book_data()
            
            success = self.admin_manager.update_book(
                book_data['title'],
                book_data['genre'],
                book_data['author'],
                book_data['description'],
                book_data['cover_link'],
                book_data['epub_link'],
                book_id
            )

            if success:
                CustomMessageBox.information(self.mainwindow, "Success", "Book modified successfully.")
                self.load_admin_table()  # Refresh the book table
            else:
                CustomMessageBox.warning(self.mainwindow, "Warning", "Failed to modify book.")

    def remove_book(self):
        selected_row = self.table_books_admin.currentRow()
        if selected_row < 0:
            CustomMessageBox.warning(self.mainwindow, 'Warning', 'You need to choose a book to remove.')
            return

        book_id_item = self.table_books_admin.item(selected_row, 0)
        if not book_id_item:
            CustomMessageBox.warning(self.mainwindow, 'Warning', 'Could not retrieve book information.')
            return

        book_id = book_id_item.text()

        # Confirmation dialog before deleting the book
        reply = CustomMessageBox.question(
            self.mainwindow, "Delete Confirmation", "Are you sure?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        # Remove from UI and database
        self.table_books_admin.removeRow(selected_row)
        self.admin_manager.delete_book(book_id)
        book_title_item = self.table_books_admin.item(selected_row, 1)
        if not book_title_item:
            return
        book_title = book_title_item.text()
        
        message = f"The book {book_title} has been deleted"
        self.load_admin_table()
        self.admin_manager.add_general_notification(message)

    def add_book_admin(self):
        dialog = BookDialog(self.admin_manager, self.mainwindow)

        if dialog.exec() == QDialog.DialogCode.Accepted:  # Only proceeds if the dialog is accepted (valid input)
            book_data = dialog.get_book_data()
            success = self.admin_manager.add_book(
                book_data['title'],
                book_data['description'],
                book_data['genre'],
                book_data['author'],
                book_data['cover_link'],
                book_data['epub_link'],
            )
            if success:
                CustomMessageBox.information(self.mainwindow, "Success", "Book added successfully.")
                self.load_admin_table()  # Refresh the book table
            else:
                CustomMessageBox.warning(self.mainwindow, "Warning", "Failed to add book.")
                return

    def visualize_top_books(self):
        try:
            # Get the row count
            row_count = self.table_books_admin.rowCount()

            # Extract book titles from table
            book_titles = [self.table_books_admin.item(row, 1).text() for row in range(row_count)]

            # Extract borrowed counts from table
            borrowed_counts = [int(self.table_books_admin.item(row, 5).text()) for row in range(row_count)]

            # Extract review counts from table
            review_counts = [int(self.table_books_admin.item(row, 6).text()) for row in range(row_count)]

            # Get the top 5 books with the highest borrowed count
            top_5_indices = sorted(range(len(borrowed_counts)), key=lambda i: borrowed_counts[i], reverse=True)[:5]
            top_5_book_titles = [book_titles[i] for i in top_5_indices]
            top_5_borrowed_counts = [borrowed_counts[i] for i in top_5_indices]
            top_5_review_counts = [review_counts[i] for i in top_5_indices]

            # Create a figure with two subplots
            fig, axs = plt.subplots(1, 2, figsize=(12, 6))

            # Create a bar chart for borrowed count in the first subplot
            axs[0].bar(top_5_book_titles, top_5_borrowed_counts)
            axs[0].set_title('Top 5 Books by Borrowed Count')
            axs[0].set_xlabel('Book Title')
            axs[0].set_ylabel('Borrowed Count')
            axs[0].tick_params(axis='x', rotation=90)

            # Create a bar chart for review count in the second subplot
            axs[1].bar(top_5_book_titles, top_5_review_counts)
            axs[1].set_title('Top 5 Books by Review Count')
            axs[1].set_xlabel('Book Title')
            axs[1].set_ylabel('Review Count')
            axs[1].tick_params(axis='x', rotation=90)

            # Show the figure
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Failed to visualize top books: {e}")

    ## Admin Category Management functions
    def add_genre(self):
        add_genre_dialog = AddGenreDialog(self.admin_manager, self.mainwindow)
        if add_genre_dialog.exec() == QDialog.DialogCode.Accepted:
            genre_name = add_genre_dialog.get_genre_name()
            try:
                self.admin_manager.add_genre(genre_name)
                CustomMessageBox.information(self.mainwindow, "Success", f"Genre '{genre_name}' added successfully.")
            except Exception as e:
                CustomMessageBox.warning(self.mainwindow, "Error", f"Failed to add genre: {str(e)}")
            self.load_admin_table()
    def visualize_genre_stats(self):
        try:
            # Get the row count
            row_count = self.table_category_admin.rowCount()

            # Extract genres from table
            genres = [self.table_category_admin.item(row, 1).text() for row in range(row_count)]

            # Extract max borrow counts from table
            max_borrow_counts = [int(self.table_category_admin.item(row, 3).text()) for row in range(row_count)]

            # Extract book counts from table
            book_counts = [int(self.table_category_admin.item(row, 4).text()) for row in range(row_count)]

            # Get the top 5 genres with the highest max borrow count
            top_5_genres = sorted(zip(genres, max_borrow_counts), key=lambda x: x[1], reverse=True)[:5]
            top_5_genres_names = [genre[0] for genre in top_5_genres]
            top_5_max_borrow_counts = [genre[1] for genre in top_5_genres]

            # Create a figure with two subplots
            fig, axs = plt.subplots(1, 2, figsize=(12, 6))

            # Create a bar chart for max borrow count in the first subplot
            axs[0].bar(top_5_genres_names, top_5_max_borrow_counts)
            axs[0].set_title('Top 5 Genres by Book the has max borrow count')
            axs[0].set_xlabel('Genre')
            axs[0].set_ylabel('Max Borrow Count')

            # Create a pie chart for book count in the second subplot
            axs[1].pie(book_counts, labels=genres, autopct='%1.1f%%')
            axs[1].set_title('Book Proposition by Genre')

            # Show the figure
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Failed to visualize genre stats: {e}")
    
    ## Admin Membership Management functions
    def load_pending_applications(self):
        headers, data = self.admin_manager.get_membership_applications()
        self.table_manager.load_data(
            self.table_user_application_admin,
            data,
            headers,
            'membership'
        )

    def approve_application(self):

        # Get selected application
        selected_row = self.table_user_application_admin.currentRow()
        if selected_row < 0:
            CustomMessageBox.warning(
                self.mainwindow, 
                "Selection Required", 
                "Please select an application to approve."
            )
            return

        # Get application ID
        application_id_item = self.table_user_application_admin.item(selected_row, 0)
        if not application_id_item:
            CustomMessageBox.warning(
                self.mainwindow, 
                "Data Error", 
                "Could not retrieve application information."
            )
            return

        # Confirm approval
        application_id = application_id_item.text()
        confirmation = CustomMessageBox.question(
            self.mainwindow,
            "Approve Application",
            "Are you sure you want to approve this membership application?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if confirmation != QMessageBox.StandardButton.Yes:
            return

        try:
            # Process approval
            self.admin_manager.approve_membership(application_id)
            CustomMessageBox.information(
                self.mainwindow,
                "Success",
                "Application approved successfully."
            )
            self.load_admin_table()
        except Exception as e:
            CustomMessageBox.critical(
                self.mainwindow,
                "Error",
                f"Failed to approve application: {str(e)}"
            )
            
    def reject_application(self):
        selected_row = self.table_user_application_admin.currentRow()
        if selected_row < 0:
            CustomMessageBox.warning(self.mainwindow, "Selection Required", "Please select an application to reject.")
            return
        application_id_item = self.table_user_application_admin.item(selected_row, 0)
        if not application_id_item:
            CustomMessageBox.warning(self.mainwindow, "Data Error", "Could not retrieve application information.")
            return
        application_id = application_id_item.text()
        confirmation = CustomMessageBox.question(self.mainwindow, "Reject Application", "Are you sure?",
                                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation == QMessageBox.StandardButton.Yes:
            self.admin_manager.reject_membership(application_id)
            CustomMessageBox.information(self.mainwindow, "Success", "Application rejected successfully.")
            self.load_admin_table()

    ## Admin Reviews Management functions

    def delete_review(self):
        selected_review = self.table_review_display_admin.currentRow()
        if selected_review < 0:
            CustomMessageBox.warning(self, "Delete Error", "Please select a review to delete.")
            return

        review_id = self.table_review_display_admin.item(selected_review, 0).text().strip()
        user_id = self.table_review_display_admin.item(selected_review, 1).text().strip()
        book_title = self.table_review_display_admin.item(selected_review,4).text().strip()

        # Show delete dialog
        dialog = DeleteReview()
        if dialog.exec():
            reason = dialog.get_selected_reason()
            # Delete review from database
            self.admin_manager.delete_book_review(review_id)

            # Notify user
            notification_text = f"Your review for '{book_title}' was deleted. Reason: {reason}."
            self.admin_manager.add_specific_notification(user_id, notification_text)

            CustomMessageBox.information(self.mainwindow, "Review Deleted", "The review has been successfully deleted.")
            # Refresh display
            self.load_admin_table()        
        
if __name__ == "__main__":
    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindowControl(Ui_Library_Control())
    window.show()
    sys.exit(app.exec())