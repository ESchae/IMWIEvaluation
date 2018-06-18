#!/usr/bin/env python3
import os
import logging
from configparser import ConfigParser
from imwievaluation.semester import Semester

logger = logging.getLogger(__name__)
configParser = ConfigParser()
configParser.read('config.ini')


def generate_empty_participant_files(current_semester, basepath, lectures):
    participants_folder = os.path.join(
        basepath, current_semester, 'participants')
    if not os.path.exists(participants_folder):
        raise OSError(
            'Participants folder in semester %s does not exist!'
            % current_semester)
    for lecture in lectures:
        filename = os.path.join(
            participants_folder, lecture.get_filename(modus='participants'))
        if os.path.exists(filename):
            logger.info('Participants file for %s exists. Skipping' % lecture)
            continue
        else:
            with open(filename, 'w') as participant_file:
                participant_file.write('firstname,lastname,email')
                logger.info('Created %s' % os.path.basename(filename))


def send_mails_to_lecturers():
    pass


current_semester = configParser['structure']['semester']
basepath = configParser['structure']['basepath']
survey_file = os.path.join(basepath, current_semester, 'lectures_survey.txt')

semester = Semester(term=current_semester)
semester.read_survey_file(survey_file)

generate_empty_participant_files(current_semester, basepath, semester.lectures)
send_mails_to_lecturers()










