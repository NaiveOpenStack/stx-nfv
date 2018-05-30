#
# Copyright (c) 2015-2016 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
from _vim_api_events import vim_api_events_initialize
from _vim_api_events import vim_api_events_finalize
from _vim_nfvi_events import vim_nfvi_events_initialize
from _vim_nfvi_events import vim_nfvi_events_finalize


def events_initialize():
    """
    Initialize the events package
    """
    vim_api_events_initialize()
    vim_nfvi_events_initialize()


def events_finalize():
    """
    Finalize the events package
    """
    vim_api_events_finalize()
    vim_nfvi_events_finalize()
