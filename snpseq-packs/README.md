# Install Flyte

Follow all these instructions to install flyte; [Getting started](https://www.union.ai/docs/v1/flyte/user-guide/getting-started/)

# Clone repository

# Clone the test_automation_engine_stackstorm for testing in a separate directory
```python
git clone https://github.com/matrulda/test_automation_engine_stackstorm.git
```

- Make sure the following services are running locally on your machine by following the steps in the `test_automation_engine_stackstorm` repo:
    - arteria-runfolder: https://github.com/arteria-project/arteria (port 9991)
    - checkqc: https://github.com/Molmed/checkQC (port 9992)

## Run checkqc
```
# Install dependencies
uv sync

# Run the checkqc workflow (called fetch_workflow) found in the run_checkqc.py file
pyflyte run run_checkqc.py fetch_workflow

# Watch monitored directories to start run_checkqc when a file is added (uses Python 'Watchdog' library)
python runfolder_sensor.py 
```
