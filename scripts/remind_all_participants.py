#!/usr/bin/env python3
import os
import logging
from configparser import ConfigParser
from imwievaluation.limesurvey import LimeSurveySession

logger = logging.getLogger(__name__)
configParser = ConfigParser()
configParser.read('config.ini')


semester = configParser['structure']['semester']
basepath = configParser['structure']['basepath']
semester_folder = os.path.join(basepath, semester)

if not os.path.exists(semester_folder):
    raise OSError(
        'Directory for semester %s does not exist!' % semester_folder)


url = configParser['limesurvey']['url']
username = configParser['limesurvey']['username']
password = configParser['limesurvey']['password']
limesurvey = LimeSurveySession(url, username, password)

limesurvey.remind_all_participants(term=semester)

