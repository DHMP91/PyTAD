# PyTAD
Python Test Automation Dashboard (PyTAD)

**Currently Under Development**

Goal of this project is to have an overall view of test health and test traceability for the **pytest** framework.

Target Users: 
    Product Manager and or QA Managers who would like to monitor and insight of automated tests and test runs

### Current Features:
- Automatic Test Registration:
  - Automatically registers tests without manual intervention.
- Test runs association to Test case
  - Compatible with parametrize test. Each input is it's own test run
- Compatible with Pytest status (e.g xfail, xpass, skipped)
- Test Deduplication: One or more test case with the same exact test body will be match to the same test case.
- Test Change Resiliency: 
  - Ensures tests can still be found after being updated or moved:
    - Internal ID (optional but recommended): Assigns a unique ID to each test with @pytest.mark.test_id(id=<unique_ID>).
    - Relative Path: Identifies tests based on the combination of the Python module path and test name, ensuring uniqueness. 
    - Code Hash: If internal id and relative path cannot be relied on, match test by using hash of the test body.
        
        | Scenario                        | Internal ID | Relative Path | Code Hash  |
        |---------------------------------|-------------|---------------|------------|
        | Moved Test (Module Change)      |      x      |               |     x      |
        | Test Rename                     |      x      |               |     x      |
        | Test Rename + Body Change       |      x      |               |            |
        | Moved Test + Body Change        |      x      |               |            |
        | Rename + Moved (Module Change)  |      x      |               |     x      |
        | Rename + Moved + Body Change    |      x      |               |            |
        | Internal ID Change              |             |       x       |     x      |
        | Internal ID Change + Rename     |             |               |     x      |
        | Internal ID Change + Moved      |             |               |     x      |
        | Internal ID Change + Body       |             |       x       |            |
        | Duplicate Test (Same Body)      |             |               |     x      |
    
    - Test Change Tracking:
      - Test code changes are tracked and linked to the same registered test if the name and path or internal ID match. 
      - Scenario: A test's code may be updated for a new product version while still running with older code to verify previous versions (e.g., after a hot patch or bug fix). This requires tracking both test runs under the same test but with different code versions.


    

### Upcoming features:
- Monitor active running tests
- History of test cases test runs
- Automatic Defect association from pytest marks
- Test status breakdown per product version/branch
- Searching ability
- Stale tests detection
- Flaky tests detection
- Single reporting source for parallel pytest run or multiple pytest runs.



#### URLS
```text
http://<server:port>/api/schema/swagger-ui
http://<server:port>/api/schema/redoc
```

#### API User and Token
```text
python .\manage.py createsuperuser # Create superuser for api
python .\manage.py migrate authtoken  # Need to be done only once per db creation
python .\manage.py drf_create_token <username> # Create token for user
```

#### Cheat sheet
```
# DB migration update and migrate
python .\manage.py makemigrations
python .\manage.py migrate

# Server start
python .\manage.py runserver

# Build schema (drf spectacuar lib)
python .\manage.py spectacular --color --file schema.yml
```