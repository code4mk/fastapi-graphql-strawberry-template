## Database migration process with Alembic
Alembic is a database migration tool for SQLAlchemy.

### revision (migration)
you can use the following command to create a new migration file.

```bash
alembic revision --autogenerate -m "initial project"
```

this will create a new migration file in the `alembic/versions` directory.

### upgrade (migrate)
you can use the following command to migrate the database.

```bash
alembic upgrade head
```

### Running the Project

To start the application:

```bash
./run-project.sh
```

The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

The graphql playground will be available at [http://127.0.0.1:8000/graphql](http://127.0.0.1:8000/graphql) in your browser.
