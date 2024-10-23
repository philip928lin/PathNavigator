# justfile

# Task to install dependencies using poetry
install:
    poetry install

# Task to run pytest tests through poetry
test:
    poetry run pytest test/
