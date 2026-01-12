# Install Flyte

Follow all these instructions to install flyte; [Getting started](https://www.union.ai/docs/v1/flyte/user-guide/getting-started/)

# Clone repository

## Clone the test_automation_engine_stackstorm for testing in a separate directory
```python
git clone https://github.com/matrulda/test_automation_engine_stackstorm.git
```

- Make sure the following services are running locally on your machine by following the steps in the `test_automation_engine_stackstorm` repo:
    - arteria-runfolder: https://github.com/arteria-project/arteria (port 9991)
    - checkqc: https://github.com/Molmed/checkQC (port 9992)
    - local cluster (uses docker)
        ```
        $ flytectl demo start
        ```
        - Known [issue](https://github.com/flyteorg/flyte/issues/6814) error ```:"error","msg":"Error response from daemon: manifest unknown"``` and [solution/workaround](https://github.com/flyteorg/flyte/issues/6814#:~:text=In%20the%20mean%20while%20you%20can%20do%20flytectl%20demo%20start%20%2D%2Dversion%20v1.16.3%20instead) for this issue


## Run checkqc
```
# Install dependencies
uv sync

# Run the checkqc workflow (called fetch_workflow) found in the run_checkqc.py file
pyflyte run workflows/run_checkqc.py fetch_workflow --url=""

# Watch monitored directories to start run_checkqc when a file is added (uses Python 'Watchdog' library)
python workflows/runfolder_sensor.py 
```


# Deploying your code to Flyte with pyflyte register
Register all the code to the project in development/ staging/ production.
```
$ pyflyte register workflows --project snpseq-packs --domain development
```

This command will:

    - Build the container image defined in your ImageSpec.
    - Package up your code and deploy it to the specified project and domain in Flyte. The package will contain the code in the Python package located in the workflows directory. Note that the presence of the __init__.py file in this directory is necessary in order to make it a Python package.
    - The command will not run the workflow. You can run it from the Web interface.

This command is useful for deploying your full set of workflows to Flyte for testing.

The combination of ```pyflyte package``` and ```flytectl register``` is the standard way of [deploying your code to ```production```](https://www.union.ai/docs/v1/flyte/user-guide/development-cycle/running-your-code/#deploying-your-code-to-production:~:text=0/outputs.pb%22-,Deploying%20your%20code%20to%20production,-Package%20your%20code). This method is often used in scripts to [build and deploy workflows in a CI/CD pipeline.](https://www.union.ai/docs/v1/flyte/user-guide/development-cycle/ci-cd-deployment)

