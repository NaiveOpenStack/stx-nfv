#
# Copyright (c) 2016 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
import os
import subprocess

from nfv_vim import database
from nfv_vim import tables


def test_nfv_vim_database_upgrade_from_17_06():
    """
    Test VIM database upgrades from 17.06 GA
    """
    root_dir = os.environ['VIRTUAL_ENV']

    devnull = open(os.devnull, 'w')
    try:
        vim_cmd = ("nfv-vim-manage db-load-data -d %s "
                   "-f %s/nfv_vim_db_17.06_GA" % (root_dir, root_dir))

        subprocess.check_call([vim_cmd], shell=True, stderr=devnull)

    except subprocess.CalledProcessError:
        raise

    config = dict()
    config['database_dir'] = root_dir
    database.database_initialize(config)
    database.database_migrate_data()
    tables.tables_initialize()
