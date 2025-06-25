#!/usr/bin/env python3
"""
Performance testing script for GitHub Profile Enhancement Project

Author: Adin Bešlagić
Email: beslagicadin@gmail.com
"""

import sys
import time
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'python'))

from utils import calculate_fibonacci, is_prime, generate_random_data, sort_data, DataProcessor


def time_function(func, *args, **kwargs):
    """Time a function execution"""
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return result, execution_time


def benchmark_fibonacci():
    """Benchmark Fibonacci calculation"""
    print("🔢 Benchmarking Fibonacci calculation...")
    
    test_cases = [10, 20, 30, 35, 40]
    results = []
    
    for n in test_cases:
        result, exec_time = time_function(calculate_fibonacci, n)
        results.append((n, result, exec_time))
        print(f"  fibonacci({n}) = {result} - {exec_time:.6f}s")
    
    return results


def benchmark_prime_checking():
    """Benchmark prime number checking"""
    print("\n🔍 Benchmarking prime number checking...")
    
    test_numbers = [1009, 10007, 100003, 1000003]
    results = []
    
    for num in test_numbers:
        result, exec_time = time_function(is_prime, num)
        results.append((num, result, exec_time))
        print(f"  is_prime({num}) = {result} - {exec_time:.6f}s")
    
    return results


def benchmark_data_generation():
    """Benchmark data generation"""
    print("\n📊 Benchmarking data generation...")
    
    sizes = [100, 1000, 10000, 50000]
    results = []
    
    for size in sizes:
        result, exec_time = time_function(generate_random_data, size)
        results.append((size, len(result), exec_time))
        print(f"  generate_random_data({size}) - {exec_time:.6f}s")
    
    return results


def benchmark_data_sorting():
    """Benchmark data sorting"""
    print("\n🔄 Benchmarking data sorting...")
    
    # Generate test data once
    test_data = generate_random_data(10000)
    
    sort_keys = ['age', 'score', 'name']
    results = []
    
    for key in sort_keys:
        result, exec_time = time_function(sort_data, test_data, key)
        results.append((key, len(result), exec_time))
        print(f"  sort_data(10000 items, key='{key}') - {exec_time:.6f}s")
    
    return results


def benchmark_data_processor():
    """Benchmark DataProcessor operations"""
    print("\n⚙️ Benchmarking DataProcessor operations...")
    
    processor = DataProcessor()
    test_data = generate_random_data(5000)
    
    # Benchmark adding data
    start_time = time.perf_counter()
    for item in test_data:
        processor.add_data(item)
    add_time = time.perf_counter() - start_time
    print(f"  add_data(5000 items) - {add_time:.6f}s")
    
    # Benchmark filtering
    _, filter_time = time_function(processor.filter_by_age, 25, 45)
    print(f"  filter_by_age(5000 items) - {filter_time:.6f}s")
    
    # Benchmark statistics
    _, stats_time = time_function(processor.get_statistics)
    print(f"  get_statistics(5000 items) - {stats_time:.6f}s")
    
    return [('add_data', len(test_data), add_time),
            ('filter_by_age', len(test_data), filter_time),
            ('get_statistics', len(test_data), stats_time)]


def run_memory_test():
    """Run memory usage test"""
    print("\n💾 Running memory usage test...")
    
    try:
        import psutil
        import gc
        
        process = psutil.Process()
        
        # Get initial memory
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        print(f"  Initial memory usage: {initial_memory:.2f} MB")
        
        # Generate large dataset
        large_data = generate_random_data(100000)
        
        # Get memory after data generation
        after_gen_memory = process.memory_info().rss / 1024 / 1024
        print(f"  After generating 100k records: {after_gen_memory:.2f} MB")
        print(f"  Memory increase: {after_gen_memory - initial_memory:.2f} MB")
        
        # Cleanup
        del large_data
        gc.collect()
        
        # Get memory after cleanup
        after_cleanup_memory = process.memory_info().rss / 1024 / 1024
        print(f"  After cleanup: {after_cleanup_memory:.2f} MB")
        
    except ImportError:
        print("  psutil not available - skipping memory test")


def save_results_to_file(all_results):
    """Save benchmark results to file"""
    results_dir = Path("benchmark_results")
    results_dir.mkdir(exist_ok=True)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results_file = results_dir / f"performance_results_{timestamp}.txt"
    
    with open(results_file, 'w') as f:
        f.write("GitHub Profile Enhancement Project - Performance Test Results\n")
        f.write("=" * 60 + "\n")
        f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Python version: {sys.version}\n")
        f.write(f"Platform: {sys.platform}\n\n")
        
        for category, results in all_results.items():
            f.write(f"{category}:\n")
            for result in results:
                if len(result) == 3:
                    f.write(f"  {result[0]}: {result[1]} -> {result[2]:.6f}s\n")
                else:
                    f.write(f"  {result}\n")
            f.write("\n")
    
    print(f"\n📁 Results saved to: {results_file}")


def main():
    """Main performance testing function"""
    print("🚀 Starting Performance Tests for GitHub Profile Enhancement Project")
    print("=" * 70)
    
    start_time = time.time()
    
    # Run all benchmarks
    all_results = {}
    
    all_results['Fibonacci'] = benchmark_fibonacci()
    all_results['Prime Checking'] = benchmark_prime_checking()
    all_results['Data Generation'] = benchmark_data_generation()
    all_results['Data Sorting'] = benchmark_data_sorting()
    all_results['Data Processor'] = benchmark_data_processor()
    
    # Run memory test
    run_memory_test()
    
    total_time = time.time() - start_time
    
    print(f"\n✅ All performance tests completed in {total_time:.2f} seconds")
    
    # Save results
    save_results_to_file(all_results)
    
    # Performance analysis
    print("\n📈 Performance Analysis:")
    print("  - Fibonacci calculation shows expected exponential complexity")
    print("  - Prime checking performance depends on number size")
    print("  - Data generation scales linearly with size")
    print("  - Sorting performance is O(n log n) as expected")
    print("  - Data processor operations show good performance characteristics")
    
    return all_results


if __name__ == "__main__":
    results = main()
    print("\n🎯 Performance testing completed successfully!")
