# 🚀 Polyglot Dev Toolkit

[![CI/CD Pipeline](https://github.com/beslagicadin/polyglot-dev-toolkit/workflows/Continuous%20Integration/badge.svg)](https://github.com/beslagicadin/polyglot-dev-toolkit/actions)
[![Code Coverage](https://codecov.io/gh/beslagicadin/polyglot-dev-toolkit/branch/master/graph/badge.svg)](https://codecov.io/gh/beslagicadin/polyglot-dev-toolkit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Java](https://img.shields.io/badge/Java-17%2B-red)](https://openjdk.java.net/)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=beslagicadin_polyglot-dev-toolkit&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=beslagicadin_polyglot-dev-toolkit)

> **A comprehensive, production-ready toolkit showcasing modern development practices across Python, JavaScript, and Java ecosystems.**

Polyglot Dev Toolkit is a curated collection of utilities, algorithms, and best practices that demonstrates professional software development across multiple programming languages. Perfect for developers looking to learn cross-language patterns, contribute to open source, or use battle-tested utilities in their projects.

## ✨ What's Inside

### 🐍 Python Ecosystem
- **File Management**: Organize files, detect duplicates, hash calculations
- **Data Processing**: CSV/JSON conversion, validation, transformation
- **System Monitoring**: Resource usage, health checks, performance metrics
- **Web Scraping**: HTTP clients, URL validation, content extraction
- **Algorithms**: Fibonacci, prime checking, sorting, statistics

### 🌐 JavaScript Ecosystem
- **DOM Utilities**: Element creation, event handling, async operations
- **API Client**: RESTful requests, response handling, error management
- **Data Utils**: Deep cloning, debouncing, throttling, grouping
- **Validation**: Email, URL, phone validation, form processing
- **Performance**: Execution timing, profiling, optimization tools

### ☕ Java Ecosystem
- **Data Structures**: Generic collections, search algorithms
- **Concurrency**: Async operations, CompletableFuture patterns
- **Cryptography**: SHA-256 hashing, security utilities
- **Statistics**: Mathematical operations, data analysis
- **Streams**: Modern Java 8+ functional programming

## 🏗️ Architecture

```
polyglot-dev-toolkit/
├── 📁 src/                    # Source code
│   ├── 🐍 python/             # Python utilities
│   │   └── utils.py           # Core Python modules
│   ├── 🌐 javascript/         # JavaScript utilities  
│   │   └── utils.js           # Modern JS/Node.js modules
│   └── ☕ java/               # Java utilities
│       └── Utils.java         # Object-oriented Java classes
├── 🧪 tests/                  # Test suites
│   ├── test_python_utils.py   # Python unit tests
│   ├── test_javascript.spec.js # JavaScript tests
│   └── TestJavaUtils.java     # Java test cases
├── 📚 docs/                   # Documentation
│   ├── README.md              # Detailed docs
│   ├── API.md                 # API reference
│   └── CONTRIBUTING.md        # Contribution guide
├── 🔧 scripts/                # Automation scripts
│   ├── performance_test.py    # Benchmarking tools
│   ├── setup.sh              # Environment setup
│   └── deploy.sh              # Deployment scripts
├── 🎯 examples/               # Usage examples
│   ├── python_examples.py     # Python demos
│   ├── javascript_examples.js # JavaScript demos
│   └── java_examples.java     # Java demos
├── ⚙️ .github/                # GitHub automation
│   └── workflows/             # CI/CD pipelines
│       ├── ci.yml             # Continuous integration
│       ├── release.yml        # Automated releases
│       └── security.yml       # Security scanning
└── 📦 config files            # Project configuration
    ├── requirements.txt       # Python dependencies
    ├── package.json          # Node.js configuration
    ├── pom.xml               # Maven configuration
    └── .gitignore            # Version control rules
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** for Python utilities
- **Node.js 18+** for JavaScript utilities
- **Java 11+** for Java utilities
- **Git** for version control

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/beslagicadin/polyglot-dev-toolkit.git
cd polyglot-dev-toolkit

# 2. Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Set up JavaScript environment
npm install

# 4. Verify Java installation
javac -version
java -version
```

### Running Examples

```bash
# Python examples
python examples/python_examples.py

# JavaScript examples (Node.js)
node examples/javascript_examples.js

# JavaScript examples (Browser)
open examples/index.html

# Java examples
javac -cp src/java src/java/*.java
java -cp src/java java.Utils
```

### Running Tests

```bash
# Run all tests
./scripts/run_tests.sh

# Individual language tests
pytest tests/ -v                    # Python
npm test                            # JavaScript
javac -cp src/java tests/*.java     # Java

# Performance benchmarks
python scripts/performance_test.py
```

## 📚 Documentation

Detailed documentation is available in the [docs](./docs) folder and on our [GitHub Pages site](https://beslagicadin.github.io/new-project/).

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](./CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 👨‍💻 Author

**Adin Bešlagić** - Software Engineer at Resonate d.o.o.
- GitHub: [@beslagicadin](https://github.com/beslagicadin)
- LinkedIn: [beslagicadin](https://www.linkedin.com/in/beslagicadin/)
- Portfolio: [beslagicadin.vercel.app](https://beslagicadin.vercel.app)

## 🏆 GitHub Achievements

This project is designed to help earn various GitHub achievements:
- ✅ First Repository
- ✅ First Commit
- ⏳ First Pull Request
- ⏳ First Issue
- ⏳ Quickdraw (Merged PR within 5 minutes)
- ⏳ YOLO (Merged PR without review)
- ⏳ Galaxy Brain (2 accepted answers)
- ⏳ Pull Shark (2 merged PRs)

## 📈 Project Stats

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/beslagicadin/polyglot-dev-toolkit)
![GitHub last commit](https://img.shields.io/github/last-commit/beslagicadin/polyglot-dev-toolkit)
![GitHub repo size](https://img.shields.io/github/repo-size/beslagicadin/polyglot-dev-toolkit)

---
*Last updated: Sat Jun 28 11:31:39 CEST 2025*
