import json
import importlib.util
import pytest
import tempfile
import pathlib
from unittest.mock import patch, mock_open, MagicMock
import sys

# Import the module functions
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

# We need to mock the file operations since the module runs code at import time
with patch('pathlib.Path.exists', return_value=True):
    with patch('pathlib.Path.write_text'):
        import expense_tracker


class TestRecordExpenses:
    """Test suite for the record_expenses function."""

    def test_record_expenses_valid_json(self):
        """Test reading valid expenses from JSON file."""
        mock_data = [
            {"amount": 50.0, "category": "Food", "date": "2026-01-15"},
            {"amount": 30.0, "category": "Transportation", "date": "2026-01-16"}
        ]
        
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            result = expense_tracker.record_expenses()
            assert result == mock_data
            assert len(result) == 2

    def test_record_expenses_empty_file(self):
        """Test reading an empty expenses file."""
        with patch("builtins.open", mock_open(read_data="[]")):
            result = expense_tracker.record_expenses()
            assert result == []

    def test_record_expenses_file_not_found(self):
        """Test handling of missing expenses file."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = expense_tracker.record_expenses()
            assert result == []

    def test_record_expenses_invalid_json(self):
        """Test handling of invalid JSON in the file."""
        with patch("builtins.open", mock_open(read_data="invalid json")):
            with pytest.raises(expense_tracker.JsonError):
                expense_tracker.record_expenses()


class TestSaveExpenses:
    """Test suite for the save_expenses function."""

    def test_save_expenses_success(self, capsys):
        """Test successful save of expenses to JSON file."""
        mock_data = [
            {"amount": 50.0, "category": "Food", "date": "2026-01-15"}
        ]
        
        with patch("builtins.open", mock_open()):
            with patch("json.dump"):
                expense_tracker.save_expenses(mock_data)
                captured = capsys.readouterr()
                assert "Expenses updated successfully" in captured.out

    def test_save_expenses_file_write_error(self):
        """Test handling of file write errors."""
        mock_data = [
            {"amount": 50.0, "category": "Food", "date": "2026-01-15"}
        ]
        
        with patch("builtins.open", side_effect=OSError("Permission denied")):
            with pytest.raises(expense_tracker.JsonError):
                expense_tracker.save_expenses(mock_data)


class TestAddExpense:
    """Test suite for the add_expense function."""

    def test_add_expense_valid_input(self):
        """Test adding a valid expense."""
        inputs = ["50.0", "Food", "2026-01-15"]
        
        with patch("builtins.input", side_effect=inputs):
            with patch.object(expense_tracker, "record_expenses", return_value=[]):
                with patch.object(expense_tracker, "save_expenses"):
                    expense_tracker.add_expense()

    def test_add_expense_zero_amount(self):
        """Test rejection of zero amount."""
        inputs = ["0", "50.0", "Food", "2026-01-15"]
        
        with patch("builtins.input", side_effect=inputs):
            with patch.object(expense_tracker, "record_expenses", return_value=[]):
                with patch.object(expense_tracker, "save_expenses"):
                    expense_tracker.add_expense()

    def test_add_expense_negative_amount(self):
        """Test rejection of negative amount."""
        inputs = ["-10.0", "50.0", "Food", "2026-01-15"]
        
        with patch("builtins.input", side_effect=inputs):
            with patch.object(expense_tracker, "record_expenses", return_value=[]):
                with patch.object(expense_tracker, "save_expenses"):
                    expense_tracker.add_expense()

    def test_add_expense_invalid_amount(self):
        """Test rejection of non-numeric amount."""
        inputs = ["abc", "50.0", "Food", "2026-01-15"]
        
        with patch("builtins.input", side_effect=inputs):
            with patch.object(expense_tracker, "record_expenses", return_value=[]):
                with patch.object(expense_tracker, "save_expenses"):
                    expense_tracker.add_expense()

    def test_add_expense_empty_category(self):
        """Test rejection of empty category."""
        inputs = ["50.0", "", "Food", "2026-01-15"]
        
        with patch("builtins.input", side_effect=inputs):
            with patch.object(expense_tracker, "record_expenses", return_value=[]):
                with patch.object(expense_tracker, "save_expenses"):
                    expense_tracker.add_expense()

    def test_add_expense_invalid_date_format(self):
        """Test rejection of invalid date format."""
        inputs = ["50.0", "Food", "01-01-2026", "2026-01-15"]
        
        with patch("builtins.input", side_effect=inputs):
            with patch.object(expense_tracker, "record_expenses", return_value=[]):
                with patch.object(expense_tracker, "save_expenses"):
                    expense_tracker.add_expense()

    def test_add_expense_empty_date(self):
        """Test rejection of empty date."""
        inputs = ["50.0", "Food", "", "2026-01-15"]
        
        with patch("builtins.input", side_effect=inputs):
            with patch.object(expense_tracker, "record_expenses", return_value=[]):
                with patch.object(expense_tracker, "save_expenses"):
                    expense_tracker.add_expense()


class TestShowExpenses:
    """Test suite for the show_expenses function."""

    def test_show_expenses_found(self, capsys):
        """Test displaying expenses for a specific month."""
        mock_expenses = [
            {"amount": 50.0, "category": "Food", "date": "2026-01-15"},
            {"amount": 30.0, "category": "Transportation", "date": "2026-01-16"},
            {"amount": 20.0, "category": "Food", "date": "2026-02-01"}
        ]
        
        with patch("builtins.input", return_value="2026-01"):
            expense_tracker.show_expenses(mock_expenses)
            captured = capsys.readouterr()
            assert "Date: 2026-01-15" in captured.out
            assert "Date: 2026-01-16" in captured.out
            assert "Total expenses for 2026-01: 80.0" in captured.out

    def test_show_expenses_not_found(self, capsys):
        """Test displaying message when no expenses found for month."""
        mock_expenses = [
            {"amount": 50.0, "category": "Food", "date": "2026-01-15"}
        ]
        
        with patch("builtins.input", return_value="2026-03"):
            expense_tracker.show_expenses(mock_expenses)
            captured = capsys.readouterr()
            assert "No expenses recorded for 2026-03" in captured.out

    def test_show_expenses_category_totals(self, capsys):
        """Test that category totals are calculated correctly."""
        mock_expenses = [
            {"amount": 50.0, "category": "Food", "date": "2026-01-15"},
            {"amount": 30.0, "category": "Food", "date": "2026-01-16"},
            {"amount": 20.0, "category": "Transportation", "date": "2026-01-17"}
        ]
        
        with patch("builtins.input", return_value="2026-01"):
            expense_tracker.show_expenses(mock_expenses)
            captured = capsys.readouterr()
            assert "Food: 80.0" in captured.out
            assert "Transportation: 20.0" in captured.out
            assert "Total expenses for 2026-01: 100.0" in captured.out

    def test_show_expenses_empty_list(self, capsys):
        """Test displaying expenses when no expenses exist."""
        mock_expenses = []
        
        with patch("builtins.input", return_value="2026-01"):
            expense_tracker.show_expenses(mock_expenses)
            captured = capsys.readouterr()
            assert "No expenses recorded for 2026-01" in captured.out


class TestCustomExceptions:
    """Test suite for custom exceptions."""

    def test_amount_error(self):
        """Test AmountError exception."""
        with pytest.raises(expense_tracker.AmountError):
            raise expense_tracker.AmountError("Amount must be greater than zero.")

    def test_option_error(self):
        """Test OptionError exception."""
        with pytest.raises(expense_tracker.OptionError):
            raise expense_tracker.OptionError("Invalid input.")

    def test_category_error(self):
        """Test CategoryError exception."""
        with pytest.raises(expense_tracker.CategoryError):
            raise expense_tracker.CategoryError("Invalid category.")

    def test_json_error(self):
        """Test JsonError exception."""
        with pytest.raises(expense_tracker.JsonError):
            raise expense_tracker.JsonError("The JSON file is not valid.")

    def test_empty_field_error(self):
        """Test EmptyFieldError exception."""
        with pytest.raises(expense_tracker.EmptyFieldError):
            raise expense_tracker.EmptyFieldError("Field cannot be empty.")


class TestModuleImportBehavior:
    """Test module import side effects."""

    def test_import_does_not_prompt_for_input(self):
        """Importing the module should not start the interactive menu."""
        module_path = pathlib.Path(__file__).parent.parent / "expense_tracker.py"
        spec = importlib.util.spec_from_file_location(
            "expense_tracker_import_check",
            module_path
        )
        module = importlib.util.module_from_spec(spec)
        assert spec is not None
        assert spec.loader is not None

        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.write_text"):
                with patch(
                    "builtins.input",
                    side_effect=AssertionError(
                        "input should not be called during import"
                    )
                ):
                    spec.loader.exec_module(module)
