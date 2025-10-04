# Quick Start - Testing Guide

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run Tests

```bash
pytest --cov=. --cov-report=term-missing --cov-report=html
```

### 3. View Coverage

```bash
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

## 🎯 Common Commands

### Run All Tests (Fast)

```bash
pytest
```

### Run with Coverage Report

```bash
pytest --cov=. --cov-report=term-missing
```

### Run Specific Test File

```bash
pytest test/test_main.py
```

### Run Tests Matching Pattern

```bash
pytest -k "upload"  # Run tests with "upload" in name
```

### Verbose Output

```bash
pytest -v
```

### Stop at First Failure

```bash
pytest -x
```

### Run in Parallel (faster)

```bash
pip install pytest-xdist
pytest -n auto
```

## 🛠️ Using the Test Runner Script

```bash
./run_tests.sh              # Run all tests with coverage
./run_tests.sh quick        # Quick test run (no coverage)
./run_tests.sh coverage     # Generate and open coverage report
./run_tests.sh clean        # Clean test artifacts
./run_tests.sh help         # Show all options
```

## 📊 Coverage Target

**Goal: 100% Code Coverage**

Current modules:

- `main.py` - FastAPI application
- `controller/garbage_controller.py` - Classification endpoint
- `model/garbage_model.py` - Classification logic
- `faiss_helper.py` - FAISS operations
- `langchain_helper.py` - LLM integration
- `embeddings.py` - Data processing

## ✅ What's Tested

- ✅ All endpoints (`/upload/`, `/classify`)
- ✅ Request validation (Pydantic models)
- ✅ Error handling (400, 422, 500 errors)
- ✅ OpenAI API integration (mocked)
- ✅ Neo4j database operations (mocked)
- ✅ S3/R2 file uploads (mocked)
- ✅ FAISS similarity search (mocked)
- ✅ CSV data processing
- ✅ Edge cases (empty strings, None values, special characters)
- ✅ File I/O operations
- ✅ Classification logic (both Neo4j hit and LLM fallback)

## 📁 Test Files

```
backend/test/
├── conftest.py                 # Shared fixtures
├── test_main.py               # 15 tests - FastAPI endpoints
├── test_garbage_controller.py # 20 tests - Controller logic
├── test_garbage_model.py      # 17 tests - Classification model
├── test_faiss_helper.py       # 23 tests - FAISS operations
├── test_langchain_helper.py   # 21 tests - LangChain/LLM
└── test_embeddings.py         # 21 tests - Data processing
```

**Total: 117+ tests**

## 🔧 Troubleshooting

### Import Errors

```bash
# Make sure you're in the backend directory
cd backend
pytest
```

### Missing Dependencies

```bash
pip install -r requirements.txt
```

### Clean Cache

```bash
rm -rf .pytest_cache __pycache__ .coverage htmlcov
```

## 📚 Documentation

- **test/README.md** - Comprehensive testing guide
- **TEST_SUITE_SUMMARY.md** - Complete test suite overview
- **pytest.ini** - Test configuration
- **.coveragerc** - Coverage configuration

## 🎓 Learn More

- [pytest docs](https://docs.pytest.org/)
- [pytest-cov docs](https://pytest-cov.readthedocs.io/)
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)

## 💡 Tips

1. **Run tests before committing**

   ```bash
   pytest --cov=. --cov-fail-under=95
   ```

2. **Watch mode for development**

   ```bash
   pip install pytest-watch
   ptw -- --cov=. --cov-report=term-missing
   ```

3. **Test a specific function**

   ```bash
   pytest test/test_main.py::test_upload_endpoint_success
   ```

4. **See print statements**

   ```bash
   pytest -s  # Don't capture output
   ```

5. **Debug with pdb**
   ```bash
   pytest --pdb  # Drop into debugger on failure
   ```

## ⚡ Performance

- All tests use mocking (no external API calls)
- Typical run time: < 5 seconds for all tests
- Parallel execution supported with `pytest-xdist`

## 🎯 CI/CD Ready

```bash
# Run in CI mode with coverage threshold
pytest --cov=. --cov-report=xml --cov-fail-under=95
```

GitHub Actions workflow included at `.github/workflows/backend-tests.yml`
