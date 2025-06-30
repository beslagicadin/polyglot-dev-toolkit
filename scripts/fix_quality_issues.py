#!/usr/bin/env python3
"""
Script to fix common code quality issues that cause SonarCloud failures.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}")
        print(f"Error: {e.stderr}")
        return e


def fix_python_quality_issues():
    """Fix Python code quality issues."""
    print("Fixing Python code quality issues...")
    
    # Check if black is available
    try:
        run_command("black --version")
        print("Running black formatter...")
        run_command("black src/python/ tests/python/")
    except:
        print("Black not available, skipping formatting")
    
    # Check if isort is available
    try:
        run_command("isort --version")
        print("Running isort...")
        run_command("isort src/python/ tests/python/")
    except:
        print("isort not available, skipping import sorting")


def fix_javascript_quality_issues():
    """Fix JavaScript code quality issues."""
    print("Fixing JavaScript code quality issues...")
    
    # Check if prettier is available
    try:
        run_command("npx prettier --version")
        print("Running prettier...")
        run_command("npx prettier --write src/javascript/")
    except:
        print("Prettier not available, skipping formatting")
    
    # Check if eslint is available
    try:
        run_command("npx eslint --version")
        print("Running eslint...")
        run_command("npx eslint src/javascript/ --fix", check=False)
    except:
        print("ESLint not available, skipping linting")


def check_java_quality():
    """Check Java code quality."""
    print("Checking Java code quality...")
    
    try:
        run_command("mvn checkstyle:check")
        print("Java checkstyle passed")
    except:
        print("Java checkstyle issues detected")


def main():
    """Main function to run quality fixes."""
    print("Running code quality fixes...")
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Fix Python issues
    fix_python_quality_issues()
    
    # Fix JavaScript issues
    fix_javascript_quality_issues()
    
    # Check Java quality
    check_java_quality()
    
    print("\nQuality fixes completed!")
    
    # Provide recommendations
    print("\nRecommendations for improving SonarCloud Quality Gate:")
    print("1. Remove code duplication")
    print("2. Reduce cognitive complexity in methods")
    print("3. Add proper error handling")
    print("4. Remove unused imports and variables")
    print("5. Add unit tests for uncovered code")
    print("6. Fix security hotspots")


if __name__ == "__main__":
    main()
