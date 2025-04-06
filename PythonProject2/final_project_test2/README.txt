## Key Components

### `database/`

* **`__init__.py`**: Initializes the `database` package.
* **`admin.py`**: Handles database operations specific to administrative tasks, such as user management and system settings.
* **`library_db.py`**: Contains core database functionalities, including book storage, retrieval, and modification.
* **`user.py`**: Manages user-related database operations, such as reading history and user profiles.

### `ui/`

* **`__init__.py`**: Initializes the `ui` package.
* **`main_window.py`**: Defines the main application window, orchestrating the overall user experience.
* **`main_lib_ui.py`**: Implements the library-specific UI, including book displays and interaction elements.
* **`dialogs/`**:
    * **`__init__.py`**: Initializes the `dialogs` subpackage.
    * **`add_book_dialog.py`**: Provides a dialog for adding new books to the library.
    * **`read_book_dialog.py`**: Manages the dialog for reading books.
    * **`calendar_dialog.py`**: Implements a calendar dialog for date selection and scheduling.
* **`readers/`**:
    * **`__init__.py`**: Initializes the `readers` subpackage.
    * **`epub_reader.py`**: Implements a reader for EPUB book files.

### `utils/`

* **`__init__.py`**: Initializes the `utils` package.
* **`checker.py`**: Contains functions for input validation and data integrity checks.
* **`helper_functions.py`**: Provides various utility functions used throughout the application.

### `resources/`

* **`images/`**: Stores image files used in the application's UI.
* **`books/`**: Stores book files in formats like EPUB or PDF.

### Project Files

* **`requirements.txt`**: Lists the project's Python dependencies.
* **`README.md`**: Provides general information and instructions for the project.
* **`main.py`**: The entry point for the application, initializing and launching the main window.

## Installation and Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd final_project
    ```

2.  **Create a virtual environment (recommended):**

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

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**

    ```bash
    python main.py
    ```

## Dependencies

The project relies on the following Python packages (specified in `requirements.txt`):

* (List the dependencies from your requirements.txt file here)

## Usage

1.  Launch the application using `python main.py`.
2.  Use the main window to navigate and interact with the library.
3.  Utilize the `Add Book` dialog to add new books to the library.
4.  Use the book reader to read books.
5.  Administrative users can manage users and system settings through the admin interface.

## Future Improvements

* Implement PDF reader.
* Add search functionality.
* Improve UI/UX.
* Add user authentication.
* Implement a more robust database solution.
* Implement testing.