from imwievaluation.resultscsv import ResultsCSV

csv_file = 'imwievaluation/tests/testfiles/survey_results.csv'
csv = ResultsCSV(csv_file)


def test_get_counted_values_by_column_matrix():
    col = 'Bitte wähle Zutreffendes aus. [Ich habe in dieser Veranstaltung viel gelernt.]'
    series = csv.get_counted_values_by_column(col)
    assert series['trifft voll zu'] == 3
    assert series['trifft zu'] == 7
    assert series['trifft eher zu'] == 3
    assert 'trifft gar nicht zu' not in series
    assert 'trifft zu' in series


def test_get_text_responses():
    col = 'Warum hast du nicht teilgenommen?'
    responses = csv.get_text_responses(col)
    assert responses == [
        'Die Inhalte haben sich mir auch so erschlossen.',
        'Habe alles ausreichend verstanden',
        'Für die bisherigen Aufgaben habe ich keine Hilfe benötigt.',
        'aus Zeitgründen']


def test_get_coords():
    question = 'Bitte wähle Zutreffendes aus.'
    sub_question = 'Ich habe in dieser Veranstaltung viel gelernt.'
    response_possibilities = ['trifft voll zu', 'trifft zu', 'trifft eher zu',
                              'trifft eher nicht zu', 'trifft nicht zu',
                              'trifft gar nicht zu']
    coords = csv.get_coords(question, sub_question, response_possibilities)
    assert coords == [('trifft voll zu', 3),
                      ('trifft zu', 7),
                      ('trifft eher zu', 3),
                      ('trifft eher nicht zu', 0),
                      ('trifft nicht zu', 0),
                      ('trifft gar nicht zu', 0)]
