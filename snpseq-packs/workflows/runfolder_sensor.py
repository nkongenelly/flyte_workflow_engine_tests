from datetime import timedelta
import json

import flytekit as fl
import requests
from flytekit import FixedRate
from flytekit.configuration import Config
from workflows.run_checkqc import fetch_workflow


@fl.task()
def runfolder_ready():
    # url = "https://palaeotropical-sparkle-polygamous.ngrok-free.dev/qc/200624_A00834_0183_BHMTFYTINY?useClosestReadLength&downgrade=ReadsPerSampleHandler"
    url = "https://palaeotropical-sparkle-polygamous.ngrok-free.dev/api/1.0/runfolders/pickup"
    # url = "http://0.0.0.0:9991/api/1.0/runfolders/pickup"
    res = requests.get(url, timeout=10)
    res.raise_for_status()  # Raises an error for bad responses

    if res.text:
        runfolder = res.json()
        runfolder_name = runfolder['path'].split('/')[-1]
        runfolder_path = f"https://palaeotropical-sparkle-polygamous.ngrok-free.dev/qc/{runfolder_name}?useClosestReadLength&downgrade=ReadsPerSampleHandler"
        checkqc_res = fetch_workflow(url=runfolder_path)
        return checkqc_res


@fl.workflow()
def runfolder_ready_workflow():
    runfolder_res = runfolder_ready()
    return runfolder_res


fl.LaunchPlan.get_or_create(
    workflow=runfolder_ready_workflow,
    name="runfolder_ready_workflow_lp",
    schedule="*/2 * * * *",  # Following schedule runs every 2 min
)
    # schedule=FixedRate(
    #     duration=timedelta(minutes=5)
    # ),
remote = fl.FlyteRemote(
        config=Config.auto(),
        default_project="snpseq-packs",
        default_domain="development"
    )
launch_plan = remote.fetch_launch_plan(
    name="runfolder_ready_workflow_lp",
    version="latest"
)
remote.client.update_launch_plan(launch_plan.id, "INACTIVE")
# # remote.execute(launch_plan, inputs=<inputs>)
remote.execute(launch_plan)