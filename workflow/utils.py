""" supporting functions """
import pysftp
from sciflow.settings_local import sdsuser, sdspass
from workflow.settings import *


def file2sds(localfpath):
    """ send a file using ftp """
    parts = localfpath.split("/")
    localfilename = parts[-1]
    with pysftp.Connection("sds.coas.unf.edu", username=sdsuser, password=sdspass) as sftp:
        with sftp.cd(sdsnewpath):
            try:
                sftp.put(localfpath)
                sftp.chmod(sdsnewpath + '/' + localfilename, 777)
                return True
            except Exception as ftpex:
                print(ftpex)
                return False


def movesdsfile(filepath, destination):
    """ move a file on the SDS server to a new folder """


# file2sds('/Users/n00002621/Google Drive/Research/sciflow/tmp/LYCAIKOWRPUZTN-UHFFFAOYSA-N.jsonld')
