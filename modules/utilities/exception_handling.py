#!/usr/bin/env python

import os
import sys
import traceback


def exception_details():
    """
    This function gets details about the exceptions

    Returns:
        _description_
    """
    # get error details
    exception_type, exception_value, exception_trace = sys.exc_info()

    # get the file location
    file_name = os.path.split(exception_trace.tb_frame.f_code.co_filename)[1]

    # get the line number
    line_no = exception_trace.tb_lineno

    # get the trace back to the source
    exception_trace = ''.join(traceback.format_tb(exception_trace))

    # return results
    return [
        str(exception_type),
        str(exception_value),
        str(exception_trace),
        str(line_no),
        str(file_name)
    ]
