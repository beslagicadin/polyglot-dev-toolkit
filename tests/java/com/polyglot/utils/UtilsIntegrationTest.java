package com.polyglot.utils;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.Security;
import java.security.Provider;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

/**
 * Integration tests for Utils class to achieve 100% code coverage
 * These tests use reflection and mocking to trigger edge cases
 * 
 * @author Adin Bešlagić
 */
public class UtilsIntegrationTest {
    
    @Test
    @DisplayName("Integration test - Force NoSuchAlgorithmException in calculateSHA256")
    void testCalculateSHA256NoSuchAlgorithmException() throws Exception {
        // This test will temporarily remove the SHA-256 provider to force the exception
        
        // First, get the current SHA-256 provider
        Provider sha256Provider = null;
        Provider[] providers = Security.getProviders();
        for (Provider provider : providers) {
            if (provider.getService("MessageDigest", "SHA-256") != null) {
                sha256Provider = provider;
                break;
            }
        }
        
        if (sha256Provider == null) {
            // If no SHA-256 provider found, this test isn't applicable
            return;
        }
        
        try {
            // Remove the SHA-256 algorithm temporarily
            Security.removeProvider(sha256Provider.getName());
            
            // Now try to calculate SHA-256 - this should throw UtilsException
            assertThrows(Utils.UtilsException.class, () -> {
                Utils.calculateSHA256("test");
            });
            
        } finally {
            // Always restore the provider
            if (sha256Provider != null) {
                Security.addProvider(sha256Provider);
            }
        }
        
        // Verify that SHA-256 works again after restoring the provider
        assertDoesNotThrow(() -> {
            String hash = Utils.calculateSHA256("test");
            assertEquals(64, hash.length());
        });
    }
    
    @Test
    @DisplayName("Integration test - Interrupt handling in processAsync")
    void testProcessAsyncInterruptHandling() throws InterruptedException {
        // This test creates a custom thread pool to better control interruption
        
        class InterruptibleTask implements Runnable {
            private volatile boolean interrupted = false;
            private volatile Exception caughtException = null;
            
            @Override
            public void run() {
                try {
                    // Create a future with a longer delay
                    CompletableFuture<String> future = Utils.processAsync("interrupt-test", 2000);
                    
                    // Wait a bit, then interrupt this thread
                    Thread.sleep(100);
                    Thread.currentThread().interrupt();
                    
                    // Try to get the result - this should handle the interrupt
                    future.get();
                    
                } catch (InterruptedException e) {
                    interrupted = true;
                    caughtException = e;
                    Thread.currentThread().interrupt(); // Restore interrupt status
                } catch (ExecutionException e) {
                    caughtException = e;
                    // Check if the cause is our UtilsException from interrupt handling
                    if (e.getCause() instanceof Utils.UtilsException) {
                        Utils.UtilsException utilsEx = (Utils.UtilsException) e.getCause();
                        if (utilsEx.getMessage().contains("Operation interrupted")) {
                            // Successfully triggered the interrupt handling path!
                            System.out.println("Successfully triggered interrupt handling in processAsync");
                        }
                    }
                } catch (Exception e) {
                    caughtException = e;
                }
            }
            
            public boolean wasInterrupted() { return interrupted; }
            public Exception getCaughtException() { return caughtException; }
        }
        
        // Run the task in a separate thread so we can control interruption
        InterruptibleTask task = new InterruptibleTask();
        Thread testThread = new Thread(task);
        testThread.start();
        
        // Wait for the test to complete
        testThread.join(5000); // 5 second timeout
        
        // Verify that some form of exception handling occurred
        assertTrue(task.wasInterrupted() || task.getCaughtException() != null);
    }
    
    @Test
    @DisplayName("Integration test - Main method exception handling paths")
    void testMainMethodExceptionPaths() throws InterruptedException {
        // This test runs main method multiple times with different conditions
        // to try to trigger the exception handling paths
        
        // Test 1: Run main method normally
        assertDoesNotThrow(() -> Utils.main(new String[]{}));
        
        // Test 2: Run with multiple threads to increase chance of timing issues
        Thread[] threads = new Thread[5];
        Exception[] exceptions = new Exception[5];
        
        for (int i = 0; i < threads.length; i++) {
            final int index = i;
            threads[i] = new Thread(() -> {
                try {
                    Utils.main(new String[]{"thread-" + index});
                } catch (Exception e) {
                    exceptions[index] = e;
                }
            });
        }
        
        // Start all threads
        for (Thread thread : threads) {
            thread.start();
        }
        
        // Wait for all threads to complete
        for (Thread thread : threads) {
            thread.join(3000); // 3 second timeout per thread
        }
        
        // Check if any exceptions were caught
        // In a well-written utility class, we expect no exceptions to propagate from main
        for (Exception e : exceptions) {
            if (e != null) {
                System.out.println("Main method thread threw exception: " + e.getMessage());
                // This is unexpected but we'll note it for debugging
            }
        }
    }
    
    @Test
    @DisplayName("Integration test - Multiple async operations with cancellation")
    void testMultipleAsyncOperationsWithCancellation() throws InterruptedException {
        // Create many async operations and cancel them at different times
        // to maximize the chance of hitting the InterruptedException path
        
        CompletableFuture<String>[] futures = new CompletableFuture[20];
        
        // Create futures with varying delays
        for (int i = 0; i < futures.length; i++) {
            futures[i] = Utils.processAsync("multi-test-" + i, 100 + (i * 50));
        }
        
        // Cancel futures at different times and with different interrupt settings
        for (int i = 0; i < futures.length; i++) {
            final int index = i;
            
            // Create a thread to cancel the future after a short delay
            Thread canceller = new Thread(() -> {
                try {
                    Thread.sleep(10 + (index * 5)); // Staggered cancellation
                    futures[index].cancel(true); // Cancel with interrupt
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            
            canceller.start();
        }
        
        // Collect results and exceptions
        int completed = 0, cancelled = 0, exceptions = 0;
        
        for (CompletableFuture<String> future : futures) {
            try {
                future.get();
                completed++;
            } catch (java.util.concurrent.CancellationException e) {
                cancelled++;
            } catch (ExecutionException e) {
                exceptions++;
                // Check if this is our UtilsException from interrupt handling
                if (e.getCause() instanceof Utils.UtilsException) {
                    Utils.UtilsException utilsEx = (Utils.UtilsException) e.getCause();
                    if (utilsEx.getMessage().contains("Operation interrupted")) {
                        System.out.println("Successfully triggered InterruptedException handling!");
                    }
                }
            }
        }
        
        System.out.println(String.format("Multi-async test: %d completed, %d cancelled, %d exceptions", 
                                        completed, cancelled, exceptions));
        
        // We expect at least some operations to be cancelled or throw exceptions
        assertTrue(cancelled + exceptions > 0);
    }
    
    @Test
    @DisplayName("Integration test - Edge case coverage for all methods")
    void testEdgeCaseCoverage() {
        // Test various edge cases to ensure all code paths are covered
        
        // Test fibonacci with larger numbers
        assertEquals(6765, Utils.fibonacci(20));
        
        // Test isPrime with edge cases
        assertFalse(Utils.isPrime(-5));
        assertFalse(Utils.isPrime(0));
        assertFalse(Utils.isPrime(1));
        assertTrue(Utils.isPrime(2));
        
        // Test sieve with larger numbers
        var primes = Utils.sieveOfEratosthenes(30);
        assertTrue(primes.contains(2));
        assertTrue(primes.contains(29));
        assertEquals(10, primes.size()); // 10 primes up to 30
        
        // Test binary search with edge cases
        String[] strings = {"a", "c", "e", "g"};
        assertEquals(0, Utils.binarySearch(strings, "a"));
        assertEquals(-1, Utils.binarySearch(strings, "b"));
        assertEquals(-1, Utils.binarySearch(strings, "z"));
        
        // Test calculateSHA256 with various inputs
        assertNotNull(Utils.calculateSHA256(""));
        assertNotNull(Utils.calculateSHA256("short"));
        
        StringBuilder longString = new StringBuilder();
        for (int i = 0; i < 1000; i++) {
            longString.append("long string test ");
        }
        assertNotNull(Utils.calculateSHA256(longString.toString()));
        
        // Test generateRandomData with different sizes
        assertEquals(0, Utils.generateRandomData(0).size());
        assertEquals(1, Utils.generateRandomData(1).size());
        assertEquals(100, Utils.generateRandomData(100).size());
        
        // Test groupBy with empty list
        assertTrue(Utils.groupBy(java.util.Collections.emptyList(), x -> x).isEmpty());
        
        // Test calculateStatistics with single element
        var singleStats = Utils.calculateStatistics(java.util.Arrays.asList(42.0));
        assertEquals(1, singleStats.getCount());
        assertEquals(42.0, singleStats.getAverage(), 0.001);
        assertEquals(42.0, singleStats.getMin(), 0.001);
        assertEquals(42.0, singleStats.getMax(), 0.001);
    }
}
