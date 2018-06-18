from imwievaluation.surveyxml import SurveyXML

xmlfile = 'imwievaluation/tests/testfiles/survey.xml'
sx = SurveyXML(xmlfile)
groups = sx.root.findall('section')
questions = sx.get_group_questions(groups[0])


def test_get_groups():
    groups = sx.get_groups()
    group_names = []
    for group in groups:
        group_names.append(sx.get_group_name(group))
    assert group_names == [
        'Beurteilung der Lehrveranstaltung',
        'Allgemeine Lehrkompetenz',
        'Studentische Leistung',
        'Lernmaterialien und Hilfsmittel',
        'Freitext',
        'Tutorium',
        'Gesamtnote']


def test_get_group_questions():
    question_names = sx.list_items_as_text(questions)
    assert question_names == [
        'Bitte wähle Zutreffendes aus.',
        'Bitte beurteile die Veranstaltung hinsichtlich folgender Aspekte \
(unabhängig von der Lehrperson):',
        'Die Lehrveranstaltung fördert ...',
        'Bitte kreuze Zutreffendes an.']


def test_get_sub_questions():
    pass


def test_get_response_names():
    response_names = sx.get_response_names(questions[0])
    assert len(response_names) == 6
    assert response_names[0] == 'trifft voll zu'
    assert response_names[-1] == 'trifft gar nicht zu'


def test_get_survey_structure():
    structure = sx.get_survey_structure()
    assert len(structure) == 7
    first_group = structure[0]
    assert type(first_group) == dict
    assert first_group['group_name'] == 'Beurteilung der Lehrveranstaltung'
    assert len(first_group['questions']) == 4
    first_question = first_group['questions'][0]
    assert first_question['question_name'] == 'Bitte wähle Zutreffendes aus.'
    first_sub_ques = first_question['sub_questions'][0]
    assert first_sub_ques == 'Ich habe in dieser Veranstaltung viel gelernt.'
    assert first_question['question_responses'][1] == 'trifft zu'
    assert first_question['question_type'] == 'matrix_text_responses'
