from database.library_db import LibraryDB
import pypyodbc
import bcrypt
from datetime import datetime

class AdminManager(LibraryDB):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.conn = None
        self.cursor = None
        self.admin_id = None

    def connect(self):
        if not self.conn:
            self.conn = pypyodbc.connect(self.connection_string)
            self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    # Authentication
    def verify_admin_login(self, input_username, input_password):
        self.connect()
        query ="SELECT Password_Hash FROM Admin WHERE User_Name = ?"
        self.cursor.execute(query, (input_username,))
        result = self.cursor.fetchone()
        if result:
            stored_hashed_password = result[0]
            if bcrypt.checkpw(input_password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                return True
        return None

    def logout(self):
        self.admin_id = None
        self.disconnect()

    # Book Management
    
    def get_book_title(self, book_id):
        self.cursor.execute("SELECT Title FROM Book WHERE Book_ID = ?", (book_id,))
        data = self.cursor.fetchone()
        return data[0] if data else None
        
    def get_books(self):
        self.cursor.execute("""SELECT Book_ID, Title, Author, Genre, Description FROM Book 
                                   JOIN Genre ON Book.Genre_ID = Genre.Genre_ID""")
        data = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]  # Fetch column names dynamically
        return column_names, data  # Return both column names and data
    def get_book_detail(self, book_id):
        self.cursor.execute("""
            SELECT Title, Genre_ID, Author, Description, Cover_Link, Book_Link 
            FROM Book WHERE Book_ID = ?
        """, (book_id,))
        
        data = self.cursor.fetchone()  # Fetch a single row instead of all
        
        return list(data) if data else None  # Convert to list if data exists
    def add_book(self, title, description, genre_id, author, cover, Book_Link):
        query = """INSERT INTO Book (Title, Description, Genre_ID, Author, Cover_Link, Book_Link)
                               VALUES (?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(query, (title, description, genre_id, author, cover, Book_Link))
        self.conn.commit()
        message = f"New book added: {title}"
        self.add_general_notification(message)
        return True
    
    def update_book(self, title, genre_id, author, description, cover, link_to_epub, book_id):
        old_title = self.get_book_title(book_id)
        
        query = """UPDATE Book 
                SET Title=?, Genre_ID=?, Author=?, Description=?, Cover_Link=?, Book_Link=? 
                WHERE Book_ID=?"""
        self.cursor.execute(query, (title, genre_id, author, description, cover, link_to_epub, book_id))
        self.conn.commit()
        row_affected = self.cursor.rowcount
        # Check if any row was actually updated
        new_title = self.get_book_title(book_id)
        if new_title != old_title:
            message = f"Book title changed from {old_title} to {new_title}"
        else:
            message = f"Book details updated for {old_title}"
        print(message)
        self.add_general_notification(message)
        
        return  row_affected>0  # Returns True if at least one row was updated, else False
    
    def delete_book(self, book_id):
        self.cursor.execute("DELETE FROM BorrowedBook WHERE Book_ID=?", (book_id,))
        self.cursor.execute(
            "DELETE FROM BookReview WHERE Book_ID = ?",
            (book_id,)
        )
        self.cursor.execute("DELETE FROM Book WHERE Book_ID = ?", (book_id,))
        self.conn.commit()
        self.add_general_notification(f"Book deleted: {book_id}")
    
    def get_genre(self):
        self.cursor.execute("SELECT Genre_ID, Genre FROM Genre ORDER BY Genre_ID ASC")
        return self.cursor.fetchall()
    
    def is_book_borrowed(self, book_id: str) -> bool:
        """Check if a book is currently borrowed.
        
        Args:
            book_id: ID of book to check
            
        Returns:
            bool: True if book is borrowed, False otherwise
        """
        self.cursor.execute("""
            SELECT COUNT(*)
            FROM BorrowedBook
            WHERE Book_ID = ? AND Returned = 0
        """, (book_id,))
        
        return self.cursor.fetchone()[0] > 0
    # User Management
    def get_users(self):
        """Get all users with their borrowing status.
        
        Returns:
            tuple: (column_names, data) containing user information
        """
        self.cursor.execute("""
            SELECT 
                c.Reader_ID,
                c.Name,
                c.Age,
                c.Membership_Status,
                COUNT(CASE WHEN bb.Returned = 0 THEN 1 END) as BorrowedBook
            FROM Reader c
            LEFT JOIN BorrowedBook bb ON c.Reader_ID = bb.Reader_ID
            GROUP BY c.Reader_ID, c.Name, c.Age, c.Membership_Status
        """)
        data = self.cursor.fetchall()
        column_names = ['ID', 'Name', 'Age', 'Membership Status', 'Books Borrowed']
        return column_names, data
    
    def get_specific_user(self, Reader_ID):
        self.cursor.execute("SELECT * FROM Reader WHERE Reader_ID = ?", (Reader_ID,))
        data = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        return column_names, data
    
    def delete_user(self, Reader_ID):
        self.cursor.execute("DELETE FROM BookReview WHERE Reader_ID = ?", (Reader_ID,))
        self.cursor.execute("DELETE FROM BorrowedBook WHERE Reader_ID = ?", (Reader_ID,))
        self.cursor.execute("DELETE FROM Membership WHERE Reader_ID = ?", (Reader_ID,))
        self.cursor.execute("DELETE FROM Reader WHERE Reader_ID = ?", (Reader_ID,))
        self.conn.commit()
        return True
    # Membership Management
    def get_membership_applications(self):
        self.cursor.execute("""SELECT m.Application_ID, m.Reader_ID, c.Name, m.Application_Date,
                            m.Reason, COUNT(CASE WHEN bb.Returned = 0 AND bb.Return_Date < GETDATE() THEN 1 ELSE NULL END) as Overdues
                            FROM Membership m
                            JOIN Reader c ON m.Reader_ID = c.Reader_ID
                            LEFT JOIN BorrowedBook bb ON c.Reader_ID = bb.Reader_ID
                            AND bb.Returned = 0
                            AND bb.Return_Date < GETDATE()
                            WHERE m.Status = 'pending'
                            GROUP BY m.Application_ID, m.Reader_ID, c.Name, m.Application_Date, m.Reason""")
        data = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        return column_names, data
    
    def approve_membership(self, application_id):
        self.cursor.execute("SELECT Reader_ID FROM Membership WHERE Application_ID = ?", (application_id,))
        result = self.cursor.fetchone()
        if result:
            user_id = result[0]
            self.cursor.execute("UPDATE Membership SET Status = 'approved' WHERE Application_ID = ?", (application_id,))
            self.cursor.execute("UPDATE Reader SET Membership_Status = 'Premium' WHERE Reader_ID = ?", (user_id,))
            self.conn.commit()
    
    def reject_membership(self, application_id):
        self.cursor.execute("UPDATE Membership SET Status = 'rejected' WHERE Application_ID = ?", (application_id,))
        self.conn.commit()
    
    # History Management
    def get_borrowing_history(self):
        """Get borrowing history with formatted dates and status."""
        self.cursor.execute("""
            SELECT 
                Reader.Name, 
                Book.Title, 
                CONVERT(date, BorrowedBook.Borrow_Date) as Borrow_Date,
                CONVERT(date, BorrowedBook.Return_Date) as Return_Date,
                CASE 
                    WHEN Returned = 1 THEN 'Returned'
                    WHEN Returned = 0 AND Return_Date >= GETDATE() THEN 'Not Returned'
                    WHEN Returned = 0 AND Return_Date < GETDATE() THEN 'Overdue'
                END as [Return Status]
            FROM BorrowedBook
            JOIN Reader ON BorrowedBook.Reader_ID = Reader.Reader_ID
            JOIN Book ON BorrowedBook.Book_ID = Book.Book_ID
        """)
        data = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        return column_names, data
    
    # Review Management
    def get_review(self):
        """Get all book reviews with review IDs.
        
        Returns:
            tuple: (column_names, data) where data contains 
            (review_id, username, review_text, book_title, review_date)
        """
        self.cursor.execute('''
            SELECT 
            br.Review_ID,
            c.Reader_ID,
            c.User_Name, 
            br.Review_Text, 
            b.Title, 
            FORMAT(br.Review_Date, 'yyyy-MM-dd') as Review_Date
        FROM BookReview br
        JOIN Reader c ON c.Reader_ID = br.Reader_ID
        JOIN Book b ON b.Book_ID = br.Book_ID
        ORDER BY br.Review_Date DESC
        ''')
        data = self.cursor.fetchall()
        column_names = ['Review ID', 'User ID', 'Username', 'Review', 'Book', 'Date']

        return column_names, data
    def delete_book_review(self, review_id: int) -> bool:
        """Delete a book review by its ID.
        
        Args:
            review_id: The unique identifier of the review to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        self.cursor.execute(
            "DELETE FROM BookReview WHERE Review_ID = ?",
            (review_id,)
        )
        rows_affected = self.cursor.rowcount
        self.conn.commit()
        return rows_affected > 0
    # Admin notifications function
    def get_user_id(self, user_name):
        self.cursor.execute("SELECT Reader_ID FROM Reader WHERE User_Name = ?", (user_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_book_id(self, book_title):
        self.cursor.execute("SELECT Book_ID FROM Book WHERE Title = ?", (book_title,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def add_general_notification(self, message):
        try:
            query = """
            INSERT INTO Notification (Reader_ID, Message, Timestamp, Unread)
            SELECT Reader_ID, ?, GETDATE(), 1
            FROM Reader;
            """
            self.cursor.execute(query, (str(message),))
            self.conn.commit()
            print("Notification successfully added.")  # Debugging message
        except Exception as e:
            print(f"Failed to add notification: {e}")

    def add_specific_notification(self, user_id: int, message: str) -> bool:
        """Add a notification for a user.
        
        Args:
            user_id: ID of user to notify
            message: Notification message
            
        Returns:
            bool: Success status
        """
        try:
            self.connect()
            self.cursor.execute(
                "INSERT INTO Notification (Reader_ID, Message, Timestamp, Unread) VALUES (?, ?, GETDATE(), 0)",
                (user_id, message)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Failed to add notification: {e}")
            return False