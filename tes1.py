#!/user/bin/env python3
# -*- coding: utf-8 -*-

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-f", "--project", dest="project",
                  help="Set Coverity project",
                  default="")
parser.add_option("-m", "--snapshot_id", dest="snapshot_id",
                  help="Set Coverity snapshot id",
                  default="")
parser.add_option("-p", "--jira_project_key", dest="jira_project_key",
                  help="Set JIRA project key",
                  default="")
parser.add_option("-i", "--impact", dest="impact",
                  help="Set the impact of the Coverity exported defects",
                  default="")
(options, args) = parser.parse_args()

