from PyQt6.QtWidgets import (
    QLineEdit,
    QAbstractItemView,
    QTableWidgetItem,
    QTableWidget,
    QHeaderView
)
from PyQt6.QtCore import Qt

class TableWidgetManager:
    """Manager class for handling multiple QTableWidget operations."""
    
    def __init__(self):
        """
        Initialize table manager.
        """
        self.table_settings = {
            'books': {'hidden_columns': [0]}, # Hide book ID
            'users': {'hidden_columns': [0]},  # Hide user ID
            'membership': {'hidden_columns': [0, 1]},  # Hide internal IDs
            'inventory': {'hidden_columns': [0]},  # Hide book ID
            'history': {'hidden_columns': [0]},  # Show all columns
            'reviews': {'hidden_columns': [0,1]},  # Hide review ID and user ID
            'ranking': {'hidden_columns': [0]},
            'notification': {'hidden_columns': [0]}
        }

    def load_data(self, table_widget: QTableWidget, data: list, 
                 header_labels: list = None, table_type: str = None):
        """Load data into specified table widget.
        
        Args:
            table_widget: Target QTableWidget
            data: List of data rows
            header_labels: Optional column headers
            table_type: Type of table for specific settings
        """
        self._configure_table(table_widget)
        self._populate_data(table_widget, data, header_labels)
        
        if table_type and table_type in self.table_settings:
            settings = self.table_settings[table_type]
            if settings['hidden_columns']:
                self._hide_columns(table_widget, settings['hidden_columns'])

    def _configure_table(self, table_widget: QTableWidget):
        """Apply default table configuration."""
        table_widget.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table_widget.verticalHeader().setVisible(False)

    def _populate_data(self, table_widget: QTableWidget, data, header_labels=None):
        table_widget.setRowCount(0)  # Clears table rows

        if not data:  # If data is empty, set headers (if provided) and return
            if header_labels:
                table_widget.setColumnCount(len(header_labels))
                table_widget.setHorizontalHeaderLabels(header_labels)
            else:
                table_widget.setColumnCount(0)
            return

        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(data[0]))

        if header_labels:
            table_widget.setHorizontalHeaderLabels(header_labels)

        # Initialize column widths with header widths
        fm = table_widget.fontMetrics()
        column_widths = [0] * len(data[0])
        
        if header_labels:
            for col, header in enumerate(header_labels):
                header_width = fm.horizontalAdvance(str(header))
                column_widths[col] = max(column_widths[col], header_width)

        # Calculate maximum content width for each column
        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                table_widget.setItem(row_index, col_index, item)
                
                # Calculate content width using font metrics
                content_width = fm.horizontalAdvance(str(cell_data))
                column_widths[col_index] = max(column_widths[col_index], content_width)

        # Apply calculated widths with padding
        for col, width in enumerate(column_widths):
            padding = 40  # Adjust padding as needed
            final_width = min(width + padding, 400)  # Maximum width of 400px
            
            # Special handling for date columns
            if header_labels and any(date_keyword in header_labels[col].lower() for date_keyword in ['date', 'time']):
                final_width = max(final_width, 120)  # Minimum width for date columns
                
            table_widget.setColumnWidth(col, final_width)

    def _hide_columns(self, table_widget: QTableWidget, hidden_columns: list[int]):
        """Hide specified columns in a QTableWidget.
        
        Args:
            table_widget: The QTableWidget to modify
            hidden_columns: List of column indices to hide
        
        Example:
            set_hidden_columns(table, [0, 1])  # Hides first two columns
        """
        for col_index in hidden_columns:
            table_widget.setColumnHidden(col_index, True)
    def swap_columns(self, headers, data):
        """Swap the positions of 'Borrow_Count' and 'Review_Count' in headers and data."""
        if not headers or "borrow_count" not in headers or "review_count" not in headers:
            return headers, data  # Return unchanged if columns are missing

        # Get the indices of the columns to swap
        borrow_idx = headers.index("borrow_count")
        review_idx = headers.index("review_count")

        # Swap headers
        headers[borrow_idx], headers[review_idx] = headers[review_idx], headers[borrow_idx]

        # Swap corresponding values in each row
        swapped_data = []
        for row in data:
            row = list(row)  # Convert tuple to list for modification
            row[borrow_idx], row[review_idx] = row[review_idx], row[borrow_idx]
            swapped_data.append(tuple(row))  # Convert back to tuple

        return headers, swapped_data
    def rearrange_columns(self, table_widget: QTableWidget, header_labels):
        """Visually moves the 'review_count' column before 'rorrow_count'."""
        if not header_labels or "borrow_count" not in header_labels or "review_count" not in header_labels:
            return  # Skip if headers are missing

        borrow_idx = header_labels.index("borrow_count")
        review_idx = header_labels.index("review_count")

        if review_idx > borrow_idx:
            table_widget.horizontalHeader().moveSection(review_idx, borrow_idx)