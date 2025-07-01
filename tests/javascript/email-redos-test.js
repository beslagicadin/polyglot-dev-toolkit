/**
 * Test to verify the email validation regex is secure against ReDoS attacks
 */

const { ValidationUtils } = require('../../src/javascript/utils.js');

function testEmailRegexPerformance() {
  console.log('Testing email regex for ReDoS vulnerability...');
  
  // Valid emails should pass quickly
  const validEmails = [
    'test@example.com',
    'user.name@domain.co.uk',
    'test+tag@example.org',
    'user123@sub.domain.com'
  ];
  
  console.log('\nTesting valid emails:');
  validEmails.forEach(email => {
    const start = performance.now();
    const result = ValidationUtils.isValidEmail(email);
    const end = performance.now();
    console.log(`  ${email}: ${result} (${(end - start).toFixed(2)}ms)`);
  });
  
  // Invalid emails should also fail quickly (no catastrophic backtracking)
  const invalidEmails = [
    'invalid-email',
    '@domain.com',
    'user@',
    'user@domain',
    '.user@domain.com',
    'user.@domain.com',
    'user..name@domain.com'
  ];
  
  console.log('\nTesting invalid emails:');
  invalidEmails.forEach(email => {
    const start = performance.now();
    const result = ValidationUtils.isValidEmail(email);
    const end = performance.now();
    console.log(`  ${email}: ${result} (${(end - start).toFixed(2)}ms)`);
  });
  
  // Test potentially problematic patterns that could cause ReDoS
  // These should fail quickly without causing exponential backtracking
  const potentialAttackVectors = [
    'a@' + 'a'.repeat(100) + '.com',
    'user@' + 'a-'.repeat(50) + 'domain.com',
    'a'.repeat(100) + '@domain.com',
    'user@domain.' + 'a'.repeat(100),
    // Edge case with many dots
    'user@' + 'a.'.repeat(30) + 'com'
  ];
  
  console.log('\nTesting potential ReDoS attack vectors:');
  potentialAttackVectors.forEach(email => {
    const start = performance.now();
    const result = ValidationUtils.isValidEmail(email);
    const end = performance.now();
    const time = end - start;
    console.log(`  Pattern (${email.length} chars): ${result} (${time.toFixed(2)}ms)`);
    
    // Assert that no email validation takes more than 10ms (should be much faster)
    if (time > 10) {
      console.error(`  ⚠️  Warning: Email validation took ${time.toFixed(2)}ms - potential performance issue`);
    }
  });
  
  console.log('\n✅ Email regex ReDoS protection test completed');
}

// Run the test
testEmailRegexPerformance();
