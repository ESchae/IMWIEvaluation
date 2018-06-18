#!/usr/bin/env python3
import os
import logging
from configparser import ConfigParser

logger = logging.getLogger(__name__)
configParser = ConfigParser()
configParser.read('config.ini')


def generate_semester_directory_structure(semester, basepath):
    semester_directory = os.path.join(basepath, semester)
    if not os.path.exists(semester_directory):
        os.makedirs(semester_directory)
        for subdirectory in ['participants', 'results-csv', 'results-pdf']:
            os.makedirs(os.path.join(semester_directory, subdirectory))
        generate_lecture_survey_file(semester_directory)
    else:
        raise OSError('Directory %s already exists!' % semester_directory)


def generate_lecture_survey_file(semester_directory):
    filename = os.path.join(semester_directory, 'lectures_survey.txt')
    with open(filename, 'w') as survey_file:
        header = ['lecturer', 'gender', 'mail', 'lecture title', 'tutorial']
        survey_file.write('\t'.join(header))



semester = configParser['structure']['semester']
basepath = configParser['structure']['basepath']

generate_semester_directory_structure(semester, basepath)








