from pylatex.utils import NoEscape
from imwievaluation.utils import clean_string

"""

Matrix --> several sub-questions and responses (responses are the same for each sub_question)

MatrixFivePoints --> mehrere sub-questions, responsesn sind '1', '2', '3', '4' und '5'

MultipleChoice --> keine sub-questions ( = []); Häufigkeiten für jede Response zählen + 'Sonstiges' checken

SingleChoice --> keine sub-questions (und keine responses?) --> Häufigkeiten zählen

Freitext --> responses = [None], sub-questions = [];

YesNoQuestion --> 

--> vgl typen in surveyxml.py


alternativ: type könnte auch über list questions (per group) und 'type' rausgefunden werden (?)
ich glaube folgende bezeichungen stimmen
'F' = Matrix
'M' = Mehrfachauswahl
'A' = MatrixFivePoints
'L' = Liste (Optionsfelder) = SingleChoice?
'T' = Text
'Y' = Ja/Nein

TODO: In Docstring Beispiels für jeden Fragentyp angeben
+ Beispiel für Latex?

"""


class Question:

    def __init__(self, question_title, coords):
        self.axis_options = None
        self.coords = coords
        self.plot_options = None
        self.question_title = question_title
        self.question_node_at = (-2, 0.5)
        self.node_options = ['text width=5cm', 'left']


class MatrixQuestion(Question):

    def __init__(self, question_title, coords, xtick_empty=False):
        super().__init__(question_title, coords)
        self.coord_names = [coord[0] for coord in coords]
        self.coord_values = [coord[1] for coord in coords]
        self.xtick_empty = xtick_empty
        self._prepare_params()

    def _prepare_params(self):
        axis_settings = [
            'width=10.0cm',
            'height=2.5cm',
            'axis lines=left',
            'ymin=0',
            'x axis line style=-',  # no arrowhead on x axis
            'nodes near coords',
            'hide y axis',
            'x tick label style={font=\small,text width=1.5cm,align=center}',
            'enlargelimits=true',
            'ymax=%s' % sum(self.coord_values),
            'symbolic x coords={%s}' % ', '.join(self.coord_names)]
        if self.xtick_empty:
            axis_settings.append('xtick=\empty')
        self.axis_options = NoEscape(r', '.join(axis_settings))
        self.plot_options = 'ybar, fill=blue'


class MatrixFivePointsQuestion(Question):

    def __init__(self, question_title, coords, text_left, text_right):
        super().__init__(question_title, coords)
        self.x_coord_values = [coord[1] for coord in coords]
        self.small_node_y = None
        self.small_left_node_text = None
        self.small_right_node_text = None
        self.small_node_options = ['align=center', 'text width=2cm']
        self._prepare_params(text_left, text_right)

    def _prepare_params(self, text_left, text_right):
        axis_settings = [
            'width=10.0cm',
            'height=2.5cm',
            'axis lines=left',
            'x axis line style=-',
            'ymin=0',
            'hide y axis',
            'xtick={1,...,5}',
            'extra x ticks={0,6}',
            'extra tick style={tick style={draw=none}}',
            'extra x tick label={\\null}',
            'enlargelimits=true',
            'xmin=0',
            'xmax=6',
            'ymax=%s' % sum(self.x_coord_values)]
        self.axis_options = NoEscape(r', '.join(axis_settings))
        self.coords = zip([1, 2, 3, 4, 5], self.x_coord_values)
        self.plot_options = 'ybar, fill=blue, nodes near coords'
        self.small_node_y = sum(self.x_coord_values) / 2.0
        self.small_left_node_text = NoEscape(
                r'\small{%s}' % r'\\'.join(text_left.split()))
        self.small_right_node_text = NoEscape(
            r'\small{%s}' % r'\\'.join(text_right.split()))


class MultipleChoiceQuestion(Question):

    def __init__(self, question_title, coords):
        super().__init__(question_title, coords)
        self.coord_names = [coord[1] for coord in coords]
        self.coord_values = [coord[0] for coord in coords]
        self._prepare_params()

    def _prepare_params(self):
        axis_settings = [
            'xbar',
            'xmin=0',
            'axis lines=left',
            'y axis line style=-',
            'hide x axis',
            'enlargelimits=true',
            'ytick=data',
            'nodes near coords',
            'nodes near coords align={horizontal}',
            'y tick label style={font=\small,text width=9.0cm,align=right}',
            'width=5.0cm',
            'height=7.0cm',
            'symbolic y coords={%s}' % ', '.join(self.coord_names)
        ]
        if '<' in self.coord_names[1]:  # reduce spacing
            axis_settings.append('height=5.0cm')
        self.axis_options = NoEscape(r', '.join(axis_settings))
        self.plot_options = 'fill=blue'
        self.question_node_at = (-8, 3)


class YesNoQuestion(Question):

    def __init__(self, question_title, num_yes, num_no):
        super().__init__(question_title,
                         coords=[('Ja', num_yes), ('Nein', num_no)])
        self._prepare_params(num_yes, num_no)

    def _prepare_params(self, num_yes, num_no):
        axis_settings = [
            'width=10.0cm',
            'height=2.5cm',
            'axis lines=left',
            'x axis line style=-',  # no arrowhead on x axis
            'ymin=0',
            'nodes near coords',
            'hide y axis',
            'x tick label style={font=\small,text width=1.5cm,align=center}',
            'enlargelimits=true',
            'xtick=data',
            'width=3cm',
            'ymax=%s' % (num_yes + num_no),
            'symbolic x coords={Ja, Nein}'
        ]
        self.axis_options = NoEscape(r', '.join(axis_settings))
        self.plot_options = 'ybar, fill=blue'
