#!/usr/bin/env python3

"""
Purpose
-------

This module is intended to collect pipeline run statistics (such as
time, cpu, RAM for each tasks) into a report JSON

Expected input
--------------

- ``trace_file`` : *Trace file generated by nextflow*


Code documentation
------------------

"""

__version__ = "1.0.0"
__build__ = "16012018"
__template__ = "pipeline_status-nf"


import os
import json
import traceback

from os.path import join

from assemblerflow_utils.assemblerflow_base import get_logger, log_error

logger = get_logger(__file__)


LOG_STATS = ".pipeline_status.json"

if __file__.endswith(".command.sh"):
    fastq_id = 'sample_id'
    TRACE_FILE = 'pipeline_stats.txt'
    WORKDIR = '${workflow.projectDir}'


def get_json_info(fields, header):
    """

    Parameters
    ----------
    fields

    Returns
    -------

    """

    json_dic = dict((x, y) for x, y in zip(header, fields))

    return json_dic


def get_previous_stats(stats_path):
    """

    Parameters
    ----------
    workdir

    Returns
    -------

    """

    logger.debug("Path to pipeline status data set to: {}".format(stats_path))
    if os.path.exists(stats_path):
        logger.debug("Existing pipeline status data found. Loading JSON.")
        with open(stats_path) as fh:
            stats_json = json.load(fh)

    else:
        logger.debug("No pipeline status data found.")
        stats_json = {}

    return stats_json


def main(sample_id, trace_file, workdir):
    """
    Parses a nextflow trace file, searches for processes with a specific tag
    and sends a JSON report with the relevant information

    The expected fields for the trace file are::

        0. task_id
        1. process
        2. tag
        3. status
        4. exit code
        5. start timestamp
        6. container
        7. cpus
        8. duration
        9. realtime
        10. queue
        11. cpu percentage
        12. memory percentage
        13. real memory size of the process
        14. virtual memory size of the process

    Parameters
    ----------
    trace_file : str
        Path to the nextflow trace file
    """

    # Determine the path of the stored JSON for the sample_id
    stats_suffix = ".stats.json"
    stats_path = join(workdir, sample_id + stats_suffix)
    trace_path = join(workdir, trace_file)

    logger.info("Starting pipeline status routine")

    logger.debug("Checking for previous pipeline status data")
    stats_array = get_previous_stats(stats_path)
    logger.info("Stats JSON object set to : {}".format(stats_array))

    # Search for this substring in the tags field. Only lines with this
    # tag will be processed for the reports
    tag = " getStats"
    logger.debug("Tag variable set to: {}".format(tag))

    logger.info("Starting parsing of trace file: {}".format(trace_path))
    with open(trace_path) as fh:

        header = next(fh).strip().split()
        logger.debug("Header set to: {}".format(header))

        for line in fh:
            fields = line.strip().split("\t")
            # Check if tag substring is in the tag field of the nextflow trace
            if tag in fields[2] and fields[3] == "COMPLETED":
                logger.debug(
                    "Parsing trace line with COMPLETED status: {}".format(
                        line))
                current_json = get_json_info(fields, header)

                stats_array[fields[0]] = current_json
            else:
                logger.debug(
                    "Ignoring trace line without COMPLETED status"
                    " or stats specific tag: {}".format(
                        line))

    with open(join(stats_path), "w") as fh, open(".report.json", "w") as rfh:
        fh.write(json.dumps(stats_array, separators=(",", ":")))
        rfh.write(json.dumps(stats_array, separators=(",", ":")))


if __name__ == "__main__":

    try:
        main(fastq_id, TRACE_FILE, WORKDIR)
    except Exception:
        logger.error("Module exited unexpectedly with error:\\n{}".format(
            traceback.format_exc()))
        log_error()
