/**
 * JavaScript Utilities Module
 * A collection of useful utilities for web development, API handling, and automation.
 * 
 * Author: Adin Bešlagić
 * Email: beslagicadin@gmail.com
 */

// DOM Utilities
class DOMUtils {
    /**
     * Create an element with specified attributes and content
     * @param {string} tag - HTML tag name
     * @param {Object} attributes - Element attributes
     * @param {string|Node} content - Element content
     * @returns {HTMLElement} Created element
     */
    static createElement(tag, attributes = {}, content = '') {
        const element = document.createElement(tag);
        
        // Set attributes
        Object.entries(attributes).forEach(([key, value]) => {
            if (key === 'className') {
                element.className = value;
            } else if (key === 'style' && typeof value === 'object') {
                Object.assign(element.style, value);
            } else {
                element.setAttribute(key, value);
            }
        });
        
        // Set content
        if (typeof content === 'string') {
            element.innerHTML = content;
        } else if (content instanceof Node) {
            element.appendChild(content);
        }
        
        return element;
    }
    
    /**
     * Add event listener with automatic cleanup
     * @param {HTMLElement} element - Target element
     * @param {string} event - Event type
     * @param {Function} handler - Event handler
     * @param {Object} options - Event options
     * @returns {Function} Cleanup function
     */
    static addEventListenerWithCleanup(element, event, handler, options = {}) {
        element.addEventListener(event, handler, options);
        
        return () => {
            element.removeEventListener(event, handler, options);
        };
    }
    
    /**
     * Wait for element to appear in DOM
     * @param {string} selector - CSS selector
     * @param {number} timeout - Timeout in milliseconds
     * @returns {Promise<HTMLElement>} Found element
     */
    static waitForElement(selector, timeout = 5000) {
        return new Promise((resolve, reject) => {
            const element = document.querySelector(selector);
            if (element) {
                resolve(element);
                return;
            }
            
            const observer = new MutationObserver(() => {
                const element = document.querySelector(selector);
                if (element) {
                    observer.disconnect();
                    resolve(element);
                }
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
            
            setTimeout(() => {
                observer.disconnect();
                reject(new Error(`Element ${selector} not found within ${timeout}ms`));
            }, timeout);
        });
    }
}

// API Utilities
class APIClient {
    constructor(baseURL = '', defaultHeaders = {}) {
        this.baseURL = baseURL;
        this.defaultHeaders = {
            'Content-Type': 'application/json',
            ...defaultHeaders
        };
    }
    
    /**
     * Make HTTP request
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Request options
     * @returns {Promise<Object>} Response data
     */
    async request(endpoint, options = {}) {
        const url = this.baseURL + endpoint;
        const config = {
            headers: { ...this.defaultHeaders, ...options.headers },
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            } else {
                return await response.text();
            }
        } catch (error) {
            console.error('API Request failed:', error);
            throw error;
        }
    }
    
    /**
     * GET request
     * @param {string} endpoint - API endpoint
     * @param {Object} headers - Additional headers
     * @returns {Promise<Object>} Response data
     */
    async get(endpoint, headers = {}) {
        return this.request(endpoint, { method: 'GET', headers });
    }
    
    /**
     * POST request
     * @param {string} endpoint - API endpoint
     * @param {Object} data - Request body
     * @param {Object} headers - Additional headers
     * @returns {Promise<Object>} Response data
     */
    async post(endpoint, data = {}, headers = {}) {
        return this.request(endpoint, {
            method: 'POST',
            headers,
            body: JSON.stringify(data)
        });
    }
    
    /**
     * PUT request
     * @param {string} endpoint - API endpoint
     * @param {Object} data - Request body
     * @param {Object} headers - Additional headers
     * @returns {Promise<Object>} Response data
     */
    async put(endpoint, data = {}, headers = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            headers,
            body: JSON.stringify(data)
        });
    }
    
    /**
     * DELETE request
     * @param {string} endpoint - API endpoint
     * @param {Object} headers - Additional headers
     * @returns {Promise<Object>} Response data
     */
    async delete(endpoint, headers = {}) {
        return this.request(endpoint, { method: 'DELETE', headers });
    }
}

// Data Utilities
class DataUtils {
    /**
     * Deep clone an object
     * @param {Object} obj - Object to clone
     * @returns {Object} Cloned object
     */
    static deepClone(obj) {
        if (obj === null || typeof obj !== 'object') {
            return obj;
        }
        
        if (obj instanceof Date) {
            return new Date(obj.getTime());
        }
        
        if (obj instanceof Array) {
            return obj.map(item => DataUtils.deepClone(item));
        }
        
        const cloned = {};
        Object.keys(obj).forEach(key => {
            cloned[key] = DataUtils.deepClone(obj[key]);
        });
        
        return cloned;
    }
    
    /**
     * Debounce function calls
     * @param {Function} func - Function to debounce
     * @param {number} delay - Delay in milliseconds
     * @returns {Function} Debounced function
     */
    static debounce(func, delay) {
        let timeoutId;
        
        return function(...args) {
            const context = this;
            
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => {
                func.apply(context, args);
            }, delay);
        };
    }
    
    /**
     * Throttle function calls
     * @param {Function} func - Function to throttle
     * @param {number} limit - Time limit in milliseconds
     * @returns {Function} Throttled function
     */
    static throttle(func, limit) {
        let inThrottle;
        
        return function(...args) {
            const context = this;
            
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                
                setTimeout(() => {
                    inThrottle = false;
                }, limit);
            }
        };
    }
    
    /**
     * Group array of objects by key
     * @param {Array} array - Array to group
     * @param {string} key - Key to group by
     * @returns {Object} Grouped object
     */
    static groupBy(array, key) {
        return array.reduce((groups, item) => {
            const group = item[key];
            groups[group] = groups[group] || [];
            groups[group].push(item);
            return groups;
        }, {});
    }
    
    /**
     * Remove duplicates from array
     * @param {Array} array - Array with potential duplicates
     * @param {string} key - Key to check for uniqueness (for objects)
     * @returns {Array} Array without duplicates
     */
    static removeDuplicates(array, key = null) {
        if (key) {
            const seen = new Set();
            return array.filter(item => {
                const value = item[key];
                if (seen.has(value)) {
                    return false;
                }
                seen.add(value);
                return true;
            });
        }
        
        return [...new Set(array)];
    }
}

// Validation Utilities
class ValidationUtils {
    /**
     * Validate email address
     * @param {string} email - Email to validate
     * @returns {boolean} True if valid
     */
    static isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    /**
     * Validate URL
     * @param {string} url - URL to validate
     * @returns {boolean} True if valid
     */
    static isValidURL(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }
    
    /**
     * Validate phone number (basic)
     * @param {string} phone - Phone number to validate
     * @returns {boolean} True if valid
     */
    static isValidPhone(phone) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
    }
    
    /**
     * Validate required fields in object
     * @param {Object} obj - Object to validate
     * @param {Array} requiredFields - Array of required field names
     * @returns {Array} Array of missing fields
     */
    static validateRequiredFields(obj, requiredFields) {
        return requiredFields.filter(field => {
            const value = obj[field];
            return value === undefined || value === null || value === '';
        });
    }
}

// Storage Utilities
class StorageUtils {
    /**
     * Set item in localStorage with JSON serialization
     * @param {string} key - Storage key
     * @param {*} value - Value to store
     */
    static setItem(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            console.error('Failed to set localStorage item:', error);
        }
    }
    
    /**
     * Get item from localStorage with JSON deserialization
     * @param {string} key - Storage key
     * @param {*} defaultValue - Default value if key not found
     * @returns {*} Stored value or default
     */
    static getItem(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Failed to get localStorage item:', error);
            return defaultValue;
        }
    }
    
    /**
     * Remove item from localStorage
     * @param {string} key - Storage key
     */
    static removeItem(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.error('Failed to remove localStorage item:', error);
        }
    }
    
    /**
     * Clear all localStorage
     */
    static clear() {
        try {
            localStorage.clear();
        } catch (error) {
            console.error('Failed to clear localStorage:', error);
        }
    }
}

// Date Utilities
class DateUtils {
    /**
     * Format date to string
     * @param {Date} date - Date to format
     * @param {string} format - Format string (YYYY-MM-DD, DD/MM/YYYY, etc.)
     * @returns {string} Formatted date
     */
    static formatDate(date, format = 'YYYY-MM-DD') {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        
        return format
            .replace('YYYY', year)
            .replace('MM', month)
            .replace('DD', day);
    }
    
    /**
     * Get relative time (e.g., "2 hours ago")
     * @param {Date} date - Date to compare
     * @returns {string} Relative time string
     */
    static getRelativeTime(date) {
        const now = new Date();
        const diff = now - date;
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        
        if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
        if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        return 'Just now';
    }
    
    /**
     * Add days to date
     * @param {Date} date - Base date
     * @param {number} days - Days to add
     * @returns {Date} New date
     */
    static addDays(date, days) {
        const result = new Date(date);
        result.setDate(result.getDate() + days);
        return result;
    }
    
    /**
     * Check if date is today
     * @param {Date} date - Date to check
     * @returns {boolean} True if today
     */
    static isToday(date) {
        const today = new Date();
        return date.toDateString() === today.toDateString();
    }
}

// Performance Utilities
class PerformanceUtils {
    /**
     * Measure function execution time
     * @param {Function} func - Function to measure
     * @param {...*} args - Function arguments
     * @returns {Object} Result and execution time
     */
    static async measureTime(func, ...args) {
        const start = performance.now();
        const result = await func(...args);
        const end = performance.now();
        
        return {
            result,
            executionTime: end - start,
            executionTimeFormatted: `${(end - start).toFixed(2)}ms`
        };
    }
    
    /**
     * Create a simple profiler
     * @param {string} name - Profiler name
     * @returns {Object} Profiler object
     */
    static createProfiler(name) {
        const marks = {};
        
        return {
            mark(label) {
                marks[label] = performance.now();
            },
            
            measure(startLabel, endLabel = null) {
                const start = marks[startLabel];
                const end = endLabel ? marks[endLabel] : performance.now();
                
                if (start === undefined) {
                    console.error(`Mark '${startLabel}' not found`);
                    return null;
                }
                
                const duration = end - start;
                console.log(`${name} - ${startLabel}${endLabel ? ` to ${endLabel}` : ''}: ${duration.toFixed(2)}ms`);
                return duration;
            }
        };
    }
}

// Export utilities for Node.js environment
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        DOMUtils,
        APIClient,
        DataUtils,
        ValidationUtils,
        StorageUtils,
        DateUtils,
        PerformanceUtils
    };
}

// Example usage and demo
function demonstrateUtilities() {
    console.log('JavaScript Utilities Demo');
    console.log('=========================\n');
    
    // Data utilities demo
    const sampleData = [
        { id: 1, name: 'Alice', department: 'Engineering' },
        { id: 2, name: 'Bob', department: 'Marketing' },
        { id: 3, name: 'Charlie', department: 'Engineering' },
        { id: 4, name: 'Diana', department: 'Marketing' }
    ];
    
    console.log('1. Data Utils Demo:');
    const grouped = DataUtils.groupBy(sampleData, 'department');
    console.log('Grouped by department:', grouped);
    
    // Validation demo
    console.log('\n2. Validation Demo:');
    console.log('Email validation:', ValidationUtils.isValidEmail('test@example.com'));
    console.log('URL validation:', ValidationUtils.isValidURL('https://github.com'));
    
    // Date utilities demo
    console.log('\n3. Date Utils Demo:');
    const now = new Date();
    console.log('Formatted date:', DateUtils.formatDate(now));
    console.log('Is today:', DateUtils.isToday(now));
    
    // Performance demo
    console.log('\n4. Performance Demo:');
    const profiler = PerformanceUtils.createProfiler('Demo');
    profiler.mark('start');
    
    // Simulate some work
    setTimeout(() => {
        profiler.mark('end');
        profiler.measure('start', 'end');
    }, 100);
    
    console.log('Demo completed!');
}

// Run demo if in browser environment
if (typeof window !== 'undefined') {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', demonstrateUtilities);
    } else {
        demonstrateUtilities();
    }
}

/**
 * Utility functions for the GitHub Profile Enhancement Project
 * 
 * This module contains various utility functions demonstrating JavaScript best practices.
 */

/**
 * Calculate the nth Fibonacci number using dynamic programming
 * @param {number} n - Position in Fibonacci sequence
 * @returns {number} The nth Fibonacci number
 * @throws {Error} If n is negative
 */
function calculateFibonacci(n) {
    if (n < 0) {
        throw new Error('n must be non-negative');
    }
    
    if (n <= 1) {
        return n;
    }
    
    let a = 0, b = 1;
    for (let i = 2; i <= n; i++) {
        [a, b] = [b, a + b];
    }
    
    return b;
}

/**
 * Check if a number is prime
 * @param {number} num - Number to check
 * @returns {boolean} True if prime, false otherwise
 */
function isPrime(num) {
    if (num < 2) {
        return false;
    }
    
    for (let i = 2; i <= Math.sqrt(num); i++) {
        if (num % i === 0) {
            return false;
        }
    }
    
    return true;
}

/**
 * Generate random data for testing purposes
 * @param {number} size - Number of records to generate
 * @returns {Array<Object>} Array of random data records
 */
function generateRandomData(size = 10) {
    const names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'];
    
    const data = [];
    for (let i = 0; i < size; i++) {
        const record = {
            id: i + 1,
            name: names[Math.floor(Math.random() * names.length)],
            age: Math.floor(Math.random() * (65 - 18 + 1)) + 18,
            score: Math.round(Math.random() * 100 * 100) / 100,
            timestamp: new Date().toISOString(),
            active: Math.random() > 0.5
        };
        data.push(record);
    }
    
    return data;
}

/**
 * Sort an array of objects by a specified key
 * @param {Array<Object>} data - Data to sort
 * @param {string} key - Key to sort by
 * @param {boolean} reverse - Sort in descending order if true
 * @returns {Array<Object>} Sorted data
 */
function sortData(data, key, reverse = false) {
    const sorted = [...data].sort((a, b) => {
        const aVal = a[key] || 0;
        const bVal = b[key] || 0;
        
        if (aVal < bVal) return reverse ? 1 : -1;
        if (aVal > bVal) return reverse ? -1 : 1;
        return 0;
    });
    
    return sorted;
}

/**
 * Class for processing data with various operations
 */
class DataProcessor {
    constructor() {
        this.data = [];
    }
    
    /**
     * Add a data item to the processor
     * @param {Object} item - Data item to add
     */
    addData(item) {
        this.data.push(item);
    }
    
    /**
     * Filter data by age range
     * @param {number} minAge - Minimum age
     * @param {number} maxAge - Maximum age
     * @returns {Array<Object>} Filtered data
     */
    filterByAge(minAge, maxAge) {
        return this.data.filter(item => {
            const age = item.age || 0;
            return age >= minAge && age <= maxAge;
        });
    }
    
    /**
     * Calculate basic statistics for numerical fields
     * @returns {Object} Statistics object
     */
    getStatistics() {
        if (this.data.length === 0) {
            return {};
        }
        
        const ages = this.data.map(item => item.age || 0);
        const scores = this.data.map(item => item.score || 0);
        
        return {
            totalRecords: this.data.length,
            avgAge: ages.reduce((sum, age) => sum + age, 0) / ages.length,
            avgScore: scores.reduce((sum, score) => sum + score, 0) / scores.length,
            minAge: Math.min(...ages),
            maxAge: Math.max(...ages),
            minScore: Math.min(...scores),
            maxScore: Math.max(...scores)
        };
    }
}

/**
 * Async function to simulate API call
 * @param {string} url - URL to fetch
 * @param {number} delay - Delay in milliseconds
 * @returns {Promise<Object>} Mock response
 */
async function mockApiCall(url, delay = 1000) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({
                status: 200,
                url: url,
                data: {
                    message: 'Success',
                    timestamp: new Date().toISOString(),
                    randomValue: Math.random()
                }
            });
        }, delay);
    });
}

// Export functions for Node.js environment
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        calculateFibonacci,
        isPrime,
        generateRandomData,
        sortData,
        DataProcessor,
        mockApiCall
    };
}

// Example usage if running directly
if (typeof window === 'undefined' && require.main === module) {
    console.log('Fibonacci(10):', calculateFibonacci(10));
    console.log('Is 17 prime?', isPrime(17));
    
    // Generate and process some data
    const processor = new DataProcessor();
    const sampleData = generateRandomData(5);
    
    sampleData.forEach(item => processor.addData(item));
    
    console.log('\nGenerated data:');
    sampleData.forEach(item => console.log('  ', item));
    
    console.log('\nStatistics:', processor.getStatistics());
    
    // Test async function
    mockApiCall('https://api.example.com/data', 500)
        .then(response => console.log('\nMock API Response:', response))
        .catch(error => console.error('Error:', error));
}
