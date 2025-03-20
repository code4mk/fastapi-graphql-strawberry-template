# Testing
This project uses `pytest` and `pytest-asyncio` for testing, along with `unittest` for unit testing (particularly for mocking and patching).

# setup env
you can add test database credentials to .env file

```bash
# Database configuration
DB_CONNECTION=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_NAME="david_commissions_test"
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

# Drop tables

To drop all tables and their data, run the following script:

```bash
python3 drop_table.py
```
