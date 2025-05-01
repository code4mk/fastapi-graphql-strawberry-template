# Testing
This project uses `pytest` and `pytest-asyncio` for testing, along with `unittest` for unit testing (particularly for mocking and patching).

# setup env
you can add test database credentials to .env file

```bash
# Database configuration
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/gql_test
```


# Run tests

Tests can be run using the test script:

```bash
./scripts/test.sh
```

The script runs pytest with the following features:
- Code coverage reporting (minimum 80% coverage required)
- Coverage reports in terminal, HTML, and XML formats
- Verbose output

You can pass additional pytest arguments to the script:

```bash
./scripts/test.sh -s
```
