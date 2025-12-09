# Hello World

import flytekit as fl
import os
import requests

image_spec = fl.ImageSpec(
    # The name of the image. This image will be used by the `say_hello`` task.
    name="run-checkqc",

    # Lock file with dependencies to be installed in the image.
    requirements="uv.lock",

    # Image registry to to which this image will be pushed.
    # Set the Environment variable FLYTE_IMAGE_REGISTRY to the URL of your registry.
    # The image will be built on your local machine, so enure that your Docker is running.
    # Ensure that pushed image is accessible to your Flyte cluster, so that it can pull the image
    # when it spins up the task container.
    registry=os.environ['FLYTE_IMAGE_REGISTRY']
)


@fl.task(container_image=image_spec)
def run_checkqc(url: str) -> dict:
    """Fetch JSON data from a given URL."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raises an error for bad responses
    return response.json()

@fl.workflow
def fetch_workflow(url: str) -> dict:
    # url = "http://localhost:9992/qc/200624_A00834_0183_BHMTFYTINY?useClosestReadLength&downgrade=ReadsPerSampleHandler"
    greeting = run_checkqc(url=url)
    return greeting
