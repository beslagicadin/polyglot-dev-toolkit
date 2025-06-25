#!/usr/bin/env python3
"""
Example usage of Python utilities

Author: Adin Bešlagić
Email: beslagicadin@gmail.com
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'python'))

from utils import FileManager, DataProcessor, SystemMonitor, WebScraper


def file_management_examples():
    """Examples of file management operations"""
    print("📁 File Management Examples")
    print("-" * 30)
    
    fm = FileManager()
    
    # Organize files in current directory
    current_dir = os.getcwd()
    organized = fm.organize_files_by_extension(current_dir)
    
    print(f"Files organized by extension in {current_dir}:")
    for ext, files in organized.items():
        print(f"  {ext}: {len(files)} file(s)")
    
    print()


def data_processing_examples():
    """Examples of data processing operations"""
    print("📊 Data Processing Examples")
    print("-" * 30)
    
    dp = DataProcessor()
    
    # Create sample CSV data
    sample_csv = Path("sample_data.csv")
    sample_json = Path("sample_data.json")
    
    # Create sample CSV
    with open(sample_csv, 'w') as f:
        f.write("name,age,score\\n")
        f.write("Alice,25,95.5\\n")
        f.write("Bob,30,87.2\\n")
        f.write("Charlie,28,92.1\\n")
    
    # Convert CSV to JSON
    success = dp.csv_to_json(str(sample_csv), str(sample_json))
    if success:
        print(f"✅ Successfully converted {sample_csv} to {sample_json}")
    
    # Validate JSON
    is_valid = dp.validate_json(str(sample_json))
    print(f"JSON validation result: {'✅ Valid' if is_valid else '❌ Invalid'}")
    
    # Cleanup
    sample_csv.unlink(missing_ok=True)
    sample_json.unlink(missing_ok=True)
    
    print()


def system_monitoring_examples():
    """Examples of system monitoring operations"""
    print("🖥️ System Monitoring Examples")
    print("-" * 30)
    
    try:
        sm = SystemMonitor()
        
        # Get system information
        system_info = sm.get_system_info()
        if system_info:
            print("System Information:")
            print(f"  Platform: {system_info.get('platform', 'Unknown')}")
            print(f"  CPU Count: {system_info.get('cpu_count', 'Unknown')}")
            print(f"  Memory Total: {system_info.get('memory_total', 0) / (1024**3):.1f} GB")
        
        # Check disk space
        disk_info = sm.check_disk_space('/')
        if disk_info:
            print(f"\\nDisk Usage for {disk_info['path']}:")
            print(f"  Used: {disk_info['percentage_used']:.1f}%")
            print(f"  Free: {disk_info['free'] / (1024**3):.1f} GB")
    
    except ImportError:
        print("⚠️ psutil not available - system monitoring examples skipped")
    
    print()


def web_scraping_examples():
    """Examples of web scraping operations"""
    print("🌐 Web Scraping Examples")
    print("-" * 30)
    
    ws = WebScraper(timeout=10)
    
    # Test URLs
    test_urls = [
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404",
        "https://github.com"
    ]
    
    for url in test_urls:
        try:
            status = ws.check_url_status(url)
            status_emoji = "✅" if status['is_accessible'] else "❌"
            print(f"  {status_emoji} {url} - Status: {status.get('status_code', 'Error')}")
        except Exception as e:
            print(f"  ❌ {url} - Error: {str(e)}")
    
    print()


def algorithm_examples():
    """Examples of algorithm implementations"""
    print("🧮 Algorithm Examples")
    print("-" * 30)
    
    from utils import calculate_fibonacci, is_prime, generate_random_data, sort_data
    
    # Fibonacci examples
    fib_numbers = [calculate_fibonacci(i) for i in range(10)]
    print(f"First 10 Fibonacci numbers: {fib_numbers}")
    
    # Prime checking examples
    test_numbers = [17, 18, 19, 20, 21]
    prime_results = [(n, is_prime(n)) for n in test_numbers]
    print("Prime checking results:")
    for num, is_prime_result in prime_results:
        status = "✅ Prime" if is_prime_result else "❌ Not Prime"
        print(f"  {num}: {status}")
    
    # Data generation and sorting
    random_data = generate_random_data(5)
    print(f"\\nGenerated {len(random_data)} random records")
    
    sorted_by_age = sort_data(random_data, 'age')
    ages = [item['age'] for item in sorted_by_age]
    print(f"Ages sorted: {ages}")
    
    print()


def main():
    """Run all examples"""
    print("🚀 Python Utilities Examples")
    print("=" * 50)
    print()
    
    file_management_examples()
    data_processing_examples()
    system_monitoring_examples()
    web_scraping_examples()
    algorithm_examples()
    
    print("✅ All examples completed successfully!")


if __name__ == "__main__":
    main()
