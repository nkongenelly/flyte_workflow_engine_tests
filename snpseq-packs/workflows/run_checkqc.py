# Hello World

import flytekit as fl
import os
import requests
import json

image_spec = fl.ImageSpec(
    # The name of the image. This image will be used by the `say_hello`` task.
    name="snpseq-packs-img",

    # Lock file with dependencies to be installed in the image.
    requirements="uv.lock",

    # Image registry to  which this image will be pushed.
    # Set the Environment variable FLYTE_IMAGE_REGISTRY to the URL of your registry.
    # The image will be built on your local machine, so enure that your Docker is running.
    # Ensure that pushed image is accessible to your Flyte cluster, so that it can pull the image
    # when it spins up the task container.
    registry="ghcr.io/nkongenelly" #os.environ['FLYTE_IMAGE_REGISTRY']
)

# @fl.task(container_image=image_spec)
# Use default docker image for now i.e https://docs-legacy.flyte.org/en/latest/user_guide/customizing_dependencies/multiple_images_in_a_workflow.html#:~:text=For%20every%20flytekit,flytekit.task()%20decorator.
@fl.task()
def run_checkqc(url: str) -> dict:
    """Fetch JSON data from a given URL."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raises an error for bad responses
    # return json.dumps(response.json())
    return response.json()

@fl.workflow
def fetch_workflow(url: str) -> dict:
    # url = "http://localhost:9992/qc/200624_A00834_0183_BHMTFYTINY?useClosestReadLength&downgrade=ReadsPerSampleHandler"
    checkqc_res = run_checkqc(url=url)
    return checkqc_res


# if __name__ == "__main__":
#     # Example run
#     print(fetch_workflow())

#     parameters:
#   base_url: https://miarka2.uppmax.uu.se:4444/checkqc/qc/200624_A00834_0183_BHMTFYTINY
#   downgrade_errors: ''
#   flowcell_name: HMTFYTINY
#   ignore_result: false
#   metadata:
#     library_tube_barcode: NV0217945-LIB
#   uppmax_api_key: '********'