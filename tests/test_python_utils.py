#!/usr/bin/env python3
"""
Comprehensive tests for Python utilities module

Author: Adin Bešlagić
Email: beslagicadin@gmail.com
"""

import unittest
import os
import sys
import tempfile
import json
import csv
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'python'))

from utils import (
    FileManager, DataProcessor, SystemMonitor, WebScraper,
    calculate_fibonacci, is_prime, generate_random_data, sort_data
)


class TestFileManager(unittest.TestCase):
    """Test cases for FileManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.file_manager = FileManager(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_organize_files_by_extension(self):
        """Test file organization by extension"""
        # Create test files
        test_files = ['test.txt', 'image.jpg', 'document.pdf', 'script.py']
        for filename in test_files:
            file_path = Path(self.temp_dir) / filename
            file_path.write_text('test content')
        
        # Test organization
        organized = self.file_manager.organize_files_by_extension(self.temp_dir)
        
        # Verify results
        self.assertIn('.txt', organized)
        self.assertIn('.jpg', organized)
        self.assertIn('.pdf', organized)
        self.assertIn('.py', organized)
        self.assertEqual(len(organized['.txt']), 1)
    
    def test_organize_nonexistent_directory(self):
        """Test organizing files in non-existent directory"""
        result = self.file_manager.organize_files_by_extension('/nonexistent/path')
        self.assertEqual(result, {})
    
    def test_find_duplicates(self):
        """Test duplicate file detection"""
        # Create duplicate files
        content1 = 'identical content'
        content2 = 'different content'
        
        file1 = Path(self.temp_dir) / 'file1.txt'
        file2 = Path(self.temp_dir) / 'file2.txt'
        file3 = Path(self.temp_dir) / 'file3.txt'
        
        file1.write_text(content1)
        file2.write_text(content1)  # Duplicate
        file3.write_text(content2)  # Different
        
        duplicates = self.file_manager.find_duplicates(self.temp_dir)
        
        # Should find one set of duplicates
        self.assertEqual(len(duplicates), 1)
        duplicate_files = list(duplicates.values())[0]
        self.assertEqual(len(duplicate_files), 2)


class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.data_processor = DataProcessor()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_csv_to_json_conversion(self):
        """Test CSV to JSON conversion"""
        # Create test CSV
        csv_file = Path(self.temp_dir) / 'test.csv'
        json_file = Path(self.temp_dir) / 'test.json'
        
        csv_data = [
            ['name', 'age', 'score'],
            ['Alice', '25', '95.5'],
            ['Bob', '30', '87.2']
        ]
        
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)
        
        # Test conversion
        success = self.data_processor.csv_to_json(str(csv_file), str(json_file))
        
        self.assertTrue(success)
        self.assertTrue(json_file.exists())
        
        # Verify JSON content
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Alice')
        self.assertEqual(data[0]['age'], '25')
    
    def test_json_to_csv_conversion(self):
        """Test JSON to CSV conversion"""
        # Create test JSON
        json_file = Path(self.temp_dir) / 'test.json'
        csv_file = Path(self.temp_dir) / 'test.csv'
        
        json_data = [
            {'name': 'Alice', 'age': 25, 'score': 95.5},
            {'name': 'Bob', 'age': 30, 'score': 87.2}
        ]
        
        with open(json_file, 'w') as f:
            json.dump(json_data, f)
        
        # Test conversion
        success = self.data_processor.json_to_csv(str(json_file), str(csv_file))
        
        self.assertTrue(success)
        self.assertTrue(csv_file.exists())
        
        # Verify CSV content
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['name'], 'Alice')
    
    def test_validate_json_valid(self):
        """Test JSON validation with valid file"""
        json_file = Path(self.temp_dir) / 'valid.json'
        json_data = {'key': 'value', 'number': 42}
        
        with open(json_file, 'w') as f:
            json.dump(json_data, f)
        
        is_valid = self.data_processor.validate_json(str(json_file))
        self.assertTrue(is_valid)
    
    def test_validate_json_invalid(self):
        """Test JSON validation with invalid file"""
        json_file = Path(self.temp_dir) / 'invalid.json'
        
        with open(json_file, 'w') as f:
            f.write('{"invalid": json content}')
        
        is_valid = self.data_processor.validate_json(str(json_file))
        self.assertFalse(is_valid)


class TestSystemMonitor(unittest.TestCase):
    """Test cases for SystemMonitor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.system_monitor = SystemMonitor()
    
    @patch('builtins.__import__')
    def test_get_system_info(self, mock_import):
        """Test system information retrieval"""
        # Create mock modules
        mock_platform = MagicMock()
        mock_platform.system.return_value = 'Linux'
        mock_platform.release.return_value = '5.4.0'
        mock_platform.version.return_value = '#1 Ubuntu'
        mock_platform.machine.return_value = 'x86_64'
        mock_platform.processor.return_value = 'Intel'
        
        mock_psutil = MagicMock()
        mock_psutil.cpu_count.return_value = 4
        
        mock_memory = MagicMock()
        mock_memory.total = 8589934592  # 8GB
        mock_memory.available = 4294967296  # 4GB
        mock_psutil.virtual_memory.return_value = mock_memory
        
        mock_disk = MagicMock()
        mock_disk.percent = 45.5
        mock_psutil.disk_usage.return_value = mock_disk
        
        # Configure mock_import to return our mocks
        def import_side_effect(name, *args, **kwargs):
            if name == 'platform':
                return mock_platform
            elif name == 'psutil':
                return mock_psutil
            else:
                return MagicMock()
        
        mock_import.side_effect = import_side_effect
        
        # Test system info retrieval
        info = self.system_monitor.get_system_info()
        
        self.assertIsInstance(info, dict)
        self.assertEqual(info['platform'], 'Linux')
        self.assertEqual(info['cpu_count'], 4)
        self.assertEqual(info['memory_total'], 8589934592)
        self.assertIn('timestamp', info)
    
    @patch('builtins.__import__')
    def test_check_disk_space(self, mock_import):
        """Test disk space checking"""
        mock_psutil = MagicMock()
        mock_usage = MagicMock()
        mock_usage.total = 1000000000  # 1GB
        mock_usage.used = 400000000    # 400MB
        mock_usage.free = 600000000    # 600MB
        mock_psutil.disk_usage.return_value = mock_usage
        
        # Configure mock_import
        def import_side_effect(name, *args, **kwargs):
            if name == 'psutil':
                return mock_psutil
            else:
                return MagicMock()
        
        mock_import.side_effect = import_side_effect
        
        result = self.system_monitor.check_disk_space('/')
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['total'], 1000000000)
        self.assertEqual(result['used'], 400000000)
        self.assertEqual(result['free'], 600000000)
        self.assertEqual(result['percentage_used'], 40.0)


class TestWebScraper(unittest.TestCase):
    """Test cases for WebScraper class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.web_scraper = WebScraper(timeout=5)
    
    @patch('utils.requests.Session')
    def test_fetch_url_success(self, mock_session_class):
        """Test successful URL fetching"""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '<html>Test content</html>'
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        scraper = WebScraper()
        result = scraper.fetch_url('https://example.com')
        
        self.assertEqual(result, '<html>Test content</html>')
        mock_session.get.assert_called_once()
    
    @patch('utils.requests.Session')
    def test_check_url_status_success(self, mock_session_class):
        """Test URL status checking"""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'text/html'}
        mock_session.head.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        scraper = WebScraper()
        result = scraper.check_url_status('https://example.com')
        
        self.assertEqual(result['status_code'], 200)
        self.assertTrue(result['is_accessible'])
        self.assertIn('timestamp', result)


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for standalone utility functions"""
    
    def test_calculate_fibonacci(self):
        """Test Fibonacci calculation"""
        test_cases = [
            (0, 0),
            (1, 1),
            (2, 1),
            (3, 2),
            (5, 5),
            (10, 55)
        ]
        
        for n, expected in test_cases:
            with self.subTest(n=n):
                result = calculate_fibonacci(n)
                self.assertEqual(result, expected)
    
    def test_calculate_fibonacci_negative(self):
        """Test Fibonacci with negative input"""
        with self.assertRaises(ValueError):
            calculate_fibonacci(-1)
    
    def test_is_prime(self):
        """Test prime number checking"""
        prime_cases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        non_prime_cases = [0, 1, 4, 6, 8, 9, 10, 12, 15, 16]
        
        for num in prime_cases:
            with self.subTest(num=num):
                self.assertTrue(is_prime(num))
        
        for num in non_prime_cases:
            with self.subTest(num=num):
                self.assertFalse(is_prime(num))
    
    def test_generate_random_data(self):
        """Test random data generation"""
        data = generate_random_data(5)
        
        self.assertEqual(len(data), 5)
        
        for item in data:
            self.assertIsInstance(item, dict)
            self.assertIn('id', item)
            self.assertIn('name', item)
            self.assertIn('age', item)
            self.assertIn('score', item)
            self.assertIn('timestamp', item)
            self.assertIn('active', item)
            
            # Check data types and ranges
            self.assertIsInstance(item['id'], int)
            self.assertIsInstance(item['name'], str)
            self.assertIsInstance(item['age'], int)
            self.assertIsInstance(item['score'], float)
            self.assertIsInstance(item['active'], bool)
            
            self.assertGreaterEqual(item['age'], 18)
            self.assertLessEqual(item['age'], 65)
            self.assertGreaterEqual(item['score'], 0)
            self.assertLessEqual(item['score'], 100)
    
    def test_sort_data(self):
        """Test data sorting"""
        test_data = [
            {'name': 'Alice', 'age': 30, 'score': 85.5},
            {'name': 'Bob', 'age': 25, 'score': 92.0},
            {'name': 'Charlie', 'age': 35, 'score': 78.3}
        ]
        
        # Sort by age ascending
        sorted_by_age = sort_data(test_data, 'age')
        ages = [item['age'] for item in sorted_by_age]
        self.assertEqual(ages, [25, 30, 35])
        
        # Sort by score descending
        sorted_by_score = sort_data(test_data, 'score', reverse=True)
        scores = [item['score'] for item in sorted_by_score]
        self.assertEqual(scores, [92.0, 85.5, 78.3])


class TestDataProcessorClass(unittest.TestCase):
    """Test cases for DataProcessor class functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = DataProcessor()
    
    def test_add_data(self):
        """Test adding data to processor"""
        item = {'id': 1, 'name': 'Test', 'age': 25}
        self.processor.add_data(item)
        
        self.assertEqual(len(self.processor.data), 1)
        self.assertEqual(self.processor.data[0], item)
    
    def test_filter_by_age(self):
        """Test filtering data by age range"""
        test_data = [
            {'name': 'Alice', 'age': 20},
            {'name': 'Bob', 'age': 30},
            {'name': 'Charlie', 'age': 40},
            {'name': 'Diana', 'age': 50}
        ]
        
        for item in test_data:
            self.processor.add_data(item)
        
        filtered = self.processor.filter_by_age(25, 45)
        names = [item['name'] for item in filtered]
        
        self.assertEqual(len(filtered), 2)
        self.assertIn('Bob', names)
        self.assertIn('Charlie', names)
    
    def test_get_statistics(self):
        """Test statistics calculation"""
        test_data = [
            {'age': 20, 'score': 80.0},
            {'age': 30, 'score': 90.0},
            {'age': 40, 'score': 70.0}
        ]
        
        for item in test_data:
            self.processor.add_data(item)
        
        stats = self.processor.get_statistics()
        
        self.assertEqual(stats['total_records'], 3)
        self.assertEqual(stats['avg_age'], 30.0)
        self.assertEqual(stats['avg_score'], 80.0)
        self.assertEqual(stats['min_age'], 20)
        self.assertEqual(stats['max_age'], 40)
    
    def test_get_statistics_empty(self):
        """Test statistics with empty data"""
        stats = self.processor.get_statistics()
        self.assertEqual(stats, {})


if __name__ == '__main__':
    # Create test suite
    test_classes = [
        TestFileManager,
        TestDataProcessor,
        TestSystemMonitor,
        TestWebScraper,
        TestUtilityFunctions,
        TestDataProcessorClass
    ]
    
    suite = unittest.TestSuite()
    for test_class in test_classes:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_class))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
