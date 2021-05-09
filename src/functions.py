import os, sys


def platform():
    return sys.platform


def project_dir():
    ''' str like '***/encryption/'''
    temp = os.path.abspath(__file__)
    return temp[:temp.rfind('src')]
