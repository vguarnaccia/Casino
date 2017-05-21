git pull
coverage run -m casino.test # run test suite and create coverage report. 
coverage html # Make html report. Shoot for 100% coveage but at least 80%.
chromium-browser htmlcov/index.html # view report
sphinx-apidoc -f -o docs/source .
