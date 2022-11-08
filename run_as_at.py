#!/usr/bin/env python3

import os
import subprocess
from job import main as run_job

run_job()
subprocess.Popen(
    f"at now + 12 hours <<< {os.path.abspath(__file__)}",
    shell=True,
    executable="/bin/bash",
)
