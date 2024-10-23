# justfile

# Task to install dependencies using hatch
install:
    hatch env create  # Create a virtual environment and install dependencies

# Task to run pytest tests located in the test/ directory
test:
    hatch run pytest test/  # Run tests using the environment managed by hatch
