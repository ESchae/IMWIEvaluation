"""

"""
import logging
import os
from limesurveyrc2api.limesurvey import LimeSurvey
from limesurveyrc2api.exceptions import LimeSurveyError
from imwievaluation.utils import filter_and_sort_dicts, sort_dicts, clean_string
from base64 import b64decode


class LimeSurveySession(object):

    def __init__(self, url, username, password):
        self.api = LimeSurvey(url, username)
        self.api.open(password)
        self.logger = logging.getLogger(__name__)

    def __del__(self):
        self.api.close()

    def generate_new_survey_with_participants(self, template, name,
                                              participant_data):
        if name in self.get_existing_survey_names():
            raise IOError('Survey %s already exists!' % name)
        # import survey from given template
        survey_id = self.api.survey.import_survey(template, name)
        self.logger.info('Created new evaluation "%s"' % name)
        self.logger.info('Used template: %s' % template)
        self.logger.info('New survey id: %s' % survey_id)

        # activate tokens
        response = self.api.survey.activate_tokens(survey_id)
        if response['status'] == 'OK':
            self.logger.info('Initialised token system for survey %s'
                             % survey_id)
        else:
            self.logger.info('Could not initialise token system for survey %s'
                             % survey_id)
            self.logger.info('Message was: %s' % response)

        # add participants
        response = self.api.token.add_participants(survey_id, participant_data)
        for participant in response:  # detailed logging on added participants
            self.logger.info(
                'Added %s %s (email %s) to survey %s' %
                (participant['firstname'], participant['lastname'],
                 participant['email'], survey_id))
        self.logger.info('\n')
        return survey_id

    def list_all_surveys(self, term=None):
        all_surveys = self.api.survey.list_surveys()
        if term:  # filter surveys by term
            filtered_surveys = []
            for survey in all_surveys:
                if term in survey['surveyls_title']:
                    filtered_surveys.append(survey)
            return filtered_surveys
        else:
            return all_surveys

    def get_existing_survey_names(self, term=None):
        existing_surveys = self.api.survey.list_surveys()
        if term:
            return [survey['surveyls_title'] for survey in existing_surveys
                    if term in survey['surveyls_title']]
        else:
            return [survey['surveyls_title'] for survey in existing_surveys]

    def invite_all_participants(self, term):
        surveys = self.list_all_surveys(term=term)
        for survey in surveys:

            # logging of general info
            self.logger.info(
                'Going to invite all participants for survey "%s" (id %s)' %
                (survey['surveyls_title'], survey['sid']))

            # activate survey
            self.api.survey.activate_survey(survey['sid'])
            self.logger.info('Activated survey %s' % survey['sid'])

            # invite participants for this survey
            response = self.api.token.invite_participants(
                survey_id=survey['sid'],
                token_ids=False)  # invite all

            # detailed logging on invited participants
            for key, value in response.items():
                if key != 'status':
                    participant_info = value
                    name = participant_info['name']
                    email = participant_info['email']
                    if participant_info['status'] == 'OK':
                        self.logger.info(
                            'Email invitation was send to %s (email %s)'
                            % (name, email))
                    else:
                        self.logger.info(
                            'Error sending invitation for %s (email %s)'
                            % (name, email))
                        self.logger.info('Message was: %s'
                                         % participant_info['status'])

            # finish logging
            self.logger.info(
                'Status for survey %s: %s\n'
                % (survey['sid'], response['status']))

    def remind_all_participants(self, term):
        surveys = self.list_all_surveys(term=term)
        for survey in surveys:

            # logging of general info
            self.logger.info(
                'Going to remind all participants for survey "%s" (id %s)' %
                (survey['surveyls_title'], survey['sid']))

            # invite participants for this survey
            response = self.api.token.remind_participants(
                survey_id=survey['sid'])

            # detailed logging on invited participants
            for key, value in response.items():
                if key != 'status':
                    participant_info = value
                    name = participant_info['name']
                    email = participant_info['email']
                    if participant_info['status'] == 'OK':
                        self.logger.info(
                            'Email reminder was send to %s (email %s)'
                            % (name, email))
                    else:
                        self.logger.info(
                            'Error sending reminder for %s (email %s)'
                            % (name, email))
                        self.logger.info('Message was: %s'
                                         % participant_info['status'])

            # finish logging
            self.logger.info(
                'Status for survey %s: %s\n'
                % (survey['sid'], response['status']))

    def export_statistics(self, term, csv_folder):
        surveys = self.list_all_surveys(term)
        for survey in surveys:
            self.logger.info(
                'Export response statistics for %s' % survey['surveyls_title'])
            try:
                response = self.api.survey.export_responses(
                    survey['sid'],
                    document_type='csv',
                    heading_type='full',
                    response_type='long')
            except LimeSurveyError as e:
                self.logger.error(e)
                continue
            # TODO: Somehow use Lecture.get_filename() here?
            filename = clean_string(survey['surveyls_title']).replace(' ', '_')
            filename = filename.replace('Evaluation', 'Ergebnisse')
            filename += '.csv'
            outfile = os.path.join(csv_folder, filename)
            with open(outfile, 'wb') as f:
                f.write(b64decode(response))
            self.logger.info('... saved to %s' % outfile)

    def get_group_and_question_structure(self, survey_id):
        question_groups = self.get_question_groups(survey_id)
        group_and_question_structure = []
        for group in question_groups:
            group_structure = dict()
            group_id = group['gid']
            group_question_structure = self.get_question_structure_by_group(
                survey_id, group_id)
            group_structure['group_name'] = group['group_name']
            group_structure['group_questions'] = group_question_structure
            group_and_question_structure.append(group_structure)
        return group_and_question_structure

    def get_question_groups(self, survey_id,
                            fields=['group_name', 'group_order', 'gid'],
                            sort_by='group_order'):
        question_groups = self.api.survey.list_groups(survey_id)
        return filter_and_sort_dicts(question_groups, sort_by, fields)

    def get_question_structure_by_group(self, survey_id, group_id):
        all_questions = self.api.survey.list_questions(survey_id, group_id)
        parent_questions = [question for question in all_questions
                            if (question['parent_qid'] == '0')]
        parent_questions = sort_dicts(parent_questions, 'question_order')
        question_structures = []
        for parent_question in parent_questions:
            question_structure = dict()
            question_structure['parent_question'] = parent_question['question']
            question_structure['type'] = parent_question['type']
            # get questions belonging to this parent question
            parent_qid = parent_question['qid']
            questions = [question for question in all_questions
                         if (question['parent_qid']) == parent_qid]
            questions = sort_dicts(questions, sort_by='question_order')
            questions = [question['question'] for question in questions]
            question_structure['child_questions'] = questions
            question_structures.append(question_structure)
        return question_structures

    def print_survey_participation(self, survey_id):
        summary = self.api.token.get_summary(survey_id)
        completed = summary['completed_responses']
        tokens = summary['token_count']
        incomplete = summary['incomplete_responses']
        # print('Survey participation for %s' % survey_id)
        print('Completed Responses: %s/%s (%.2f Prozent), %s incomplete'
                         % (completed, tokens, int(completed) / int(tokens) * 100,
                            incomplete))

    def get_survey_participation(self, survey_id):
        summary = self.api.token.get_summary(survey_id)
        completed = int(summary['completed_responses'])
        tokens = int(summary['token_count'])
        incomplete = int(summary['incomplete_responses'])
        return completed, tokens, incomplete
