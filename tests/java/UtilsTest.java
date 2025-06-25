package com.polyglot.utils;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

/**
 * Comprehensive test suite for Java Utils class
 * 
 * @author Adin Bešlagić
 */
public class UtilsTest {

    @Test
    @DisplayName("Test Fibonacci calculation")
    void testFibonacci() {
        // Test base cases
        assertEquals(0, Utils.fibonacci(0));
        assertEquals(1, Utils.fibonacci(1));
        
        // Test known values
        assertEquals(1, Utils.fibonacci(2));
        assertEquals(2, Utils.fibonacci(3));
        assertEquals(55, Utils.fibonacci(10));
        
        // Test negative input
        assertThrows(IllegalArgumentException.class, () -> Utils.fibonacci(-1));
    }

    @Test
    @DisplayName("Test prime number checking")
    void testIsPrime() {
        // Test small numbers
        assertFalse(Utils.isPrime(0));
        assertFalse(Utils.isPrime(1));
        assertTrue(Utils.isPrime(2));
        assertTrue(Utils.isPrime(3));
        assertFalse(Utils.isPrime(4));
        assertTrue(Utils.isPrime(5));
        
        // Test larger primes
        assertTrue(Utils.isPrime(17));
        assertTrue(Utils.isPrime(97));
        assertFalse(Utils.isPrime(100));
    }

    @Test
    @DisplayName("Test Sieve of Eratosthenes")
    void testSieveOfEratosthenes() {
        List<Integer> primes = Utils.sieveOfEratosthenes(10);
        List<Integer> expected = Arrays.asList(2, 3, 5, 7);
        assertEquals(expected, primes);
        
        // Test edge case
        List<Integer> primesSmall = Utils.sieveOfEratosthenes(2);
        assertEquals(Arrays.asList(2), primesSmall);
    }

    @Test
    @DisplayName("Test binary search")
    void testBinarySearch() {
        Integer[] array = {1, 3, 5, 7, 9, 11, 13, 15};
        
        // Test existing elements
        assertEquals(0, Utils.binarySearch(array, 1));
        assertEquals(3, Utils.binarySearch(array, 7));
        assertEquals(7, Utils.binarySearch(array, 15));
        
        // Test non-existing elements
        assertEquals(-1, Utils.binarySearch(array, 2));
        assertEquals(-1, Utils.binarySearch(array, 16));
        
        // Test empty array
        Integer[] emptyArray = {};
        assertEquals(-1, Utils.binarySearch(emptyArray, 5));
    }

    @Test
    @DisplayName("Test SHA-256 hashing")
    void testCalculateSHA256() {
        String input = "Hello, World!";
        String hash = Utils.calculateSHA256(input);
        
        // SHA-256 should always produce 64-character hex string
        assertEquals(64, hash.length());
        
        // Same input should produce same hash
        assertEquals(hash, Utils.calculateSHA256(input));
        
        // Different input should produce different hash
        assertNotEquals(hash, Utils.calculateSHA256("Different input"));
        
        // Test known hash
        String knownInput = "test";
        String expectedHash = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08";
        assertEquals(expectedHash, Utils.calculateSHA256(knownInput));
    }

    @Test
    @DisplayName("Test random data generation")
    void testGenerateRandomData() {
        int size = 10;
        List<Utils.Person> people = Utils.generateRandomData(size);
        
        assertEquals(size, people.size());
        
        // Check that all people have valid properties
        for (Utils.Person person : people) {
            assertTrue(person.getId() > 0);
            assertNotNull(person.getName());
            assertTrue(person.getAge() >= 18 && person.getAge() <= 65);
            assertTrue(person.getScore() >= 0 && person.getScore() <= 100);
        }
    }

    @Test
    @DisplayName("Test groupBy functionality")
    void testGroupBy() {
        List<Utils.Person> people = Arrays.asList(
            new Utils.Person(1, "Alice", 25, 85.5),
            new Utils.Person(2, "Bob", 35, 92.0),
            new Utils.Person(3, "Charlie", 25, 78.3)
        );
        
        Map<Integer, List<Utils.Person>> grouped = Utils.groupBy(people, Utils.Person::getAge);
        
        assertEquals(2, grouped.size());
        assertEquals(2, grouped.get(25).size());
        assertEquals(1, grouped.get(35).size());
    }

    @Test
    @DisplayName("Test statistics calculation")
    void testCalculateStatistics() {
        List<Double> numbers = Arrays.asList(1.0, 2.0, 3.0, 4.0, 5.0);
        Utils.Statistics stats = Utils.calculateStatistics(numbers);
        
        assertEquals(5, stats.getCount());
        assertEquals(15.0, stats.getSum(), 0.001);
        assertEquals(3.0, stats.getAverage(), 0.001);
        assertEquals(1.0, stats.getMin(), 0.001);
        assertEquals(5.0, stats.getMax(), 0.001);
        
        // Test empty list
        Utils.Statistics emptyStats = Utils.calculateStatistics(new ArrayList<>());
        assertEquals(0, emptyStats.getCount());
        assertEquals(0.0, emptyStats.getSum(), 0.001);
    }

    @Test
    @DisplayName("Test async processing")
    void testProcessAsync() throws ExecutionException, InterruptedException {
        String input = "test input";
        CompletableFuture<String> future = Utils.processAsync(input, 100);
        
        String result = future.get();
        assertTrue(result.contains("Processed: " + input));
        assertTrue(result.contains("at"));
    }

    @Test
    @DisplayName("Test Person class")
    void testPersonClass() {
        Utils.Person person1 = new Utils.Person(1, "Alice", 30, 85.5);
        Utils.Person person2 = new Utils.Person(1, "Bob", 25, 90.0);
        Utils.Person person3 = new Utils.Person(2, "Charlie", 30, 85.5);
        
        // Test equality (based on ID)
        assertEquals(person1, person2);
        assertNotEquals(person1, person3);
        
        // Test getters
        assertEquals(1, person1.getId());
        assertEquals("Alice", person1.getName());
        assertEquals(30, person1.getAge());
        assertEquals(85.5, person1.getScore(), 0.001);
        
        // Test toString
        String str = person1.toString();
        assertTrue(str.contains("Alice"));
        assertTrue(str.contains("30"));
        assertTrue(str.contains("85.5"));
    }

    @Test
    @DisplayName("Test Statistics class")
    void testStatisticsClass() {
        Utils.Statistics stats = new Utils.Statistics(5, 15.0, 3.0, 1.0, 5.0);
        
        assertEquals(5, stats.getCount());
        assertEquals(15.0, stats.getSum(), 0.001);
        assertEquals(3.0, stats.getAverage(), 0.001);
        assertEquals(1.0, stats.getMin(), 0.001);
        assertEquals(5.0, stats.getMax(), 0.001);
        
        // Test toString
        String str = stats.toString();
        assertTrue(str.contains("count=5"));
        assertTrue(str.contains("sum=15.00"));
        assertTrue(str.contains("avg=3.00"));
    }

    @Test
    @DisplayName("Test UtilsException")
    void testUtilsException() {
        Utils.UtilsException exception1 = new Utils.UtilsException("Test message");
        assertEquals("Test message", exception1.getMessage());
        
        RuntimeException cause = new RuntimeException("Cause");
        Utils.UtilsException exception2 = new Utils.UtilsException("Test with cause", cause);
        assertEquals("Test with cause", exception2.getMessage());
        assertEquals(cause, exception2.getCause());
    }
}
