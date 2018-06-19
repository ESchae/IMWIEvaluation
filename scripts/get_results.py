#!/usr/bin/env python3
# from imwievaluation.surveyxml import SurveyXML
#
# sx = SurveyXML('../imwievaluation/tests/testfiles/survey.xml')
# structure = sx.get_survey_structure()
#
# for group in structure:
#     print(group['group_name'])
#     for question in group['questions']:
#         print('\t %s' % question['question_name'])
#         print('\t %s' % question['question_responses'])
#         print('\t %s' % question['sub_questions'])
#         print('\t %s' % question['question_type'])

import logging
import os
from configparser import ConfigParser
from imwievaluation.limesurvey import LimeSurveySession
from imwievaluation.semester_old import Semester
from imwievaluation.latex import LatexResults


logger = logging.getLogger(__name__)
configParser = ConfigParser()
configParser.read('config.ini')


current_semester = configParser['structure']['semester']
basepath = configParser['structure']['basepath']
semester_folder = os.path.join(basepath, current_semester)


if not os.path.exists(semester_folder):
    logger.warning(
        'Directory for semester %s does not exist!' % semester_folder)
    logger.warning('Run initialise_new_semester.py first')


# initialise limesurvey api connection
url = configParser['limesurvey']['url']
username = configParser['limesurvey']['username']
password = configParser['limesurvey']['password']
limesurvey = LimeSurveySession(url, username, password)


# parse survey file
lectures_survey = os.path.join(semester_folder, 'lectures_survey.txt')
semester = Semester(term=current_semester)
semester.read_survey_file(lectures_survey)


# export response statistics as csv files
csv_folder = os.path.join(semester_folder, 'results-csv')
limesurvey.export_statistics(current_semester, csv_folder)

# generate pretty pdfs
for lecture in semester.lectures:
    print('Generate pdf for %s' % lecture.title)
    csv_file = lecture.get_filename(modus='csv')
    csv_file = os.path.join(csv_folder, csv_file)
    if not os.path.exists(csv_file):
        print('No csv found for %s' % csv_file)
        continue
    if lecture.with_tutorial == 'y':
        xml_file = 'templates/surveys/__VORLAGE__Evaluation-mit-Tutorium.xml'
    else:
        xml_file = 'templates/surveys/__VORLAGE__Evaluation-ohne-Tutorium.xml'
    outfile = os.path.join(semester_folder, 'results-pdf',
                           lecture.get_filename(modus='pdf'))
    title = lecture.get_filename(modus='evaluation')
    try:
        results = LatexResults().generate_results_file(title=title,
                                                       xml_file=xml_file,
                                                       csv_file=csv_file,
                                                       outputfile=outfile,
                                                       clean_tex=True)
    except Exception as e:
        raise

