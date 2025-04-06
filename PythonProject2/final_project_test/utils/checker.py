import re
class Checker:
    def is_name_valid(self, name):
        if not name:
            return False, "Name cannot be empty."
        if not isinstance(name, str):
            return False, "Name must be a string."
        if not re.match(r"^[a-zA-Z\s]+$", name):
            return False, "Name contains unexpected characters."
        return True, "Your Name is valid."

    def is_username_valid(self, username: str) -> tuple[bool, str]:
        """Validate username format.
        
        Rules:
        - Cannot be empty
        - Must be a string
        - Can contain letters, numbers, and underscores
        - Must start with a letter
        - Length between 3-20 characters
        
        Args:
            username: Username to validate
            
        Returns:
            tuple: (is_valid, message)
        """
        if not username:
            return False, "Username cannot be empty."
        
        if not isinstance(username, str):
            return False, "Username must be a string."
        
        if len(username) < 6:
            return False, "Username must be at least 3 characters long."
            
        if len(username) > 20:
            return False, "Username cannot exceed 20 characters."
        
        if not username[0].isalpha():
            return False, "Username must start with a letter."
        
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", username):
            return False, "Username can only contain letters, numbers, and underscores."
        
        return True, "Username is valid."

    def is_password_valid(self, password: str) -> tuple[bool, str]:
        # Check if the password is at least 12 characters long
        if len(password) < 12:
            return False, "Password must be at least 12 characters long."

        # Check if the password contains at least one lowercase letter
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter."

        # Check if the password contains at least one uppercase letter
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter."

        # Check if the password contains at least one digit
        if not re.search(r"\d", password):
            return False, "Password must contain at least one digit."

        # Check if the password contains at least one special character
        if not re.search(r"[@$!%*#?&]", password):
            return False, "Password must contain at least one special character."
        # If all checks pass, return True and an empty error message
        return True, ""
    def is_password_match_valid(self, password, conf_password):
        if password == conf_password:
            return True, ""
        return False, "Your password is not matched to its confirm"

    def is_age_valid(self, age):
        if age:
            if not age.isdigit():
                return False, "Age must be a number."
            if int(age) <= 0:
                return False, "Age must be a positive number."
        return True, ""

    def is_phone_number_valid(self, phone_number: str) -> tuple[bool, str]:
        # Check if the phone number is a string of digits
        if not phone_number.isdigit():
            return False, "Phone number must be a string of digits."

        # Check if the phone number starts with 0
        if not phone_number.startswith("0"):
            return False, "Phone number must start with 0."

        # Check if the phone number has a length between 9 and 11
        if not 9 <= len(phone_number) <= 11:
            return False, "Phone number must have a length between 9 and 11."

        # If all checks pass, return True and an empty error message
        return True, ""

    def is_address_valid(self, address):
        if not address:
            return False, "Address cannot be left blank."
        return True, ""

    def is_interest_valid(self, interest):
        return True, ""

    def is_gender_valid(self, checked_button):
        if not checked_button:
            return False, "Please select an option male or female."
        return True, ""
