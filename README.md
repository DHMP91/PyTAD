# PyTAD
Python Test Automation Dashboard (PyTAD)

**Currently Under Development**

Goal of this project is to have an overall view of test health and test traceability for the **pytest** framework.

Target Users: 
    Product Manager and or QA Managers who would like to monitor and insight of automated tests and test runs

Planned features is:
- Automatic registering of tests from pytest
- View for active running test
- History of test cases test runs
- Automatic Defect association from pytest marks
- Test status breakdown per product version/branch
- Searching ability
- Stale tests detection
- Flaky tests detection
- Single reporting source for parallel pytest run or multiple pytest runs.



# Create API User and Token
```text
python .\manage.py createsuperuser # Create superuser for api
python .\manage.py migrate authtoken  # Need to be done only once per db creation
python .\manage.py drf_create_token <username> # Create token for user
```

# Cheat sheet
```
# DB migration update and migrate
python .\manage.py makemigrations
python .\manage.py migrate

# Server start
python .\manage.py runserver

# Build schema (drf spectacuar lib)
python .\manage.py spectacular --color --file schema.yml
```