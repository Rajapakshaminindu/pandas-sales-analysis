# Contributing to Pandas Sales Analysis

Thank you for your interest in contributing to **Pandas Sales Analysis**! We welcome all contributions from bug fixes and documentation improvements to new data visualization features.

## How to Contribute

1. **Fork the Repository**:
   Click the **Fork** button at the top right of this page.

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/pandas-sales-analysis.git
   cd pandas-sales-analysis
   ```

3. **Create a new branch**:
   ```bash
   git checkout -b feature/my-cool-feature
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Make your changes & run tests**:
   ```bash
   python -m pytest -v
   python pandas_sales_analysis.py
   ```

6. **Commit & Push**:
   ```bash
   git add .
   git commit -m "feat: Add new analysis feature"
   git push origin feature/my-cool-feature
   ```

7. **Open a Pull Request**:
   Go to the original repository on GitHub and open a Pull Request describing your changes.

## Code Standards
- Keep functions well-documented with docstrings and type hints.
- Write pytest tests for any new data processing logic in `tests/`.
- Ensure existing tests pass before submitting.
