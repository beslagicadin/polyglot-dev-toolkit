#!/usr/bin/env python3
"""
Python Utilities Module
A collection of useful utilities for data processing, file management, and automation.

Author: Adin Bešlagić
Email: beslagicadin@gmail.com
"""

import csv
import hashlib
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


class FileManager:
    """Utility class for file operations and management."""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger(f"{__name__}.FileManager")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def organize_files_by_extension(
        self, directory: str, recursive: bool = False
    ) -> Dict[str, List[str]]:
        """Organize files in a directory by their extensions."""
        dir_path = Path(directory)
        organized: Dict[str, List[str]] = {}

        if not dir_path.exists():
            self.logger.error(f"Directory {directory} does not exist")
            return organized

        try:
            # Use iterdir() for non-recursive (default for performance) or rglob() for recursive
            iterator = dir_path.rglob("*") if recursive else dir_path.iterdir()

            file_count = 0
            for file_path in iterator:
                if self._should_skip_file(file_path):
                    continue

                extension = file_path.suffix.lower() or "no_extension"
                if extension not in organized:
                    organized[extension] = []
                organized[extension].append(str(file_path))
                file_count += 1

                # Limit file processing for performance in CI
                if file_count >= 100:
                    break

            self.logger.info(
                f"Organized {sum(len(files) for files in organized.values())} files"
            )
        except OSError as e:
            self.logger.error(f"Error organizing files: {e}")
        
        return organized
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped during processing."""
        if not file_path.is_file():
            return True
        
        # Skip hidden files and common build/cache directories for performance
        skip_patterns = ["node_modules", ".git", "target", "__pycache__"]
        return (
            file_path.name.startswith(".")
            or any(part in str(file_path) for part in skip_patterns)
        )

    def find_duplicates(self, directory: str) -> Dict[str, List[str]]:
        """Find duplicate files in a directory based on content hash."""
        dir_path = Path(directory)
        hash_dict: Dict[str, str] = {}
        duplicates: Dict[str, List[str]] = {}

        if not dir_path.exists():
            self.logger.error(f"Directory {directory} does not exist")
            return duplicates

        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                try:
                    file_hash = self._calculate_file_hash(file_path)
                    if file_hash in hash_dict:
                        if file_hash not in duplicates:
                            duplicates[file_hash] = [hash_dict[file_hash]]
                        duplicates[file_hash].append(str(file_path))
                    else:
                        hash_dict[file_hash] = str(file_path)
                except Exception as e:
                    self.logger.error(f"Error processing {file_path}: {e}")

        self.logger.info(f"Found {len(duplicates)} sets of duplicate files")
        return duplicates

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def csv_to_json(self, csv_file: str, json_file: str) -> bool:
        """Convert CSV file to JSON format."""
        try:
            with open(csv_file, mode="r", encoding="utf-8") as csvf:
                csv_reader = csv.DictReader(csvf)
                data = list(csv_reader)
            with open(json_file, mode="w", encoding="utf-8") as jsonf:
                json.dump(data, jsonf, indent=2, ensure_ascii=False)
            self.logger.info(f"Successfully converted {csv_file} to {json_file}")
            return True
        except Exception as e:
            self.logger.error(f"Error converting CSV to JSON: {e}")
            return False

    def json_to_csv(self, json_file: str, csv_file: str) -> bool:
        """Convert JSON file to CSV format."""
        try:
            with open(json_file, mode="r", encoding="utf-8") as jsonf:
                data = json.load(jsonf)
            if isinstance(data, list) and isinstance(data[0], dict):
                fieldnames = data[0].keys()
                with open(csv_file, mode="w", newline="", encoding="utf-8") as csvf:
                    writer = csv.DictWriter(csvf, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
                self.logger.info(f"Successfully converted {json_file} to {csv_file}")
                return True
            else:
                self.logger.error("JSON data must be a list of dictionaries")
                return False
        except Exception as e:
            self.logger.error(f"Error converting JSON to CSV: {e}")
            return False

    def validate_json(self, json_file: str) -> bool:
        """Validate JSON file format."""
        try:
            with open(json_file, mode="r", encoding="utf-8") as f:
                json.load(f)
            self.logger.info(f"JSON file {json_file} is valid")
            return True
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in {json_file}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error validating JSON file: {e}")
            return False


class DataProcessor:
    """Class for processing data with various utilities."""

    def __init__(self):
        self.data: List[Dict[str, Any]] = []

    def add_data(self, item: Dict[str, Any]) -> None:
        """Add a data item to the processor."""
        self.data.append(item)

    def filter_by_age(self, min_age: int, max_age: int) -> List[Dict[str, Any]]:
        """Filter data by age range."""
        return [item for item in self.data if min_age <= item.get("age", 0) <= max_age]

    def get_statistics(self) -> Dict[str, float]:
        """Calculate basic statistics for numerical fields."""
        if not self.data:
            return {}
        ages = [item.get("age", 0) for item in self.data]
        scores = [item.get("score", 0) for item in self.data]
        return {
            "total_records": len(self.data),
            "avg_age": sum(ages) / len(ages) if ages else 0,
            "avg_score": sum(scores) / len(scores) if scores else 0,
            "min_age": min(ages) if ages else 0,
            "max_age": max(ages) if ages else 0,
            "min_score": min(scores) if scores else 0,
            "max_score": max(scores) if scores else 0,
        }



class SystemMonitor:
    """Utility class for system monitoring operations."""

    def __init__(self):
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger(f"{__name__}.SystemMonitor")
        logger.setLevel(logging.INFO)
        return logger

    def get_system_info(self) -> Dict[str, Any]:
        """Get basic system information."""
        import platform

        import psutil

        try:
            info = {
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total,
                "memory_available": psutil.virtual_memory().available,
                "disk_usage": psutil.disk_usage("/").percent,
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info("Successfully retrieved system information")
            return info

        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            return {}

    def check_disk_space(self, path: str = "/") -> Dict[str, Any]:
        """Check disk space for given path."""
        try:
            import psutil

            usage = psutil.disk_usage(path)

            result = {
                "path": path,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percentage_used": (usage.used / usage.total) * 100,
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"Disk usage for {path}: {result['percentage_used']:.1f}%")
            return result

        except Exception as e:
            self.logger.error(f"Error checking disk space: {e}")
            return {}


class WebScraper:
    """Utility class for web scraping operations."""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger(f"{__name__}.WebScraper")
        logger.setLevel(logging.INFO)
        return logger

    def fetch_url(
        self, url: str, headers: Optional[Dict[str, str]] = None
    ) -> Optional[str]:
        """Fetch content from a URL."""
        try:
            default_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            if headers:
                default_headers.update(headers)

            response = self.session.get(
                url, headers=default_headers, timeout=self.timeout
            )
            response.raise_for_status()

            self.logger.info(f"Successfully fetched {url}")
            return response.text

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    def check_url_status(self, url: str) -> Dict[str, Any]:
        """Check the status of a URL."""
        try:
            response = self.session.head(url, timeout=self.timeout)

            result = {
                "url": url,
                "status_code": response.status_code,
                "is_accessible": response.status_code == 200,
                "headers": dict(response.headers),
                "timestamp": datetime.now().isoformat(),
            }

            self.logger.info(f"URL {url} status: {response.status_code}")
            return result

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error checking {url}: {e}")
            return {
                "url": url,
                "status_code": None,
                "is_accessible": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }


# Utility functions

import math
import random


def calculate_fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number using dynamic programming.

    Args:
        n (int): Position in Fibonacci sequence

    Returns:
        int: The nth Fibonacci number

    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b

    return b


def is_prime(num: int) -> bool:
    """
    Check if a number is prime.

    Args:
        num (int): Number to check

    Returns:
        bool: True if prime, False otherwise
    """
    if num < 2:
        return False

    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False

    return True


def generate_random_data(size: int = 10) -> List[Dict[str, Any]]:
    """
    Generate random data for testing purposes.

    Args:
        size (int): Number of records to generate

    Returns:
        List[Dict[str, Any]]: List of random data records
    """
    names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]

    data = []
    for i in range(size):
        record = {
            "id": i + 1,
            "name": random.choice(names),
            "age": random.randint(18, 65),
            "score": round(random.uniform(0, 100), 2),
            "timestamp": datetime.now().isoformat(),
            "active": random.choice([True, False]),
        }
        data.append(record)

    return data


def sort_data(
    data: List[Dict[str, Any]], key: str, reverse: bool = False
) -> List[Dict[str, Any]]:
    """
    Sort a list of dictionaries by a specified key.

    Args:
        data (List[Dict[str, Any]]): Data to sort
        key (str): Key to sort by
        reverse (bool): Sort in descending order if True

    Returns:
        List[Dict[str, Any]]: Sorted data
    """
    return sorted(data, key=lambda x: x.get(key, 0), reverse=reverse)


def main():
    """Main function to demonstrate the utilities."""
    print("Python Utilities Demo")
    print("====================\n")

    # File Manager Demo
    print("1. File Manager Demo:")
    fm = FileManager()
    # Use a smaller, controlled directory for CI compatibility
    # Try src directory first, fallback to current directory with limit
    test_dir = "src" if os.path.exists("src") else "."
    try:
        organized = fm.organize_files_by_extension(test_dir)
        print(f"Found {len(organized)} different file types in {test_dir} directory")
    except Exception as e:
        print(f"File organization demo skipped: {e}")

    # Data Processor Demo
    print("\n2. Data Processor Demo:")
    dp = DataProcessor()
    sample_data = generate_random_data(5)

    for item in sample_data:
        dp.add_data(item)

    print("\nGenerated data:")
    for item in sample_data:
        print(f"  {item}")

    print("\nStatistics:", dp.get_statistics())

    # Utility functions demo
    print("\n5. Utility Functions Demo:")
    print("Fibonacci(10):", calculate_fibonacci(10))
    print("Is 17 prime?", is_prime(17))

    # System Monitor Demo
    print("\n3. System Monitor Demo:")
    sm = SystemMonitor()
    try:
        system_info = sm.get_system_info()
        if system_info:
            print(f"Platform: {system_info.get('platform', 'Unknown')}")
            print(f"CPU Count: {system_info.get('cpu_count', 'Unknown')}")
    except ImportError:
        print("psutil not installed - skipping system monitor demo")

    # Web Scraper Demo
    print("\n4. Web Scraper Demo:")
    ws = WebScraper(timeout=5)  # Shorter timeout for CI
    try:
        status = ws.check_url_status("https://httpbin.org/status/200")
        print(f"Test URL status: {status.get('status_code', 'Error')}")
    except Exception as e:
        print(f"Web scraper demo skipped: {e}")

    print("\nDemo completed!")


if __name__ == "__main__":
    main()
