const js = require('@eslint/js');

module.exports = [
  {
    files: ['src/javascript/**/*.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'script',  // Use script instead of module for Node.js compatibility
      globals: {
        console: 'readonly',
        process: 'readonly',
        Buffer: 'readonly',
        __dirname: 'readonly',
        __filename: 'readonly',
        exports: 'writable',
        module: 'writable',
        require: 'readonly',
        global: 'readonly',
        setTimeout: 'readonly',
        clearTimeout: 'readonly',
        setInterval: 'readonly',
        clearInterval: 'readonly',
        document: 'readonly',
        window: 'readonly',
        fetch: 'readonly',
        MutationObserver: 'readonly',
        Node: 'readonly',
        URL: 'readonly',
        localStorage: 'readonly',
        performance: 'readonly'
      }
    },
    rules: {
      'no-unused-vars': 'error',
      'no-undef': 'error',
      'semi': ['error', 'always'],
      'quotes': ['error', 'single'],
      'indent': ['error', 2],
      'no-trailing-spaces': 'error',
      'eol-last': 'error',
      'constructor-super': 'off'  // Disable problematic rule
    }
  }
];
