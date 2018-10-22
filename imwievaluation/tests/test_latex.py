from imwievaluation.latex import LatexResults

lr = LatexResults()


def test_title():
    title = lr.title('test survey 12345').dumps()
    assert title == r'''\begin{center}%
\begin{Large}%
test survey 12345%
\end{Large}%
\end{center}'''


# def test_generate_questio_matrix_style():
#     x_coord_names = ['trifft voll zu', 'trifft zu', 'trifft eher zu',
#                      'trifft eher nicht zu', 'trifft nicht zu',
#                      'trifft gar nicht zu']
#     x_coords_values = [6, 1, 1, 0, 0, 0]
#     question_title = 'Ich besuche diese Veranstaltung gerne'
#     question = lr.generate_question_matrix_style(
#         x_coord_names, x_coords_values, question_title)
#     assert question.dumps() == r'''\begin{tikzpicture}%
# \begin{axis}[width=10.0cm, height=2.5cm, axis lines=left, ymin=0, nodes near coords, hide y axis, x tick label style={font=\small,text width=1.5cm,align=center}, enlargelimits=true, symbolic x coords={trifft voll zu, trifft zu, trifft eher zu, trifft eher nicht zu, trifft nicht zu, trifft gar nicht zu}, ymax=8]%
# \addplot[ybar, fill=blue] coordinates {%
# (trifft voll zu,6)%
# (trifft zu,1)%
# (trifft eher zu,1)%
# (trifft eher nicht zu,0)%
# (trifft nicht zu,0)%
# (trifft gar nicht zu,0)%
# };%
# %
# %
# \end{axis}%
# \node[text width=5cm, left] at (-2, 0.5) {Ich besuche diese Veranstaltung gerne};%
# \end{tikzpicture}'''
#
#
# def test_node():
#     text = 'A node text.'
#     at = (1, -2)
#     options = ['left', 'text width=5cm']
#     node = lr.node(at=at, text=text, options=options)
#     assert node == r'\node[left, text width=5cm] at (1, -2) {A node text.};'
#
#
# def test_generate_matrix_five_points():
#     x_coord_values = [0, 4, 3, 1, 0]
#     text_left = 'sehr einfach'
#     text_right = 'sehr schwierig'
#     question_title = 'Inhalt'
#     question = lr.generate_question_matrix_five_points_style(
#         x_coord_values, text_left, text_right, question_title)
#     assert question.dumps() == r'''\begin{tikzpicture}%
# \begin{axis}[width=10.0cm, height=2.5cm, axis lines=left, x axis line style=-, ymin=0, hide y axis, xtick={1,...,5}, extra x ticks={0,6}, extra tick style={tick style={draw=none}}, extra x tick label={\null}, enlargelimits=true, xmin=0, xmax=6, ymax=8]%
# \addplot[ybar, fill=blue, nodes near coords] coordinates {%
# (1,0)%
# (2,4)%
# (3,3)%
# (4,1)%
# (5,0)%
# };%
# %
# %
# \node[align=center, text width=2cm] at (axis cs: 0, 4.0) {\small{sehr\\einfach}};%
# \node[align=center, text width=2cm] at (axis cs: 6, 4.0) {\small{sehr\\schwierig}};%
# \end{axis}%
# \node[text width=5cm, left] at (-2, 0.5) {Inhalt};%
# \end{tikzpicture}'''
#
#
# def test_add_question_multiple_choice_style():
#     y_coord_names = ['du', 'ich', 'er']
#     y_coord_values = [5, 1, 2]
#     question_title = 'I asked something'
#     question = lr.add_question_multiple_choice_style(
#         y_coord_names, y_coord_values, question_title)
#     assert question.dumps() == r'''\begin{tikzpicture}%
# \begin{axis}[xbar, xmin=0, axis lines=left, y axis line style=-, hide x axis, enlargelimits=true, ytick=data, nodes near coords, nodes near coords align={horizontal}, y tick label style={font=\small,text width=9.0cm,align=right}, width=5.0cm, height=7.0cm, symbolic y coords={du, ich, er}]%
# \addplot[fill=blue] coordinates {%
# (5,du)%
# (1,ich)%
# (2,er)%
# };%
# %
# %
# \end{axis}%
# \node[text width=5cm, left] at (-8, 3) {I asked something};%
# \end{tikzpicture}'''
#
#
# def test_yes_no_question():
#     question = lr.add_yes_no_question(3, 4, 'something')
#     assert question.dumps() == r'''\begin{tikzpicture}%
# \begin{axis}[width=10.0cm, height=2.5cm, axis lines=left, ymin=0, nodes near coords, hide y axis, x tick label style={font=\small,text width=1.5cm,align=center}, enlargelimits=true,xtick=data,width3cm,ymin=0,ymax=7,symbolic x coords={Ja, Nein}]%
# \addplot[ybar, fill=blue] coordinates {%
# (Ja,3)%
# (Nein,4)%
# };%
# %
# %
# \end{axis}%
# \node[text width=5cm, left] at (-2, 0.5) {something};%
# \end{tikzpicture}'''


def test_question():
    question = lr.question(axis_options='xbar',
                           coords=[(1, 2), ('ich', 3)],
                           plot_options='ybar',
                           question_title='Title')
    assert question.dumps() == r'''\begin{tikzpicture}%
\begin{axis}[xbar]%
\addplot[ybar] coordinates {%
(1,2)%
(ich,3)%
};%
%
%
\end{axis}%
\node[text width=5cm, left] at (-2, 0.5) {Title};%
\end{tikzpicture}'''


def test__prepare_params_matrix():
    x_coord_names = ['a', 'b', 'c', 'd', 'e', 'f']
    x_coord_values = [6, 1, 1, 0, 0, 0]
    axis_options, coords, plot_options = lr._prepare_params_matrix(
        x_coord_names, x_coord_values)
    assert 'symbolic x coords={a, b, c, d, e, f}' in axis_options
    assert 'ymax=8' in axis_options
    text = 'x tick label style={font=\small,text width=1.5cm,align=center}'
    assert text in axis_options
    assert list(coords) == [('a', 6), ('b', 1), ('c', 1), ('d', 0),
                            ('e', 0), ('f', 0)]


def test__prepare_params_matrix_five_points():
    x_coord_values = [6, 1, 1, 0, 0, ]
    text_left = 'sehr einfach'
    text_right = 'sehr schwierig'
    (axis_options, coords, plot_options, small_left_node_text,
     small_right_node_text, small_node_y) = \
        lr._prepare_params_matrix_five_points(
            x_coord_values, text_left, text_right)
    assert r'extra x tick label={\null}' in axis_options
    assert 'xtick={1,...,5}' in axis_options
    assert 'ymax=8' in axis_options
    assert list(coords) == [(1, 6), (2, 1), (3, 1), (4, 0), (5, 0)]
    assert small_left_node_text == r'\small{sehr\\einfach}'
    assert small_right_node_text == r'\small{sehr\\schwierig}'
    assert small_node_y == 4



