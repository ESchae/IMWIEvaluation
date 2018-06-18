import logging
import os
from string import Template
from configparser import ConfigParser
from imwievaluation.semester import Semester
from imwievaluation.mail import MailServer
from imwievaluation.limesurvey import LimeSurveySession



logger = logging.getLogger(__name__)
configParser = ConfigParser()
configParser.read('config.ini')


current_semester = configParser['structure']['semester']
basepath = configParser['structure']['basepath']
semester_folder = os.path.join(basepath, current_semester)
pdf_folder = os.path.join(current_semester, 'results-pdf')


if not os.path.exists(semester_folder):
    logger.warning(
        'Directory for semester %s does not exist!' % semester_folder)
    logger.warning('Run initialise_new_semester.py first')


# parse survey file
lectures_survey = os.path.join(semester_folder, 'lectures_survey.txt')
semester = Semester(term=current_semester)
semester.read_survey_file(lectures_survey)


# initialise limesurvey api connection
url = configParser['limesurvey']['url']
username = configParser['limesurvey']['username']
password = configParser['limesurvey']['password']
limesurvey = LimeSurveySession(url, username, password)


# initialise mail server
from_mail_address = configParser['mail']['from_mail_address']
smtp_server = configParser['mail']['smtp_server']
port = configParser['mail']['port']
password = configParser['mail']['password']
mail = MailServer(from_mail_address, smtp_server, port, password)

send_results_mail = Template('''
$opening 


anbei erhalten Sie die bisherigen Ergebnisse der Evaluation Ihrer Lehrveranstaltungen.


Folgende Veranstaltungen wurden evaluiert (inklusive Teilnahme an Evaluation):

$evaluated_lectures

Die Ergebnisse von Evaluationen, an denen weniger als drei Personen teilgenommen haben,
werden nicht verschickt.

Wir würden uns freuen, wenn Sie in Ihren Veranstaltungen Zeit finden würden, die Ergebnisse gemeinsam mit Ihrem Kurs zu besprechen.


Falls Sie gerne noch mehr Rückmeldungen erhalten möchten, können Sie folgendes versuchen:
Antworten Sie bitte auf diese Mail und nennen Sie einen Termin, bis wann Sie die Evaluation verlängern möchten.
In diesem Fall werden nochmals automatisierte Erinnerungsmails an die Teilnehmenden verschickt.
Gleichzeitig können Sie die Evaluation erneut in Ihren Veranstaltungen ansprechen.
Sie erhalten die neuen Ergebnisse abschließend zum vereinbartem Termin.



Vielen Dank nochmals für Ihre Mithilfe!
Mit freundlichen Grüßen
IMWI Studentischer Ausschuss - Verantwortliche Elke Schächtele

''')

all_surveys = limesurvey.list_all_surveys(term=current_semester)
all_surveys_titles_with_id = {survey['surveyls_title']: int(survey['sid']) for survey in all_surveys}

for lecturer in semester.lecturers:

    if lecturer.name == 'Cunillera':
        print('Skipping %s' % lecturer.name)
        continue
    print('Preparing mail for %s' % lecturer.name)
    if lecturer.gender == 'm':
        opening = 'Sehr geehrter Herr %s,' % lecturer.name
    else:
        opening = 'Sehr geehrte Frau %s,' % lecturer.name

    evaluated_lectures = []
    attachment_files = []

    for lecture in lecturer.lectures:
        survey_title = lecture.get_filename(modus='evaluation')
        if survey_title in all_surveys_titles_with_id:
            # get participation
            survey_id = all_surveys_titles_with_id[survey_title]
            complete, tokens, incomplete = limesurvey.get_survey_participation(survey_id)
            percentage_participation = complete / tokens * 100
            evaluated_lectures.append('%s \n\tVollständig teilgenommen: %s/%s (%.2f Prozent), Unvollständig teilgenommen: %s\n'
                                      % (lecture.title, complete, tokens, percentage_participation, incomplete))

            # only send evaluation if three or more participants
            if complete >= 3:
                pdf_file = lecture.get_filename(modus='pdf') + '.pdf'
                pdf_file = os.path.join(pdf_folder, pdf_file)
                if not os.path.exists(pdf_file):
                    print('Could not find pdf file for %s' % pdf_file)
                    continue
                attachment_files.append(pdf_file)
        else:
            print('DID NOT EVALUATE %s' % survey_title)
            continue

    if evaluated_lectures == []:
        print('No lectures evaluated for %s' % lecturer.name)
        continue

    # send mail
    mail_text = send_results_mail.substitute(
        opening=opening, evaluated_lectures=''.join(evaluated_lectures))
    print(attachment_files)
    print(mail_text)
    print()
    to_mail_address = lecturer.mail
    print(to_mail_address)
    mail.send(to_mail_address=to_mail_address,
              subject='Ergebnisse Evaluation WS2017/2018',
              text=mail_text,
              attachment_files=attachment_files)

