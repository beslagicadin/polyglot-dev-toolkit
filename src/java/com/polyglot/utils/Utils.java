/**
 * Java Utilities Module
 * A collection of useful utilities for data structures, algorithms, and common operations.
 * 
 * Author: Adin Bešlagić
 * Email: beslagicadin@gmail.com
 */

package com.polyglot.utils;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ThreadLocalRandom;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Utility class for common data operations
 */
public class Utils {
    
    private static final Logger LOGGER = Logger.getLogger(Utils.class.getName());
    
    /**
     * Calculate the nth Fibonacci number using dynamic programming
     * @param n Position in Fibonacci sequence
     * @return The nth Fibonacci number
     * @throws IllegalArgumentException if n is negative
     */
    public static long fibonacci(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("n must be non-negative");
        }
        
        if (n <= 1) {
            return n;
        }
        
        long a = 0, b = 1;
        for (int i = 2; i <= n; i++) {
            long temp = a + b;
            a = b;
            b = temp;
        }
        
        return b;
    }
    
    /**
     * Check if a number is prime
     * @param num Number to check
     * @return true if prime, false otherwise
     */
    public static boolean isPrime(int num) {
        if (num < 2) {
            return false;
        }
        
        for (int i = 2; i <= Math.sqrt(num); i++) {
            if (num % i == 0) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * Find all prime numbers up to n using Sieve of Eratosthenes
     * @param n Upper limit
     * @return List of prime numbers
     */
    public static List<Integer> sieveOfEratosthenes(int n) {
        boolean[] isPrime = new boolean[n + 1];
        Arrays.fill(isPrime, true);
        isPrime[0] = isPrime[1] = false;
        
        for (int i = 2; i * i <= n; i++) {
            if (isPrime[i]) {
                for (int j = i * i; j <= n; j += i) {
                    isPrime[j] = false;
                }
            }
        }
        
        List<Integer> primes = new ArrayList<>();
        for (int i = 2; i <= n; i++) {
            if (isPrime[i]) {
                primes.add(i);
            }
        }
        
        return primes;
    }
    
    /**
     * Generic binary search implementation
     * @param array Sorted array to search
     * @param target Target value
     * @return Index of target or -1 if not found
     */
    public static <T extends Comparable<T>> int binarySearch(T[] array, T target) {
        int left = 0, right = array.length - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            int comparison = array[mid].compareTo(target);
            
            if (comparison == 0) {
                return mid;
            } else if (comparison < 0) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return -1;
    }
    
    /**
     * Calculate SHA-256 hash of a string
     * @param input Input string
     * @return SHA-256 hash as hexadecimal string
     */
    public static String calculateSHA256(String input) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(input.getBytes());
            StringBuilder hexString = new StringBuilder();
            
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) {
                    hexString.append('0');
                }
                hexString.append(hex);
            }
            
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new UtilsException("SHA-256 algorithm not available", e);
        }
    }
    
    /**
     * Generate random data for testing purposes
     * @param size Number of records to generate
     * @return List of random Person objects
     */
    public static List<Person> generateRandomData(int size) {
        String[] names = {"Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"};
        List<Person> data = new ArrayList<>();
        
        for (int i = 0; i < size; i++) {
            // ThreadLocalRandom is safe for test data generation (not cryptographic purposes)
            String name = names[ThreadLocalRandom.current().nextInt(names.length)];
            int age = ThreadLocalRandom.current().nextInt(18, 66);
            double score = ThreadLocalRandom.current().nextDouble(0, 100);
            
            data.add(new Person(i + 1, name, age, score));
        }
        
        return data;
    }
    
    /**
     * Group list of objects by a key function
     * @param list List to group
     * @param keyFunction Function to extract grouping key
     * @return Map with grouped results
     */
    public static <T, K> Map<K, List<T>> groupBy(List<T> list, Function<T, K> keyFunction) {
        return list.stream()
                   .collect(Collectors.groupingBy(keyFunction));
    }
    
    /**
     * Calculate statistics for a list of numbers
     * @param numbers List of numbers
     * @return Statistics object
     */
    public static Statistics calculateStatistics(List<Double> numbers) {
        if (numbers.isEmpty()) {
            return new Statistics(0, 0.0, 0.0, 0.0, 0.0);
        }
        
        double sum = numbers.stream().mapToDouble(Double::doubleValue).sum();
        double average = sum / numbers.size();
        double min = numbers.stream().mapToDouble(Double::doubleValue).min().orElse(0.0);
        double max = numbers.stream().mapToDouble(Double::doubleValue).max().orElse(0.0);
        
        return new Statistics(numbers.size(), sum, average, min, max);
    }
    
    /**
     * Async operation simulation
     * @param input Input string
     * @param delayMs Delay in milliseconds
     * @return CompletableFuture with processed result
     */
    public static CompletableFuture<String> processAsync(String input, long delayMs) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(delayMs);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new UtilsException("Operation interrupted", e);
            }
            
            return String.format("Processed: %s at %s", 
                               input, 
                               LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        });
    }
    
    /**
     * Person class for testing data structures
     */
    public static class Person {
        private final int id;
        private final String name;
        private final int age;
        private final double score;
        
        public Person(int id, String name, int age, double score) {
            this.id = id;
            this.name = name;
            this.age = age;
            this.score = score;
        }
        
        // Getters
        public int getId() {
            return id;
        }
        
        public String getName() {
            return name;
        }
        
        public int getAge() {
            return age;
        }
        
        public double getScore() {
            return score;
        }
        
        @Override
        public String toString() {
            return String.format("Person{id=%d, name='%s', age=%d, score=%.2f}", 
                               id, name, age, score);
        }
        
        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            Person person = (Person) obj;
            return id == person.id;
        }
        
        @Override
        public int hashCode() {
            return Objects.hash(id);
        }
    }
    
    /**
     * Statistics record class
     */
    public static class Statistics {
        private final int count;
        private final double sum;
        private final double average;
        private final double min;
        private final double max;
        
        public Statistics(int count, double sum, double average, double min, double max) {
            this.count = count;
            this.sum = sum;
            this.average = average;
            this.min = min;
            this.max = max;
        }
        
        // Getters
        public int getCount() {
            return count;
        }
        
        public double getSum() {
            return sum;
        }
        
        public double getAverage() {
            return average;
        }
        
        public double getMin() {
            return min;
        }
        
        public double getMax() {
            return max;
        }
        
        @Override
        public String toString() {
            return String.format("Statistics{count=%d, sum=%.2f, avg=%.2f, min=%.2f, max=%.2f}", 
                               count, sum, average, min, max);
        }
    }
    
    /**
     * Custom unchecked exception for utility operations.
     * 
     * Note: This is an unchecked exception (extends RuntimeException) which means
     * callers are not required to handle it in try-catch blocks. This design choice
     * allows for cleaner code when calling utility methods that may fail due to
     * system issues (like missing algorithms or interrupted operations).
     * 
     * @since 1.0.0
     */
    public static class UtilsException extends RuntimeException {
        public UtilsException(String message) {
            super(message);
        }
        
        public UtilsException(String message, Throwable cause) {
            super(message, cause);
        }
    }
    
    /**
     * Main method for testing utilities
     */
    public static void main(String[] args) {
        LOGGER.info("Java Utilities Demo");
        LOGGER.info("===================\n");
        
        // Test Fibonacci
        LOGGER.info("1. Fibonacci Demo:");
        LOGGER.info("Fibonacci(10): " + fibonacci(10));
        
        // Test prime checking
        LOGGER.info("\n2. Prime Number Demo:");
        LOGGER.info("Is 17 prime? " + isPrime(17));
        LOGGER.info("Primes up to 20: " + sieveOfEratosthenes(20));
        
        // Test data generation and processing
        LOGGER.info("\n3. Data Processing Demo:");
        List<Person> people = generateRandomData(5);
        LOGGER.info("Generated people:");
        people.forEach(person -> LOGGER.info(person.toString()));
        
        // Group by age range
        Map<String, List<Person>> grouped = groupBy(people, person -> {
            int age = person.getAge();
            if (age < 30) return "Young";
            else if (age < 50) return "Middle";
            else return "Senior";
        });
        
        LOGGER.info("\nGrouped by age:");
        grouped.forEach((key, value) -> 
            LOGGER.info(key + ": " + value.size() + " people"));
        
        // Test statistics
        LOGGER.info("\n4. Statistics Demo:");
        // Note: Stream.toList() returns an immutable list (Java 16+)
        // If you need a mutable list, use .collect(Collectors.toList()) instead
        List<Double> scores = people.stream()
                                   .map(Person::getScore)
                                   .toList();
        Statistics stats = calculateStatistics(scores);
        LOGGER.info("Score statistics: " + stats);
        
        // Test SHA-256
        LOGGER.info("\n5. Hashing Demo:");
        String input = "Hello, GitHub!";
        LOGGER.info("SHA-256 of '" + input + "': " + calculateSHA256(input));
        
        // Test async operation
        LOGGER.info("\n6. Async Operation Demo:");
        CompletableFuture<String> future = processAsync("GitHub Stats Enhancement", 1000);
        future.thenAccept(result -> LOGGER.info("Async result: " + result));
        
        LOGGER.info("\nDemo completed!");
        
        // Wait for async operation to complete
        try {
            future.get();
        } catch (InterruptedException e) {
            // Re-interrupt the thread as required by Sonar
            Thread.currentThread().interrupt();
            LOGGER.log(Level.SEVERE, "Async operation interrupted: " + e.getMessage(), e);
        } catch (Exception e) {
            LOGGER.log(Level.SEVERE, "Error in async operation: " + e.getMessage(), e);
        }
    }
}
