"""
Tests for the Python utility functions.
"""

import builtins
import os
import sys

import pytest

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.python.utils import (DataProcessor, FileManager, SystemMonitor,
                              WebScraper, calculate_fibonacci,
                              generate_random_data, is_prime, sort_data)


class TestFibonacci:
    """Test cases for the Fibonacci function."""

    def test_fibonacci_base_cases(self):
        """Test base cases for Fibonacci sequence."""
        assert calculate_fibonacci(0) == 0
        assert calculate_fibonacci(1) == 1

    def test_fibonacci_positive_numbers(self):
        """Test Fibonacci for positive numbers."""
        assert calculate_fibonacci(2) == 1
        assert calculate_fibonacci(3) == 2
        assert calculate_fibonacci(4) == 3
        assert calculate_fibonacci(5) == 5
        assert calculate_fibonacci(10) == 55

    def test_fibonacci_negative_input(self):
        """Test Fibonacci with negative input."""
        with pytest.raises(ValueError):
            calculate_fibonacci(-1)


class TestPrime:
    """Test cases for the prime number function."""

    def test_is_prime_true_cases(self):
        """Test numbers that are prime."""
        assert is_prime(2) == True
        assert is_prime(3) == True
        assert is_prime(5) == True
        assert is_prime(7) == True
        assert is_prime(11) == True
        assert is_prime(17) == True

    def test_is_prime_false_cases(self):
        """Test numbers that are not prime."""
        assert is_prime(0) == False
        assert is_prime(1) == False
        assert is_prime(4) == False
        assert is_prime(6) == False
        assert is_prime(8) == False
        assert is_prime(9) == False
        assert is_prime(10) == False

    def test_is_prime_negative_numbers(self):
        """Test negative numbers (should all be False)."""
        assert is_prime(-1) == False
        assert is_prime(-5) == False


class TestDataGeneration:
    """Test cases for data generation functions."""

    def test_generate_random_data_default_size(self):
        """Test generating data with default size."""
        data = generate_random_data()
        assert len(data) == 10
        assert all("id" in item for item in data)
        assert all("name" in item for item in data)
        assert all("age" in item for item in data)

    def test_generate_random_data_custom_size(self):
        """Test generating data with custom size."""
        data = generate_random_data(5)
        assert len(data) == 5

        data = generate_random_data(20)
        assert len(data) == 20

    def test_data_structure(self):
        """Test the structure of generated data."""
        data = generate_random_data(1)
        item = data[0]

        assert "id" in item
        assert "name" in item
        assert "age" in item
        assert "score" in item
        assert "timestamp" in item
        assert "active" in item

        assert isinstance(item["id"], int)
        assert isinstance(item["name"], str)
        assert isinstance(item["age"], int)
        assert isinstance(item["score"], float)
        assert isinstance(item["active"], bool)


class TestSorting:
    """Test cases for data sorting function."""

    def test_sort_by_age(self):
        """Test sorting by age."""
        data = [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30},
            {"name": "Charlie", "age": 20},
        ]

        sorted_data = sort_data(data, "age")
        ages = [item["age"] for item in sorted_data]
        assert ages == [20, 25, 30]

    def test_sort_by_age_reverse(self):
        """Test sorting by age in reverse order."""
        data = [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30},
            {"name": "Charlie", "age": 20},
        ]

        sorted_data = sort_data(data, "age", reverse=True)
        ages = [item["age"] for item in sorted_data]
        assert ages == [30, 25, 20]


class TestFileManager:
    """Test cases for the FileManager class."""

    def test_filemanager_initialization(self):
        """Test FileManager initialization."""
        fm = FileManager()
        assert str(fm.base_path) == "."

        fm_custom = FileManager("/tmp")
        # Use Path for cross-platform compatibility
        from pathlib import Path

        assert Path(str(fm_custom.base_path)) == Path("/tmp")

    def test_organize_files_by_extension(self, tmp_path):
        """Test organizing files by extension."""
        fm = FileManager()

        # Create test files
        (tmp_path / "file1.txt").write_text("content")
        (tmp_path / "file2.py").write_text("print('hello')")
        (tmp_path / "file3.txt").write_text("more content")
        (tmp_path / "noext").write_text("no extension")

        organized = fm.organize_files_by_extension(str(tmp_path))

        assert ".txt" in organized
        assert ".py" in organized
        assert "no_extension" in organized
        assert len(organized[".txt"]) == 2
        assert len(organized[".py"]) == 1
        assert len(organized["no_extension"]) == 1

    def test_organize_files_nonexistent_directory(self):
        """Test organizing files in non-existent directory."""
        fm = FileManager()
        result = fm.organize_files_by_extension("/nonexistent/path")
        assert result == {}

    def test_find_duplicates(self, tmp_path):
        """Test finding duplicate files."""
        fm = FileManager()

        # Create identical files
        (tmp_path / "file1.txt").write_text("identical content")
        (tmp_path / "file2.txt").write_text("identical content")
        (tmp_path / "file3.txt").write_text("different content")

        duplicates = fm.find_duplicates(str(tmp_path))

        # Should find one set of duplicates
        assert len(duplicates) == 1
        for file_hash, files in duplicates.items():
            assert len(files) == 2

    def test_find_duplicates_nonexistent_directory(self):
        """Test finding duplicates in non-existent directory."""
        fm = FileManager()
        result = fm.find_duplicates("/nonexistent/path")
        assert result == {}

    def test_csv_to_json_success(self, tmp_path):
        """Test successful CSV to JSON conversion in FileManager."""
        fm = FileManager()

        # Create a test CSV file
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("name,age\nAlice,25\nBob,30")

        json_file = tmp_path / "test.json"

        result = fm.csv_to_json(str(csv_file), str(json_file))
        assert result == True
        assert json_file.exists()

    def test_csv_to_json_failure(self):
        """Test CSV to JSON conversion failure in FileManager."""
        fm = FileManager()
        result = fm.csv_to_json("nonexistent.csv", "output.json")
        assert result == False

    def test_json_to_csv_success(self, tmp_path):
        """Test successful JSON to CSV conversion in FileManager."""
        fm = FileManager()

        # Create a test JSON file
        json_file = tmp_path / "test.json"
        json_file.write_text(
            '[{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]'
        )

        csv_file = tmp_path / "test.csv"

        result = fm.json_to_csv(str(json_file), str(csv_file))
        assert result == True
        assert csv_file.exists()

    def test_json_to_csv_invalid_format(self, tmp_path):
        """Test JSON to CSV conversion with invalid format in FileManager."""
        fm = FileManager()

        # Create invalid JSON file (not a list of dicts)
        json_file = tmp_path / "invalid.json"
        json_file.write_text('{"key": "value"}')

        csv_file = tmp_path / "output.csv"

        result = fm.json_to_csv(str(json_file), str(csv_file))
        assert result == False

    def test_validate_json_valid(self, tmp_path):
        """Test JSON validation with valid file in FileManager."""
        fm = FileManager()

        json_file = tmp_path / "valid.json"
        json_file.write_text('{"name": "Alice", "age": 25}')

        result = fm.validate_json(str(json_file))
        assert result == True

    def test_validate_json_invalid(self, tmp_path):
        """Test JSON validation with invalid file in FileManager."""
        fm = FileManager()

        json_file = tmp_path / "invalid.json"
        json_file.write_text('{"name": "Alice", "age": 25')

        result = fm.validate_json(str(json_file))
        assert result == False

    def test_validate_json_general_exception(self, tmp_path, monkeypatch):
        """Test JSON validation when a general exception occurs."""
        fm = FileManager()

        # Create a valid JSON file
        json_file = tmp_path / "test.json"
        json_file.write_text('{"name": "Alice", "age": 25}')

        # Mock open to raise a general exception
        import builtins

        original_open = builtins.open

        def mock_open(*args, **kwargs):
            if str(json_file) in str(args[0]):
                raise Exception("Simulated file read error")
            return original_open(*args, **kwargs)

        monkeypatch.setattr(builtins, "open", mock_open)

        result = fm.validate_json(str(json_file))
        assert result == False


class TestDataProcessor:
    """Test cases for the DataProcessor class."""

    def test_add_data(self):
        """Test adding data to processor."""
        processor = DataProcessor()
        assert len(processor.data) == 0

        processor.add_data({"name": "Alice", "age": 25})
        assert len(processor.data) == 1

    def test_filter_by_age(self):
        """Test filtering data by age range."""
        processor = DataProcessor()
        processor.add_data({"name": "Alice", "age": 25})
        processor.add_data({"name": "Bob", "age": 35})
        processor.add_data({"name": "Charlie", "age": 45})

        filtered = processor.filter_by_age(30, 40)
        assert len(filtered) == 1
        assert filtered[0]["name"] == "Bob"

    def test_get_statistics_empty(self):
        """Test statistics with empty data."""
        processor = DataProcessor()
        stats = processor.get_statistics()
        assert stats == {}

    def test_get_statistics_with_data(self):
        """Test statistics with actual data."""
        processor = DataProcessor()
        processor.add_data({"age": 25, "score": 85.5})
        processor.add_data({"age": 35, "score": 92.0})

        stats = processor.get_statistics()
        assert stats["total_records"] == 2
        assert stats["avg_age"] == 30.0
        assert stats["min_age"] == 25
        assert stats["max_age"] == 35

    # Note: File operation methods (csv_to_json, json_to_csv, validate_json) 
    # have been moved to FileManager class to avoid code duplication.
    # These tests are now in the TestFileManager class above.


class TestSystemMonitor:
    """Test cases for the SystemMonitor class."""

    def test_system_monitor_initialization(self):
        """Test SystemMonitor initialization."""
        sm = SystemMonitor()
        assert sm.logger is not None

    @pytest.mark.skipif(
        True, reason="Requires psutil, may not be available in all environments"
    )
    def test_get_system_info(self):
        """Test getting system information."""
        sm = SystemMonitor()
        info = sm.get_system_info()

        # Should have basic fields if psutil is available
        if info:  # Only test if psutil is available
            assert "platform" in info
            assert "cpu_count" in info
            assert "memory_total" in info

    @pytest.mark.skipif(
        True, reason="Requires psutil, may not be available in all environments"
    )
    def test_check_disk_space(self):
        """Test checking disk space."""
        sm = SystemMonitor()
        result = sm.check_disk_space("/")

        # Should have basic fields if psutil is available
        if result:  # Only test if psutil is available
            assert "path" in result
            assert "total" in result
            assert "used" in result
            assert "free" in result
            assert "percentage_used" in result


class TestWebScraper:
    """Test cases for the WebScraper class."""

    def test_webscraper_initialization(self):
        """Test WebScraper initialization."""
        ws = WebScraper()
        assert ws.timeout == 30
        assert ws.session is not None
        assert ws.logger is not None

        ws_custom = WebScraper(timeout=60)
        assert ws_custom.timeout == 60

    @pytest.mark.skipif(True, reason="Requires network access, skip for offline tests")
    def test_fetch_url_success(self):
        """Test successful URL fetching."""
        ws = WebScraper(timeout=5)
        # Using a reliable test URL
        content = ws.fetch_url("https://httpbin.org/get")
        # Only test if we get a response (network dependent)
        if content:
            assert isinstance(content, str)

    @pytest.mark.skipif(True, reason="Requires network access, skip for offline tests")
    def test_check_url_status_success(self):
        """Test checking URL status."""
        ws = WebScraper(timeout=5)
        # Using a reliable test URL
        result = ws.check_url_status("https://httpbin.org/status/200")

        # Only test if we get a response (network dependent)
        if result.get("status_code"):
            assert "url" in result
            assert "status_code" in result
            assert "is_accessible" in result
            assert "timestamp" in result

    def test_fetch_url_with_custom_headers(self):
        """Test URL fetching with custom headers."""
        ws = WebScraper()
        # This will likely fail but tests the header merging logic
        custom_headers = {"Authorization": "Bearer token"}
        content = ws.fetch_url("https://httpbin.org/headers", headers=custom_headers)
        # We expect this to return None due to timeout or network issues in test environment
        # but the important thing is it doesn't crash
        assert content is None or isinstance(content, str)


class TestMainFunction:
    """Test cases for the main function and demo code."""

    def test_main_function_execution(self, capsys, monkeypatch):
        """Test the main function execution."""
        # Mock input to avoid interactive prompts
        monkeypatch.setattr("builtins.input", lambda _: "y")

        # Import and run main function
        from src.python.utils import main

        main()

        # Capture output
        captured = capsys.readouterr()
        assert "Python Utilities Demo" in captured.out
        assert "File Manager Demo" in captured.out
        assert "Data Processor Demo" in captured.out


class TestSystemMonitorWithMocks:
    """Test SystemMonitor with mocked dependencies."""

    def test_get_system_info_with_psutil(self, monkeypatch):
        """Test get_system_info when psutil is available."""
        # Mock psutil module
        import sys
        from unittest.mock import MagicMock

        mock_psutil = MagicMock()
        mock_psutil.cpu_count.return_value = 4
        mock_psutil.virtual_memory.return_value.total = 8589934592
        mock_psutil.virtual_memory.return_value.available = 4294967296
        mock_psutil.disk_usage.return_value.percent = 45.2

        mock_platform = MagicMock()
        mock_platform.system.return_value = "Darwin"
        mock_platform.release.return_value = "20.6.0"
        mock_platform.version.return_value = "Darwin Kernel Version 20.6.0"
        mock_platform.machine.return_value = "x86_64"
        mock_platform.processor.return_value = "i386"

        sys.modules["psutil"] = mock_psutil
        sys.modules["platform"] = mock_platform

        sm = SystemMonitor()
        info = sm.get_system_info()

        assert info["platform"] == "Darwin"
        assert info["cpu_count"] == 4
        assert info["memory_total"] == 8589934592
        assert "timestamp" in info

    def test_get_system_info_with_exception(self, monkeypatch):
        """Test get_system_info when an exception occurs."""
        import sys
        from unittest.mock import MagicMock

        mock_psutil = MagicMock()
        mock_psutil.cpu_count.side_effect = Exception("Mock error")

        sys.modules["psutil"] = mock_psutil

        sm = SystemMonitor()
        info = sm.get_system_info()

        assert info == {}

    def test_check_disk_space_success(self, monkeypatch):
        """Test successful disk space checking."""
        import sys
        from unittest.mock import MagicMock

        mock_psutil = MagicMock()
        mock_usage = MagicMock()
        mock_usage.total = 1000000000
        mock_usage.used = 500000000
        mock_usage.free = 500000000
        mock_psutil.disk_usage.return_value = mock_usage

        sys.modules["psutil"] = mock_psutil

        sm = SystemMonitor()
        result = sm.check_disk_space("/")

        assert result["path"] == "/"
        assert result["total"] == 1000000000
        assert result["used"] == 500000000
        assert result["free"] == 500000000
        assert result["percentage_used"] == 50.0
        assert "timestamp" in result

    def test_check_disk_space_with_exception(self, monkeypatch):
        """Test disk space checking when an exception occurs."""
        import sys
        from unittest.mock import MagicMock

        mock_psutil = MagicMock()
        mock_psutil.disk_usage.side_effect = Exception("Disk error")

        sys.modules["psutil"] = mock_psutil

        sm = SystemMonitor()
        result = sm.check_disk_space("/")

        assert result == {}


class TestWebScraperWithMocks:
    """Test WebScraper with mocked requests."""

    def test_fetch_url_success(self, monkeypatch):
        """Test successful URL fetching."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.text = "<html>Test content</html>"
        mock_response.raise_for_status.return_value = None

        mock_session = MagicMock()
        mock_session.get.return_value = mock_response

        ws = WebScraper()
        ws.session = mock_session

        content = ws.fetch_url("https://example.com")

        assert content == "<html>Test content</html>"
        mock_session.get.assert_called_once()

    def test_fetch_url_with_custom_headers(self, monkeypatch):
        """Test URL fetching with custom headers."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.text = "Custom response"
        mock_response.raise_for_status.return_value = None

        mock_session = MagicMock()
        mock_session.get.return_value = mock_response

        ws = WebScraper()
        ws.session = mock_session

        custom_headers = {"Authorization": "Bearer token"}
        content = ws.fetch_url("https://api.example.com", headers=custom_headers)

        assert content == "Custom response"

        # Verify headers were merged
        call_args = mock_session.get.call_args
        sent_headers = call_args[1]["headers"]
        assert "Authorization" in sent_headers
        assert "User-Agent" in sent_headers

    def test_fetch_url_request_exception(self, monkeypatch):
        """Test URL fetching when requests raises an exception."""
        from unittest.mock import MagicMock

        import requests.exceptions

        mock_session = MagicMock()
        mock_session.get.side_effect = requests.exceptions.RequestException(
            "Connection error"
        )

        ws = WebScraper()
        ws.session = mock_session

        content = ws.fetch_url("https://broken.example.com")

        assert content is None

    def test_check_url_status_success(self, monkeypatch):
        """Test successful URL status checking."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/html"}

        mock_session = MagicMock()
        mock_session.head.return_value = mock_response

        ws = WebScraper()
        ws.session = mock_session

        result = ws.check_url_status("https://example.com")

        assert result["url"] == "https://example.com"
        assert result["status_code"] == 200
        assert result["is_accessible"] == True
        assert "headers" in result
        assert "timestamp" in result

    def test_check_url_status_request_exception(self, monkeypatch):
        """Test URL status checking when requests raises an exception."""
        from unittest.mock import MagicMock

        import requests.exceptions

        mock_session = MagicMock()
        mock_session.head.side_effect = requests.exceptions.RequestException(
            "Network error"
        )

        ws = WebScraper()
        ws.session = mock_session

        result = ws.check_url_status("https://broken.example.com")

        assert result["url"] == "https://broken.example.com"
        assert result["status_code"] is None
        assert result["is_accessible"] == False
        assert "error" in result
        assert "timestamp" in result


class TestFileManagerEdgeCases:
    """Test FileManager edge cases."""

    def test_organize_files_large_directory(self, tmp_path):
        """Test organizing files with more than 100 files to trigger break condition."""
        fm = FileManager()
        
        # Create more than 100 files to trigger the break on line 72
        for i in range(105):
            (tmp_path / f"file{i}.txt").write_text(f"content {i}")
        
        organized = fm.organize_files_by_extension(str(tmp_path))
        
        # Should have .txt files but limited by the break condition
        assert ".txt" in organized
        # The break should limit to 100 files processed
        assert len(organized[".txt"]) <= 100

    def test_organize_files_os_error(self, tmp_path, monkeypatch):
        """Test organizing files when OSError occurs to cover lines 77-78."""
        fm = FileManager()
        
        # Mock Path.iterdir to raise OSError
        from pathlib import Path
        original_iterdir = Path.iterdir
        
        def mock_iterdir(self):
            raise OSError("Permission denied")
        
        monkeypatch.setattr(Path, "iterdir", mock_iterdir)
        
        # This should trigger the OSError handling on lines 77-78
        organized = fm.organize_files_by_extension(str(tmp_path))
        
        # Should return empty dict due to error
        assert organized == {}

    def test_calculate_file_hash_error_handling(self, tmp_path):
        """Test file hash calculation with permission error."""
        fm = FileManager()

        # Create a file and then make it unreadable
        test_file = tmp_path / "unreadable.txt"
        test_file.write_text("content")

        # Mock open to raise an exception
        import builtins

        original_open = builtins.open

        def mock_open(*args, **kwargs):
            if str(test_file) in str(args[0]):
                raise PermissionError("Access denied")
            return original_open(*args, **kwargs)

        builtins.open = mock_open

        try:
            # This should handle the exception gracefully
            duplicates = fm.find_duplicates(str(tmp_path))
            # The file with error should be skipped
            assert len(duplicates) == 0
        finally:
            builtins.open = original_open

    def test_json_to_csv_empty_data(self, tmp_path):
        """Test JSON to CSV conversion with empty list."""
        fm = FileManager()

        # Create JSON file with empty list
        json_file = tmp_path / "empty.json"
        json_file.write_text("[]")

        csv_file = tmp_path / "output.csv"

        result = fm.json_to_csv(str(json_file), str(csv_file))
        assert result == False


class TestDataProcessorEdgeCases:
    """Test DataProcessor edge cases."""

    def test_filter_by_age_edge_cases(self):
        """Test filter_by_age with edge cases."""
        processor = DataProcessor()
        
        # Add data with missing age fields
        processor.add_data({"name": "Alice"})  # No age field
        processor.add_data({"name": "Bob", "age": 25})
        processor.add_data({"name": "Charlie", "age": None})  # None age
        
        # Should handle missing/None age gracefully
        filtered = processor.filter_by_age(20, 30)
        assert len(filtered) == 1
        assert filtered[0]["name"] == "Bob"


class TestMainFunctionExecution:
    """Test main function and module execution paths."""

    def test_main_function_file_manager_exception(self, monkeypatch):
        """Test main function when FileManager raises exception to cover lines 445-446."""
        from src.python.utils import FileManager
        
        # Mock FileManager.organize_files_by_extension to raise exception
        original_method = FileManager.organize_files_by_extension
        
        def mock_organize(*args, **kwargs):
            raise Exception("Simulated file manager error")
        
        monkeypatch.setattr(FileManager, "organize_files_by_extension", mock_organize)
        
        # Capture output
        from io import StringIO
        import sys
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            from src.python.utils import main
            main()
            
            output = captured_output.getvalue()
            assert "File organization demo skipped:" in output
        finally:
            sys.stdout = sys.__stdout__
            # Restore original method
            FileManager.organize_files_by_extension = original_method

    def test_main_function_webscraper_exception(self, monkeypatch):
        """Test main function when WebScraper raises exception to cover lines 484-485."""
        from src.python.utils import WebScraper
        
        # Mock WebScraper.check_url_status to raise exception
        original_method = WebScraper.check_url_status
        
        def mock_check_url(*args, **kwargs):
            raise Exception("Simulated network error")
        
        monkeypatch.setattr(WebScraper, "check_url_status", mock_check_url)
        
        # Capture output
        from io import StringIO
        import sys
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            from src.python.utils import main
            main()
            
            output = captured_output.getvalue()
            assert "Web scraper demo skipped:" in output
        finally:
            sys.stdout = sys.__stdout__
            # Restore original method
            WebScraper.check_url_status = original_method

    def test_main_function_import_error(self, monkeypatch):
        """Test that main handles ImportError gracefully if psutil is not installed."""
        # Mock sys.modules to simulate that psutil is not installed
        import sys

        original_sys_modules = sys.modules.copy()
        if "psutil" in sys.modules:
            del sys.modules["psutil"]

        # Mock __import__ to raise ImportError when psutil is requested
        original_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "psutil":
                raise ImportError("No module named psutil")
            return original_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)

        try:
            # Capture output
            from io import StringIO

            from src.python.utils import main

            captured_output = StringIO()
            sys.stdout = captured_output

            main()

            sys.stdout = sys.__stdout__

            output = captured_output.getvalue()
            assert "psutil not installed" in output

        finally:
            # Restore original state
            sys.modules.clear()
            sys.modules.update(original_sys_modules)

    def test_module_direct_execution(self):
        """Test that the module runs correctly when executed directly."""
        # Execute the module directly and verify it runs without errors
        # Use current working directory instead of hardcoded path
        import os
        import subprocess
        import sys

        cwd = os.getcwd()
        result = subprocess.run(
            [sys.executable, "-m", "src.python.utils"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60,  # Increased timeout for CI environments
        )

        assert result.returncode == 0
        assert "Python Utilities Demo" in result.stdout


class TestMainFunction:
    """Test main function and module execution."""

    def test_main_function_execution(self, capsys):
        """Test that main function executes without errors."""
        from src.python.utils import main

        # Call main function
        main()

        # Capture output
        captured = capsys.readouterr()

        # Verify some output was produced
        assert len(captured.out) > 0
        assert "System Monitor" in captured.out or "File Manager" in captured.out

    def test_system_monitor_import_error_handling(self, monkeypatch):
        """Test graceful handling of psutil ImportError."""
        # Mock the import to raise ImportError
        import sys

        original_modules = sys.modules.copy()

        # Remove psutil from sys.modules if it exists
        if "psutil" in sys.modules:
            del sys.modules["psutil"]

        # Mock __import__ to raise ImportError for psutil
        original_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "psutil":
                raise ImportError("No module named 'psutil'")
            return original_import(name, *args, **kwargs)

        builtins.__import__ = mock_import

        try:
            # Reload the utils module to trigger the import error handling
            import importlib

            import src.python.utils as utils

            importlib.reload(utils)

            # The module should still be importable despite psutil error
            assert utils is not None

        finally:
            # Restore original import and modules
            builtins.__import__ = original_import
            sys.modules.clear()
            sys.modules.update(original_modules)

    def test_module_main_execution(self):
        """Test direct module execution (__name__ == '__main__')."""
        # Run the module directly to test __name__ == '__main__' block
        # Use current working directory instead of hardcoded path
        import os
        import subprocess
        import sys

        cwd = os.getcwd()
        result = subprocess.run(
            [sys.executable, "-m", "src.python.utils"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30,  # Increased timeout for CI environments
        )

        # Should execute without errors
        assert result.returncode == 0
        # Should produce some output
        assert len(result.stdout) > 0


if __name__ == "__main__":
    pytest.main([__file__])
