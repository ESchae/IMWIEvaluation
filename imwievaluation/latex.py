""" Module for generating pretty pdf results using Latex.
"""
from pylatex import Document, Section, TikZ, Axis, Plot, Center, LargeText, HorizontalSpace, LineBreak
from pylatex.utils import NoEscape, bold
from pylatex import Package
from imwievaluation.resultscsv import ResultsCSV
from imwievaluation.surveyxml import SurveyXML
from imwievaluation.questions import MatrixQuestion, MatrixFivePointsQuestion, MultipleChoiceQuestion, YesNoQuestion


exclude_question_names = ['Bitte wähle Zutreffendes aus.',
                          'Bitte kreuze Zutreffendes an.']

with_xticks = [
    'Ich erkenne die Bedeutung der Lehrinhalte für das weitere Studium.',
    'Das inhaltliche Niveau der Veranstaltung ist...',
    'Verglichen mit den vergebenen Leistungspunkten ist mein tatsächlicher Arbeitsaufwand für diese Lehrveranstaltung (1 ECTS = 30 Stunden Arbeitsaufwand)...',
    '... geht gut auf Fragen und Belange der Studierenden ein.',
    'Die Lernmaterialien spiegeln den Inhalt der Lehrveranstaltung vollständig wieder.'
]

freitext_question = 'Bitte nimm dir an dieser Stelle kurz Zeit und nutze die Chance für eine ausführlichere Rückmeldung.    WICHTIG: Bedenke, dass qualitatives Feedback in den Freitextfeldern VIEL hilfreicher ist, als deine Abstimmung bisher, vor allem in relativ kleinen Kursen. Mach was draus!  Hier ist Platz für Kommentare jeglicher Art. Zum Beispiel:   	Was hat dir an dieser Lehrveranstaltung besonders gut gefallen? 	Wo siehst du Verbesserungsvorschläge für diese Lehrveranstaltung? 	Sonstiges?'


class LatexResults(object):

    def __init__(self):
        self.doc = Document(documentclass='article',
                            document_options=['a4paper', '10pt'],
                            fontenc='T1',
                            inputenc='utf8',
                            geometry_options=['margin=1.5cm'],
                            indent=False)
        self.doc.packages.append(Package('babel', options='ngerman'))

    def add_title(self, title):
        with self.doc.create(Center()):
            self.doc.append(LargeText(bold(title)))

    def node(self, at, text, options):
        return NoEscape(
            r'\node[%s] at (%s, %s) {%s};' % (NoEscape(r', '.join(options)),
                                              at[0], at[1],
                                              text))

    def get_latex_question(self, question):
        latex_question = TikZ()
        with latex_question.create(Axis(options=question.axis_options)) as ax:
            ax.append(Plot(options=question.plot_options,
                           coordinates=question.coords))
            # TODO: check for class type better
            if hasattr(question, 'small_left_node_text'):  # MatrixFivePoints
                ax.append(self.node(at=('axis cs: 0', question.small_node_y),
                                    options=question.small_node_options,
                                    text=question.small_left_node_text))
                ax.append(self.node(at=('axis cs: 6', question.small_node_y),
                                    options=question.small_node_options,
                                    text=question.small_right_node_text))
        latex_question.append(self.node(at=question.question_node_at,
                                        text=question.question_title,
                                        options=question.node_options))
        return latex_question

    def generate_results_file(self, title, xml_file, csv_file, outputfile,
                              clean_tex=False):
        structure = SurveyXML(xml_file).get_survey_structure()
        results = ResultsCSV(csv_file)
        self.add_title(title)
        for question_group in structure:
            section_name = question_group['group_name']
            with self.doc.create(Section(section_name)):
                for parent_question in question_group['questions']:
                    parent_question_name = parent_question['question_name']
                    question_responses = parent_question['question_responses']
                    question_type = parent_question['question_type']
                    sub_questions = parent_question['sub_questions']
                    if question_type == 'matrix':
                        if parent_question_name not in exclude_question_names:
                            self.doc.append(parent_question_name)
                            self.doc.append('\n\n')
                        for sub_question in sub_questions:
                            coords = results.get_coords(parent_question_name,
                                                        sub_question,
                                                        question_responses)
                            if sub_question in with_xticks:
                                xtick_empty = False
                            else:
                                xtick_empty = True
                            question = MatrixQuestion(
                                sub_question, coords, xtick_empty)
                            latex_question = self.get_latex_question(question)
                            self.doc.append(latex_question)
                            self.doc.append('\n\n')

                    elif question_type == 'matrix_five_points':
                        if '-->' in sub_questions[0]:
                            self.doc.append(parent_question_name)
                            self.doc.append('\n\n')
                        for sub_question in sub_questions:
                            responses = [int(response) for response in question_responses]
                            coords = results.get_coords(
                                parent_question_name,
                                sub_question,
                                responses)
                            if '-->' in sub_question:
                                question_title, details = sub_question.split('-->')
                                text_left, text_right = details.split('|')
                            else:
                                question_title = parent_question_name
                                text_left, text_right = sub_question.split('|')
                            question = MatrixFivePointsQuestion(
                                question_title, coords,
                                text_left, text_right)
                            latex_question = self.get_latex_question(
                                question)
                            self.doc.append(latex_question)
                            self.doc.append('\n\n')

                    elif question_type == 'multiple_choice':
                        coords, sonstiges = results.get_coords_and_sonstiges_multiple_choice(
                            parent_question_name, question_responses)
                        question = MultipleChoiceQuestion(parent_question_name,
                                                          coords)
                        latex_question = self.get_latex_question(question)
                        self.doc.append(latex_question)
                        self.doc.append('\n')
                        self.doc.append(HorizontalSpace('7cm'))
                        self.doc.append(NoEscape(r'Sonstiges: %s' % r'; '.join(sonstiges)))
                        self.doc.append('\n\n')

                    elif question_type == 'text':
                        if not section_name == 'Freitext':
                            self.doc.append(bold(parent_question_name))
                            self.doc.append('\n\n')
                            text = results.get_text_responses(parent_question_name)
                        else:
                            text = results.get_text_responses(freitext_question)
                        self.doc.append(' \n\n '.join(text))
                        self.doc.append('\n\n')

                    elif question_type == 'yes_no':
                        num_yes, num_no = results.get_num_yes_num_no(parent_question_name)
                        question = YesNoQuestion(parent_question_name, num_yes, num_no)
                        latex_question = self.get_latex_question(question)
                        self.doc.append(latex_question)
                        self.doc.append('\n\n')

                    elif question_type == 'single_choice':
                        coords = results.get_coords_single_choice(
                            parent_question_name, question_responses)
                        question = MultipleChoiceQuestion(
                            parent_question_name, coords)
                        latex_question = self.get_latex_question(question)
                        self.doc.append(latex_question)
                        self.doc.append('\n\n')

                    elif question_type == 'gesamtnote':
                        responses = [int(response) for response in question_responses]
                        coords = results.get_coords(parent_question_name, None, responses)
                        question = MatrixFivePointsQuestion(parent_question_name, coords,
                                                            text_left='', text_right='')
                        latex_question = self.get_latex_question(question)
                        self.doc.append(latex_question)

        self.doc.generate_pdf(outputfile, clean_tex=clean_tex)
