"""nf-redun-06"""

import subprocess

from flytekit import task
from flytekitplugins.pod import Pod
from kubernetes.client.models import (V1Container, V1PodSpec,
                                      V1ResourceRequirements, V1Toleration)
from latch import workflow
from latch.types import LatchDir, LatchFile


def _get_96_spot_pod() -> Pod:
    """[ "c6i.24xlarge", "c5.24xlarge", "c5.metal", "c5d.24xlarge", "c5d.metal" ]"""

    primary_container = V1Container(name="primary")
    resources = V1ResourceRequirements(
        requests={"cpu": "90", "memory": "170Gi"},
        limits={"cpu": "96", "memory": "192Gi"},
    )
    primary_container.resources = resources

    return Pod(
        pod_spec=V1PodSpec(
            containers=[primary_container],
            tolerations=[
                V1Toleration(effect="NoSchedule", key="ng", value="cpu-96-spot")
            ],
        ),
        primary_container_name="primary",
    )


large_spot_task = task(task_config=_get_96_spot_pod())


@large_spot_task
def redun_task(
    fastq1: LatchFile,
    fastq2: LatchFile,
    sample: str,
) -> LatchDir:

    with open("/root/sample.csv", "w") as f:
        f.write("sample,fastq_1,fastq_2\n")
        f.write(f"{sample},{fastq1.local_path},{fastq2.local_path}\n")

    subprocess.run(
        [
            "nextflow",
            "run",
            "nf-redun-06",
            "-c",
            "/root/nf-redun-06/conf/test.config",
            "--input",
            "/root/sample.csv",
            "--genome",
            "GRCh37",
        ],
        check=True,
    )
    return LatchDir("/root/results", f"latch:///Rejuvenome Redun 06/{sample}/")


@workflow
def redun_workflow(
    fastq1: LatchFile,
    fastq2: LatchFile,
    sample: str,
) -> LatchDir:
    """nf-redun-06


    __metadata__:
        display_name: nf-redun-06
        author:
            name:
            email:
            github:
        repository:
        license:
            id: MIT

    Args:

        fastq1:
          Paired-end read 1 file to be processed.

          __metadata__:
            display_name: FastQ Read 1

        fastq2:
          Paired-end read 2 file to be processed.

          __metadata__:
            display_name: FastQ Read 2

        sample:
          Semantic sample identifier.

          __metadata__:
            display_name: Sample
    """
    return redun_task(
        fastq1=fastq1,
        fastq2=fastq2,
        sample=sample,
    )
