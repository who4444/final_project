from database.library_db import LibraryDB
from datetime import datetime
import bcrypt
class UserManager(LibraryDB):
    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.user_id = None
    # Account Manager
    
    def _find_user_id(self, username: str) -> int:
        """Find user ID by username.
        
        Args:
            username: Username to look up
            
        Returns:
            int: Customer_Id if found, None if not found
        """
        self.connect()
        query = "SELECT Reader_ID FROM Reader WHERE User_Name = ?"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def is_username_taken(self, username: str) -> bool:
        """Check if username already exists.
        Args:
            username: Username to check
        Returns:
            bool: True if username exists, False otherwise
        """
        self.connect()
        query = "SELECT COUNT(*) FROM Reader WHERE User_Name = ?"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        return result[0] > 0

    def add_registered_info(self, Name, Gender, User_name, Password_hash, Age, Address, Phone_num, Interests):
        hashed_password = bcrypt.hashpw(Password_hash.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        query="""INSERT INTO Reader (Name, Gender, User_Name, Password_Hash, Age, Address, Phone_Number, Interests)
                    VALUES (?,?,?,?,?,?,?,?)"""
        self.cursor.execute(query,(Name, Gender, User_name, hashed_password, Age, Address, Phone_num, Interests))
        self.conn.commit()
        self._update_new_user_id()
        return True

    def _update_new_user_id(self):
        query = "SELECT MAX(Reader_ID) FROM Reader"
        self.cursor.execute(query)
        new_user_id = self.cursor.fetchone()[0]
        self.user_id = new_user_id

    def get_profile(self):
        self.cursor.execute("SELECT User_Name, Name,Gender, Address, Age, Phone_Number, Interests FROM Reader WHERE Reader_ID = ?", (self.user_id,))
        return self.cursor.fetchone()
    def update_profile(self, User_name: str, Name: str, 
                    Address: str, Phone_num: str, Gender: str, 
                    Age: int, Interests: str) -> None:
        """Update current user's profile."""
        self.cursor.execute(
            """UPDATE Reader 
            SET User_Name = ?, Name = ?, Address = ?, 
                Phone_Number = ?, Gender = ?, Age = ?, 
                Interests = ? 
            WHERE Reader_ID = ?""",
            (User_name, Name, Address, Phone_num, 
            Gender, Age, Interests, self.user_id)
        )
        self.conn.commit()
    def check_login(self, username: str, input_password: str) -> bool:
        """Verify user credentials and set user_id if valid.
        Args:
            username: Username to check
            input_password: Password to verify
            
        Returns:
            bool: True if credentials valid, False otherwise
        """
        self.connect()
        query = """SELECT Reader_ID, Password_Hash 
                FROM Reader 
                WHERE User_Name = ?"""
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        
        if result is None:
            return False
            
        customer_id, stored_hashed_password = result
        
        if bcrypt.checkpw(
            input_password.encode('utf-8'), 
            stored_hashed_password.encode('utf-8')
        ):
            self.user_id = customer_id  # Set user_id on successful login
            return True
        return False
    
    def logout(self):
        """Logout and close connection"""
        self.user_id = None
        self.disconnect()
    # Book Operations
    def get_books(self, search_text=None):
        if (search_text):  # If search text is provided, filter by title
            query = """SELECT Book_ID, Title, Genre, Author, Description FROM Book 
                       JOIN Genre ON Book.Genre_ID = Genre.Genre_ID 
                       WHERE Title LIKE ?"""
            self.cursor.execute(query, (f"%{search_text}%",))
        else:  # If no search text, return all books
            query = """SELECT Book_ID, Genre, Title, Author, Description FROM Book 
                       JOIN Genre ON Book.Genre_ID = Genre.Genre_ID"""
            self.cursor.execute(query)

        data = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]  # Fetch column names dynamically
        return column_names, data
    def get_my_inventory(self) -> tuple:
        """Get current user's borrowed books with return status.
        
        Returns:
            tuple: (column_names, data) where data contains
            (book_id, title, pdf_link, return_date, status)
        """
        self.cursor.execute("""
            SELECT 
                BorrowedBook.Book_ID,
                Book.Title,
                Book.Book_Link,
                FORMAT(BorrowedBook.Borrow_Date, 'yyyy-MM-dd') as Borrow_Date,
                FORMAT(BorrowedBook.Return_Date, 'yyyy-MM-dd') as Return_Date,
                CASE 
                    WHEN BorrowedBook.Returned = 0 THEN 'Not Returned'
                    WHEN BorrowedBook.Return_Date < GETDATE() THEN 'Overdue'
                    ELSE 'Returned'
                END as Status
            FROM BorrowedBook 
            INNER JOIN Book ON BorrowedBook.Book_ID = Book.Book_ID
            WHERE Reader_ID = ? 
            ORDER BY BorrowedBook.Return_Date DESC
        """, (self.user_id,))
        
        data = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        return column_names, data

    def able_to_borrow(self):
        """Checks if the user has reached their borrowing limit."""
        
        self.cursor.execute("SELECT Membership_Status FROM Reader WHERE Reader_ID = ?", (self.user_id,))
        membership_status = self.cursor.fetchone()

        if membership_status and membership_status[0] != 'Premium':
            MAX_BORROW_LIMIT = 10
            self.cursor.execute("""
                SELECT COUNT(*) FROM BorrowedBook 
                WHERE Reader_ID = ? AND Returned = 0
            """, (self.user_id,))
            borrowed_count = self.cursor.fetchone()[0]

            return borrowed_count < MAX_BORROW_LIMIT
        
        return True  # Premium members have no limit

    def is_book_borrowed(self, book_id):
        """Checks if the user has already borrowed a specific book."""
        
        self.cursor.execute("""
            SELECT 1 FROM BorrowedBook WHERE Reader_ID = ? AND Book_ID = ?
        """, (self.user_id, book_id))

        return self.cursor.fetchone() is not None

    def add_borrow_record(self, book_id, return_date):
        """Adds a new borrowing record to the database."""
        
        self.cursor.execute("""
            INSERT INTO BorrowedBook (Reader_ID, Book_ID, Borrow_Date, Return_Date, Returned)
            VALUES (?, ?, CURRENT_TIMESTAMP, ?, 0)
        """, (self.user_id, book_id, return_date))
        
        self.conn.commit()
        return True

    def return_book(self, book_id: int) -> None:
        """Return a borrowed book."""
        self.cursor.execute(
            """UPDATE BorrowedBook 
               SET Returned = 1, Return_Date = GETDATE() 
               WHERE Reader_ID = ? AND Book_ID = ?""",
            (self.user_id, book_id)
        )
        self.conn.commit()
    def get_overdue_books(self) -> list:
        """Get current user's overdue books."""
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            """SELECT BorrowedBook.Borrow_ID, Book.Title, BorrowedBook.Return_Date
               FROM BorrowedBook
               JOIN Book ON BorrowedBook.Book_ID = Book.Book_ID
               WHERE BorrowedBook.Reader_ID = ? 
               AND BorrowedBook.Return_Date < ?
               AND BorrowedBook.Returned = 0""",
            (self.user_id, today)
        )
        return self.cursor.fetchall()

    # Membership Operations
    def apply_membership(self, reason):
        self.cursor.execute("""
                    INSERT INTO Membership (Reader_ID, Application_Date, Reason, Status) 
                    VALUES (?, GETDATE(), ?, 'pending')
                """, (self.user_id, reason))
        self.conn.commit()
        return True
    def get_membership_status(self) -> str:
        """Get current user's membership status."""
        self.cursor.execute(
            "SELECT Membership_Status FROM Reader WHERE Reader_ID = ?",
            (self.user_id,)
        )
        return self.cursor.fetchone()[0]
    # Review Operations
    def get_book_rankings(self, timeframe):
        time_filter = {
            "daily": "DATEADD(DAY, -1, GETDATE())",
            "weekly": "DATEADD(DAY, -7, GETDATE())",
            "monthly": "DATEADD(DAY, -30, GETDATE())"
        }.get(timeframe, "DATEADD(DAY, -1, GETDATE())")  # Default to daily if invalid input

        query = f"""
            SELECT TOP 10 Book.Title, COUNT(BorrowedBook.Book_ID) AS Borrow_Count
            FROM BorrowedBook
            JOIN Book ON BorrowedBook.Book_ID = Book.Book_ID
            WHERE BorrowedBook.Borrow_Date >= {time_filter}
            GROUP BY Book.Title
            ORDER BY Borrow_Count DESC;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    def submit_review(self, book_id, review_text):
        if not review_text.strip():  # Prevent empty reviews
            return False
        self.cursor.execute(
            "INSERT INTO BookReview (Reader_ID, Book_ID, Review_Text) VALUES (?, ?, ?)",
            (self.user_id, book_id, review_text)
        )
        self.conn.commit()
        return True
    def get_review(self, book_id: int) -> tuple[list, list]:
        """Get all reviews for a book.
        
        Args:
            book_id: ID of the book to get reviews for
            
        Returns:
            tuple: (column_names, reviews)
            where reviews contains (review_id, username, review_text, review_date)
        """
        self.cursor.execute("""
            SELECT 
                br.Review_ID,
                c.User_Name,
                br.Review_Text,
                FORMAT(br.Review_Date, 'yyyy-MM-dd') as Review_Date
            FROM BookReview br
            JOIN Reader c ON c.Reader_ID = br.Reader_ID
            WHERE br.Book_ID = ?
            ORDER BY br.Review_Date DESC
        """, (book_id,))   
        data = self.cursor.fetchall()
        column_names = ['Review ID', 'Username', 'Review', 'Date']
        return column_names, data
    
    def delete_review(self, review_id: int) -> tuple[bool, str]:
        """Delete a review if owned by current user.
        
        Args:
            review_id: ID of review to delete
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            self.cursor.execute("""
                DELETE FROM BookReview 
                WHERE Review_ID = ? AND Reader_ID = ?
            """, (review_id, self.user_id))
            
            if self.cursor.rowcount > 0:
                self.conn.commit()
                return True, "Review deleted successfully"
            return False, "Review not found or not authorized to delete"
        except Exception as e:
            return False, f"Failed to delete review: {str(e)}"
    # Notifications management
    def get_unread_notification_count(self):
        self.connect()
        self.cursor.execute("SELECT COUNT(*) FROM Notification WHERE Reader_ID = ? AND Unread = 1", (self.user_id,))
        return self.cursor.fetchone()[0]

    def get_notifications(self):
        self.cursor.execute("""
        SELECT
            Notification_ID,
            Message,
            FORMAT(Timestamp, 'yyyy-MM-dd HH:mm') AS DateTime_Hour,
            CASE
                WHEN Unread = 1 THEN '!!!'
                ELSE CAST(Unread AS VARCHAR(10))
            END AS Unread_Status
        FROM
            Notification
        WHERE
            Reader_ID = ?
        ORDER BY
            Timestamp DESC;""",
                                    (self.user_id,))
        data= self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        return column_names, data
    

    def mark_notifications_as_read(self):
        self.cursor.execute("UPDATE Notification SET Unread = 0 WHERE Reader_ID = ?", (self.user_id,))
        self.conn.commit()
    def send_welcome_notifications(self) -> bool:
        """Send a welcome notification to newly registered user.
        
        Returns:
            bool: True if notification sent successfully, False otherwise
        """
        welcome_message = "Welcome to our library! 📚 You can borrow up to 10 books as a regular member. Need more benefits? Apply for Premium membership!"
        
        try:
            self.cursor.execute(
                "INSERT INTO Notification (Reader_ID, Message, Timestamp, Unread) VALUES (?, ?, GETDATE(), 1)",
                (self.user_id, welcome_message)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Failed to send welcome notification: {e}")
            return False
    # User Book rankings management
    def get_book_rankings(self, sort_by="borrow_count",timeframe="daily", order="DESC"):
        # Validate sorting options
        valid_sort_columns = {"borrow_count", "review_count"}
        valid_orders = {"ASC", "DESC"}

        if sort_by not in valid_sort_columns:
            sort_by = "borrow_count"  # Default sorting column

        if order not in valid_orders:
            order = "DESC"  # Default order

        time_filter = {
            "daily": "DATEADD(DAY, -1, GETDATE())",
            "weekly": "DATEADD(DAY, -7, GETDATE())",
            "monthly": "DATEADD(DAY, -30, GETDATE())"
        }.get(timeframe)  # Default to daily if invalid input

        query = f"""
            SELECT TOP 10 
                Book.Book_ID, 
                Book.Title, 
                COUNT(BorrowedBook.Book_ID) AS Borrow_Count, 
                COUNT(BookReview.Review_ID) AS review_count
            FROM Book
            LEFT JOIN BorrowedBook ON BorrowedBook.Book_ID = Book.Book_ID
            LEFT JOIN BookReview ON BookReview.Book_ID = Book.Book_ID
            WHERE BorrowedBook.Borrow_Date >= {time_filter}
            GROUP BY Book.Book_ID, Book.Title
            ORDER BY {sort_by} {order};
        """
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        return column_names, data

    # Change password management
    def check_password(self,input_password: str) -> bool:
        """Verify user credentials and set user_id if valid.
        Args:
            username: Username to check
            input_password: Password to verify
            
        Returns:
            bool: True if credentials valid, False otherwise
        """
        self.connect()
        query = """SELECT Password_Hash 
                FROM Reader 
                WHERE Reader_ID = ?"""
        self.cursor.execute(query, (self.user_id,))
        result = self.cursor.fetchone()
        
        if result is None:
            return False
            
        stored_hashed_password = result[0]
        if bcrypt.checkpw(
            input_password.encode('utf-8'), 
            stored_hashed_password.encode('utf-8')
        ):
            return True
        return False
    def update_user_password(self, new_password):
        """Updates the password for a specific user ID."""
        self.connect()  # Ensure connection to the database
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            self.cursor.execute(
                "UPDATE Reader SET Password_Hash = ? WHERE Reader_ID = ?",
                (hashed_password, self.user_id)
            )
            self.conn.commit()
            return True  # Indicate success
        except Exception as e:
            print(f"Error updating password: {e}")
            return False  # Indicate failure
    
