""" validation of SciData JSON-LD files """
from datasets.mysql import *
from .logwriter import *
import json


def validate(path, filetype, loginfo):
    """ all-in-one validation function. Includes every check that we would want to do on a file m"""

    validity = {}

    # runs a check to make sure the file is in proper scidata format
    check_scidata(path, validity, loginfo)

    # Specialized checks for each dataset type
    searchstrings = getcodesnames()
    string = searchstrings[filetype]
    check_type(path, validity, loginfo, filetype, string)

    # Validity Check
    if all(validity.values()):
        return True
    else:
        return False

    # if filetype == "herg":
    #     hergcheck(path, validity, loginfo)
    # if filetype == "cif":
    #    cifcheck(path, validity, loginfo)

    # i = 0
    # for value in validity.values():
    #     if value is False:
    #         i += 1
    #         break
    #
    # if i == 0:
    #     return True
    # else:
    #     return False


def check_scidata(path, validity, loginfo):
    """ checks that file is present, is valid json, and conforms to the SciData specification """
    try:
        with open(path) as json_file:
            data = json.load(json_file)
            keys_a = []
            keys_b = []
            isscidata = True
            for k, v in data.items():
                keys_a.append(k)
                if k == '@graph':
                    for y, z in v.items():
                        keys_b.append(y)
            for y in ['@context', '@id', '@graph']:
                if y not in keys_a:
                    isscidata = False
            for y in ['scidata']:
                if y not in keys_b:
                    isscidata = False
            # write to logs
            if isscidata is True:
                logwrite("act", loginfo, "\t- Scidata: Valid")
            else:
                logwrite("act", loginfo, "\t- Scidata: Invalid!")
                logwrite("err", loginfo, "- Invalid Scidata Format!\n")
            # update validity
            validity.update({"isscidata": isscidata})
    except FileNotFoundError as ex:
        logwrite("err", loginfo, str(ex) + "\n")
        validity.update({"validfile": False})


def check_type(path, validity, loginfo, filetype, string):
    """ generic function to check for a specific type of SciData file. assumes that scidata check has been done """
    found = False
    with open(path) as file:
        if string in file.read():
            found = True
    if found:
        logwrite("act", loginfo, "\t- " + filetype + ": Valid\n")
    else:
        logwrite("act", loginfo, "\t- " + filetype + ": Invalid!\n")
        logwrite("err", loginfo, "- " + " not found!\n")

    validity.update({"is" + filetype: found})


# not needed
def hergcheck(path, validity, loginfo):
    """ check that this is a herg file"""
    searchfile = open(path)
    a = 0
    b = 0
    for line in searchfile:
        # checking if it is actually herg
        if "\"CHEMBL240\"" in line:
            a += 1
        # verifying author (an example used for testing purposes)
        if "Fray MJ" in line:
            b += 1

    if a > 0:
        isherg = True
        logwrite("act", loginfo, "\t- Herg: Valid\n")
    else:
        isherg = False
        logwrite("act", loginfo, "\t- Herg: Invalid!\n")
        logwrite("err", loginfo, "- No instance of CHEMBL240 found!\n")

    validity.update({"isherg": isherg})
    searchfile.close()


# not needed
def cifcheck(path):
    """ check that this is a CIF file"""
    searchfile = open(path)
    i = 0
    for line in searchfile:
        if "potato" in line:
            i += 1
    if i > 0:
        valid = True
    else:
        valid = False
    searchfile.close()
    return valid
