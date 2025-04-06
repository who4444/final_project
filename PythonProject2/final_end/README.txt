# Readiverse Project

## Overview

Readiverse is a comprehensive library management system that allows users to manage books, read reviews, and interact with a user-friendly interface. The project is built using Python and PyQt6 for the GUI, with SQL Server for database management.

## Project Structure

```
main.py
controller.py
note.txt
README.txt
requirements.txt

database/
    admin.py
    config.py
    library_db.py
    user.py
    __pycache__/
resources/
    config.py
    resources_rc.py
    resources.qrc
    __pycache__/
    books/
    icons/
    images/
ui/
    design.py
    design.ui
    window.py
    __pycache__/
    dialogs/
    message_box/
    readers/
utils/
    checker.py
    helper_functions.py
    __pycache__/
    table/
```

## Key Components

### `database/`

* **`admin.py`**: Handles database operations specific to administrative tasks, such as user management and system settings.
* **`config.py`**: Configuration settings for the database.
* **`library_db.py`**: Contains core database functionalities, including book storage, retrieval, and modification.
* **`user.py`**: Manages user-related database operations, such as reading history and user profiles.

### `ui/`

* **`design.py`**: Contains the main design logic for the UI.
* **`design.ui`**: XML file defining the UI layout.
* **`window.py`**: Manages the main application window.
* **`dialogs/`**: Contains various dialog windows used in the application.
* **`message_box/`**: Custom message boxes for user interactions.
* **`readers/`**: Implements readers for different book formats.

### `utils/`

* **`checker.py`**: Contains functions for input validation and data integrity checks.
* **`helper_functions.py`**: Provides various utility functions used throughout the application.

### `resources/`

* **`config.py`**: Configuration settings for resources.
* **`resources_rc.py`**: Compiled resource file.
* **`resources.qrc`**: Resource file containing references to images, icons, and other assets.
* **`books/`**: Stores book files in formats like EPUB or PDF.
* **`icons/`**: Stores icon files used in the application.
* **`images/`**: Stores image files used in the application's UI.

## Installation and Setup

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd final_project
    ```

2. **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

    * **Windows:**

        ```bash
        venv\Scripts\activate
        ```

    * **macOS and Linux:**

        ```bash
        source venv/bin/activate
        ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**

    ```bash
    python main.py
    ```

## Dependencies

The project relies on the following Python packages (specified in `requirements.txt`):

* python>=3.8
* pypyodbc>=1.3.3
* sql-server>=1.0.0
* PyQt6>=6.2.0
* PyQt6-WebEngine>=6.2.0
* beautifulsoup4>=4.10.0
* better-profanity>=0.1.2
* bcrypt>=3.2.0
* matplotlib>=3.4.3
* httpx>=0.20.0
* zipfile>=0.0.0
* PySide6>=6.2.0

## Usage

1. Launch the application using `python main.py`.
2. Use the main window to navigate and interact with the library.
3. Utilize the `Add Book` dialog to add new books to the library.
4. Use the book reader to read books.
5. Administrative users can manage users and system settings through the admin interface.

## Future Improvements

* Improve search functionality.
* Improve UI/UX.
* Implement a more robust database solution.
* Implement testing.