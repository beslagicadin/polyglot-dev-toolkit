"""
Tests for the Python utility functions.
"""

import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'python'))

from utils import calculate_fibonacci, is_prime, generate_random_data, sort_data, DataProcessor


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
        assert all('id' in item for item in data)
        assert all('name' in item for item in data)
        assert all('age' in item for item in data)
    
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
        
        assert 'id' in item
        assert 'name' in item
        assert 'age' in item
        assert 'score' in item
        assert 'timestamp' in item
        assert 'active' in item
        
        assert isinstance(item['id'], int)
        assert isinstance(item['name'], str)
        assert isinstance(item['age'], int)
        assert isinstance(item['score'], float)
        assert isinstance(item['active'], bool)


class TestSorting:
    """Test cases for data sorting function."""
    
    def test_sort_by_age(self):
        """Test sorting by age."""
        data = [
            {'name': 'Alice', 'age': 25},
            {'name': 'Bob', 'age': 30},
            {'name': 'Charlie', 'age': 20}
        ]
        
        sorted_data = sort_data(data, 'age')
        ages = [item['age'] for item in sorted_data]
        assert ages == [20, 25, 30]
    
    def test_sort_by_age_reverse(self):
        """Test sorting by age in reverse order."""
        data = [
            {'name': 'Alice', 'age': 25},
            {'name': 'Bob', 'age': 30},
            {'name': 'Charlie', 'age': 20}
        ]
        
        sorted_data = sort_data(data, 'age', reverse=True)
        ages = [item['age'] for item in sorted_data]
        assert ages == [30, 25, 20]


class TestDataProcessor:
    """Test cases for the DataProcessor class."""
    
    def test_add_data(self):
        """Test adding data to processor."""
        processor = DataProcessor()
        assert len(processor.data) == 0
        
        processor.add_data({'name': 'Alice', 'age': 25})
        assert len(processor.data) == 1
    
    def test_filter_by_age(self):
        """Test filtering data by age range."""
        processor = DataProcessor()
        processor.add_data({'name': 'Alice', 'age': 25})
        processor.add_data({'name': 'Bob', 'age': 35})
        processor.add_data({'name': 'Charlie', 'age': 45})
        
        filtered = processor.filter_by_age(30, 40)
        assert len(filtered) == 1
        assert filtered[0]['name'] == 'Bob'
    
    def test_get_statistics_empty(self):
        """Test statistics with empty data."""
        processor = DataProcessor()
        stats = processor.get_statistics()
        assert stats == {}
    
    def test_get_statistics_with_data(self):
        """Test statistics with actual data."""
        processor = DataProcessor()
        processor.add_data({'age': 25, 'score': 85.5})
        processor.add_data({'age': 35, 'score': 92.0})
        
        stats = processor.get_statistics()
        assert stats['total_records'] == 2
        assert stats['avg_age'] == 30.0
        assert stats['min_age'] == 25
        assert stats['max_age'] == 35


if __name__ == "__main__":
    pytest.main([__file__])
