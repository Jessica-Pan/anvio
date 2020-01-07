#!/usr/bin/env python
# -*- coding: utf-8
"""
    This file contains KofamSetup and Kofam classes.

"""

import os
import gzip
import shutil
import requests

import anvio
import anvio.dbops as dbops
import anvio.utils as utils
import anvio.terminal as terminal
import anvio.filesnpaths as filesnpaths

__author__ = "Developers of anvi'o (see AUTHORS.txt)"
__copyright__ = "Copyleft 2015-2020, the Meren Lab (http://merenlab.org/)"
__license__ = "GPL 3.0"
__version__ = anvio.__version__
__maintainer__ = "Özcan Esen"
__email__ = "ozcanesen@gmail.com"

run = terminal.Run()
progress = terminal.Progress()
pp = terminal.pretty_print


class KofamSetup(object):
    def __init__(self, args, run=run, progress=progress):
        self.args = args
        self.run = run
        self.progress = progress
        self.kofam_data_dir = args.kofam_data_dir

        filesnpaths.is_program_exists('hmmpress')

        # default directory will be called KEGG and will store the KEGG Module data as well
        if not self.kofam_data_dir:
            self.kofam_data_dir = os.path.join(os.path.dirname(anvio.__file__), 'data/misc/KEGG')

        if not args.reset:
            self.is_database_exists()

        filesnpaths.gen_output_directory(self.kofam_data_dir, delete_if_exists=args.reset)

        # ftp path for HMM profiles and KO list
            # for ko list, add /ko_list.gz to end of url
            # for profiles, add /profiles.tar.gz  to end of url 
        self.database_url = "ftp://ftp.genome.jp/pub/db/kofam"


    def is_database_exists(self):
        if os.path.exists(os.path.join(self.kofam_data_dir, 'K00001.hmm')): # we arbitrarily check for the first profile
            raise ConfigError("It seems you already have KOfam HMM profiles installed in '%s', please use --reset flag if you want to re-download it." % self.kofam_data_dir)