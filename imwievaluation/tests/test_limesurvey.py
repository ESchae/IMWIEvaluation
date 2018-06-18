import configparser
import pytest
from imwievaluation.limesurvey import LimeSurveySession

config = configparser.ConfigParser()
with open('imwievaluation/tests/config.ini') as config_file:
    config.read_file(config_file)

# TODO: Make more modular
# TODO: Speed up tests with VCR casette

@pytest.fixture
def session():
    return LimeSurveySession(config['limesurvey']['url'],
                             config['limesurvey']['username'],
                             config['limesurvey']['password'])


@pytest.fixture
def participant_data():
    return [
        {'email': 'dg@example.com',
         'firstname': 'Doris',
         'lastname': 'Ganter'},
        {'email': 'muenster@example.com',
         'firstname': 'Anißa',
         'lastname': 'Münster'},
        {'email': 'vAAL@example.com',
         'firstname': 'Anna Lisa',
         'lastname': 'von Adel'}
    ]


def test_generate_new_survey_with_participants(session, participant_data):
    template = 'tests/testfiles/example_template_with_tutorial.lss'
    name = 'A small test! (Müller)'
    survey_id = session.generate_new_survey_with_participants(template, name,
                                                              participant_data)
    participants = session.api.token.list_participants(survey_id)
    for i, participant in enumerate(participants):
        participant = participant['participant_info']
        assert participant['email'] == participant_data[i]['email']
        assert participant['firstname'] == participant_data[i]['firstname']
        assert participant['lastname'] == participant_data[i]['lastname']
    # clean up
    session.api.survey.delete_survey(survey_id)


def test_list_all_surveys(session, participant_data):
    template = 'tests/testfiles/example_template_with_tutorial.lss'
    all_surveys = session.list_all_surveys(term=None)
    current_len = len(all_surveys)
    survey_ids = []
    for name in ['1 WS2001-2002/02', '2 WS2001-2002/02', '3 SoSe2011']:
        survey_id = session.generate_new_survey_with_participants(
            template, name, participant_data)
        survey_ids.append(survey_id)
    all_surveys = session.list_all_surveys(term=None)
    assert len(all_surveys) - current_len == 3
    ws_surveys = session.list_all_surveys(term='WS2001-2002/02')
    assert len(ws_surveys) == 2
    sose_surveys = session.list_all_surveys(term='SoSe2011')
    assert len(sose_surveys) == 1
    # clean up
    for survey_id in survey_ids:
        session.api.survey.delete_survey(survey_id)


def test_invite_all_participants(session, participant_data):
    template = 'tests/testfiles/example_template_with_tutorial.lss'
    survey_ids = []
    for name in ['1 WS2001-2002/02', '2 WS2001-2002/02', '3 SoSe2011']:
        survey_id = session.generate_new_survey_with_participants(
            template, name, participant_data)
        survey_ids.append(survey_id)
    session.invite_all_participants(term='WS2001-2002/02')
    # TODO: Tests (so far only manually tested and via log file
    # clean up
    for survey_id in survey_ids:
        session.api.survey.delete_survey(survey_id)


    # TODO: add test for get_question_groups and more
    # TODO: mock limesurvey!
