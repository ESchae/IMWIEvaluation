import pandas as pd
from pylatex.utils import NoEscape
from imwievaluation.utils import escape_latex_special_characters


class ResultsCSV(object):

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file)

    def get_counted_values_by_column(self, column):
        """ Count occurencies of every answer for the given column.
        
        :param column: (str) name of the column (header in csv file)
        :return: pandas.core.series.Series
        """
        return self.df[column].value_counts()

    def get_text_responses(self, column):
        responses = []
        for row in self.df[column]:
            if type(row) == str:
                # prevent unwanted utf-8 characters, that can not be decoded
                # properly by LaTeX
                row = row.encode('iso-8859-1', 'ignore').decode('iso-8859-1').strip()
                row = escape_latex_special_characters(row)
                row = NoEscape(row)
                responses.append(row)
        return responses

    def get_column_name(self, question, sub_question):
        if sub_question is None:
            return question
        column_name = '%s [%s]' % (question, sub_question)
        return column_name

    def get_coords(self, question, sub_question, response_possibilities):
        column_name = self.get_column_name(question, sub_question)
        counted_values = self.get_counted_values_by_column(column_name)
        coords = []
        for response_possibility in response_possibilities:
            if response_possibility in counted_values:
                coords.append((response_possibility,
                               counted_values[response_possibility]))
            else:
                coords.append((response_possibility, 0))
        return coords

    def get_coords_and_sonstiges_multiple_choice(self, question, sub_questions):
        coords = []
        for sub_question in sub_questions:
            column_name = self.get_column_name(question, sub_question)
            if sub_question == 'Sonstiges':
                sonstiges = self.get_text_responses(column_name)
                if not sonstiges:
                    sonstiges = ['Keine Angaben']
                continue
            counts = self.df[column_name].value_counts()
            if 'Ja' in counts:
                value = counts['Ja']
            else:
                value = 0
            # TODO: nicer and more general solutions for the replace cases
            # cases fail in .tex file
            coords.append((value, sub_question.replace('ß', 'ss').replace('(', '').replace(')','').replace(',', '')))
        return coords, sonstiges

    def get_coords_single_choice(self, question, responses):
        coords = []
        value_counts = self.df[question].value_counts()
        for response in responses:
            value = value_counts[response] if response in value_counts else 0
            coords.append((value, response))
        return coords

    def get_num_yes_num_no(self, question):
        value_counts = self.df[question].value_counts()
        num_yes = value_counts['Ja'] if 'Ja' in value_counts else 0
        num_no = value_counts['Nein'] if 'Nein' in value_counts else 0
        return num_yes, num_no


