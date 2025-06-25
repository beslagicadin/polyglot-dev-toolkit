# Contributing to Polyglot Dev Toolkit

🎉 Thank you for considering contributing to Polyglot Dev Toolkit! Your contributions help make this project a valuable resource for the developer community.

## 🚀 How to Contribute

### 1. Fork & Clone
```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/polyglot-dev-toolkit.git
cd polyglot-dev-toolkit
```

### 2. Set Up Development Environment
```bash
# Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# JavaScript environment
npm install

# Verify Java setup
javac -version
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number
```

## 📝 Development Guidelines

### Code Style

#### Python
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write comprehensive docstrings
- Use `black` for code formatting
- Use `isort` for import sorting

```bash
# Format Python code
black src/python/
isort src/python/

# Check style
flake8 src/python/
mypy src/python/
```

#### JavaScript
- Follow modern ES6+ standards
- Use JSDoc for function documentation
- Use consistent naming conventions
- Use Prettier for code formatting

```bash
# Format JavaScript code
npm run format

# Check style
npm run lint
```

#### Java
- Follow Oracle Java Code Conventions
- Use meaningful variable and method names
- Write comprehensive Javadoc comments
- Follow standard Java formatting

### Testing Requirements

All contributions must include appropriate tests:

#### Python Tests
```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/python --cov-report=html

# Test specific module
pytest tests/test_python_utils.py::TestFileManager -v
```

#### JavaScript Tests
```bash
# Run tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test
npm test -- --grep "DataUtils"
```

#### Java Tests
```bash
# Compile and run tests
javac -cp src/java tests/*.java
java -cp ".:src/java:tests" org.junit.runner.JUnitCore TestJavaUtils
```

### Documentation

- Update README.md if adding new features
- Add examples to the `examples/` directory
- Update API documentation in `docs/`
- Include code comments for complex logic

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear title** describing the issue
2. **Steps to reproduce** the bug
3. **Expected behavior** vs actual behavior
4. **Environment details** (OS, Python/Node/Java versions)
5. **Code samples** if applicable
6. **Error messages** or stack traces

Use this template:
```markdown
**Bug Description:**
A clear description of the bug.

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: [e.g., macOS 12.0, Ubuntu 20.04]
- Python: [e.g., 3.9.7]
- Node.js: [e.g., 16.14.0]
- Java: [e.g., OpenJDK 11.0.12]
```

## ✨ Feature Requests

When suggesting features:

1. **Check existing issues** to avoid duplicates
2. **Describe the use case** and problem it solves
3. **Provide examples** of how it would be used
4. **Consider the scope** - does it fit the project goals?

## 📋 Pull Request Process

### Before Submitting
- [ ] Code follows style guidelines for the language
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated if needed
- [ ] Commit messages are clear and descriptive

### Pull Request Checklist
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] All existing tests pass
- [ ] New tests added and passing
- [ ] Manual testing completed

## Documentation
- [ ] README updated if needed
- [ ] Code comments added
- [ ] Examples updated if needed
```

### Commit Message Format
Use conventional commit format:
```
type(scope): brief description

Detailed explanation if needed

- Change 1
- Change 2
```

Examples:
- `feat(python): add file compression utilities`
- `fix(javascript): handle edge case in data validation`
- `docs: update installation instructions`
- `test(java): add unit tests for Statistics class`

## 🏆 Recognition

Contributors will be:
- Listed in the project's contributors section
- Mentioned in release notes for significant contributions
- Given appropriate credit in documentation

## 🤝 Code of Conduct

### Our Pledge
We are committed to making participation in this project a harassment-free experience for everyone.

### Standards
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Enforcement
Project maintainers will remove, edit, or reject comments, commits, code, issues, and other contributions that do not align with this Code of Conduct.

## 🎯 Development Workflow

1. **Issue Discussion**: Discuss significant changes in issues first
2. **Development**: Write code following guidelines
3. **Testing**: Ensure all tests pass
4. **Documentation**: Update relevant documentation
5. **Review**: Submit PR and address feedback
6. **Merge**: Maintainers will merge approved PRs

## 📞 Getting Help

- **General Questions**: Open a GitHub Discussion
- **Bug Reports**: Create a GitHub Issue
- **Security Issues**: Email beslagicadin@gmail.com
- **Feature Ideas**: Open a GitHub Issue with feature request template

## 🙏 Thank You

Your contributions make this project better for everyone. Whether it's fixing a typo, adding a feature, or improving documentation - every contribution matters!

Happy coding! 🚀
