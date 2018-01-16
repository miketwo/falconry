# -*- coding: utf-8 -*-
import subprocess
import os
import re


class Commit(dict):
    def __init__(self, sha, list_of_changes):
        self['sha'] = sha
        self['changes'] = list_of_changes


class Change(dict):
    def __init__(self, file, additions, deletions, is_binary=False):
        self['file'] = file
        self['additions'] = additions
        self['deletions'] = deletions
        self['is_binary'] = is_binary


def explode_path(path):
    ''' Turns a file path into a list of folders.

    Example:
        path = "/home/git/project/library/file.txt"

        Returns [
            '/home',
            '/home/git',
            '/home/git/project',
            '/home/git/project/library',
            '/home/git/project/library/file.txt',
            ]
    '''
    assert path, "No blanks!"
    retval = [path]
    while True:
        # print("retval={}".format(retval))
        split = os.path.split(retval[-1])
        if not split[1]:
            break
        retval.append(split[0])
    return retval


def line_has_sha(line):
    ''' Something like:
    999fc0687d6b27309e3604602cf996c71b229537 Added a few tests for smtp EmailBackend.
    '''
    result = re.search(r'^[a-z0-9]{40}\b', line)
    # print("Checking {} for SHA == {}".format(line, bool(result)))
    return bool(result)


def line_has_stats(line):
    ''' Something like:
    6   5   docs/topics/auth/passwords.txt
    '''
    result = re.search(r'^[0-9]+[\s]+[0-9]+', line)
    return bool(result)


def path_from_line(line):
    ''' Something like:
    6   5   docs/topics/auth/passwords.txt
    '''
    return line.split()[2]


def parse(gitlog):
    ''' Git log looks something like
        COMMIT_SHA1    DESCRIPTION
        ADDITIONS  DELETIONS   FILEPATH
        ADDITIONS  DELETIONS   FILEPATH
        ADDITIONS  DELETIONS   FILEPATH
        ADDITIONS  DELETIONS   FILEPATH
        ADDITIONS  DELETIONS   FILEPATH
        COMMIT_SHA2    DESCRIPTION
        ADDITIONS  DELETIONS   FILEPATH
        ADDITIONS  DELETIONS   FILEPATH

        We're aiming to change this into something the Apriori algorithm can
        digest -- namely a "transaction" specifying what files and folders
        changed together.] in the commit.

       To start we'll consider each commit a transaction, so we want to yield
       Transactions (tuples)
    '''
    split_gitlog = gitlog.strip().split('\n')
    retval = list()
    for line in split_gitlog:
        if line_has_sha(line):
            if retval:
                yield tuple(retval)
            retval = [line[:40]]
        elif line_has_stats(line):
            pth = path_from_line(line)
            exploded = explode_path(pth)
            retval.extend(exploded[:-1])
        else:
            raise Exception("Error processing {}".format(line))


def read_git_repo(path):
    cmd = "git log --pretty=oneline --simplify-merges --numstat"
    output = subprocess.check_output(cmd, shell=True)
    parse(output)


def add_two_things(a, b):
    return a+b
