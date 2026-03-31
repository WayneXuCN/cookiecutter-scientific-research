---
paths:
  - "tests/**/*"
  - "**/*_test.py"
  - "**/test_*.py"
---

# Testing Guidelines

## Test Organization

- Place tests in `tests/` directory
- Mirror source structure: `src/module.py` → `tests/test_module.py`

## Running Tests

```bash
# Run all tests
make test
# or
pytest

# Run specific test file
pytest tests/test_module.py

# Run with coverage
pytest --cov=src
```

## Test Style

- Use descriptive test names: `test_compute_probability_returns_zero_for_empty_input`
- One assertion per test when practical
- Use fixtures for common setup
