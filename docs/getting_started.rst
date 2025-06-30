Getting Started
===============

This guide will help you set up and start using the Polyglot Development Toolkit.

Prerequisites
-------------

* Python 3.8 or higher
* Node.js 18 or higher
* Java 17 or higher
* Git

Installation
------------

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/beslagicadin/polyglot-dev-toolkit.git
   cd polyglot-dev-toolkit

2. Set up Python environment:

.. code-block:: bash

   # Create virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt

3. Set up JavaScript environment:

.. code-block:: bash

   npm install

4. Set up Java environment:

.. code-block:: bash

   # Compile Java sources
   mvn compile

Running Tests
-------------

Python Tests
~~~~~~~~~~~~

.. code-block:: bash

   # Run all Python tests
   pytest tests/python/
   
   # Run with coverage
   pytest tests/python/ --cov=src/python --cov-report=html

JavaScript Tests
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Run all JavaScript tests
   npm test
   
   # Run with coverage
   npm run test:coverage

Java Tests
~~~~~~~~~~

.. code-block:: bash

   # Run all Java tests
   mvn test
   
   # Run tests with coverage
   mvn test jacoco:report

Quick Examples
--------------

Python
~~~~~~

.. code-block:: python

   from src.python.utils import FileUtils, DataUtils
   
   # File operations
   file_utils = FileUtils()
   files = file_utils.find_duplicates('/path/to/directory')
   
   # Data processing
   data_utils = DataUtils()
   json_data = data_utils.csv_to_json('data.csv')

JavaScript
~~~~~~~~~~

.. code-block:: javascript

   const { FileUtils, DataUtils } = require('./src/javascript/utils');
   
   // File operations
   const fileUtils = new FileUtils();
   const files = await fileUtils.findDuplicates('/path/to/directory');
   
   // Data processing
   const dataUtils = new DataUtils();
   const jsonData = dataUtils.csvToJson('data.csv');

Java
~~~~

.. code-block:: java

   import src.java.Utils;
   
   // File operations
   List<String> duplicates = Utils.findDuplicates("/path/to/directory");
   
   // Data processing
   String jsonData = Utils.csvToJson("data.csv");

Development Setup
-----------------

For active development, consider setting up:

1. **IDE Configuration**: Import project into your preferred IDE
2. **Pre-commit Hooks**: Install pre-commit hooks for code quality
3. **Environment Variables**: Set up any required environment variables
4. **Database Setup**: If using database features, configure connections

.. code-block:: bash

   # Install pre-commit hooks
   pre-commit install
   
   # Run quality checks
   ./quality_check.sh
