# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from imwievaluation.semester_old import Semester, Lecturer, Lecture


@pytest.fixture
def semester():
    return Semester('WS2017/18')


@pytest.fixture
def lecturers():
    return [
        ('Maier', 'm', 'herr_maier@example.com'),
        ('Müller', 'f', 'frau-mueller@example.com'),
        ('Lastone', 'm', 'mrlastone@example.com'),
        ('one More', 'm', 'onemore@example.com')
    ]


@pytest.fixture
def lectures_by_lecturer():
    return [
        ('Maier', ['Musik macht: schön', 'Alles – manches – nichts']),
        ('Müller', ['You. And me', 'Title / Or something else + more (nice)']),
        ('Lastone', ['A question? Nice title!']),
        ('one More', ['ÄäÖöÜüß, and things like éè'])
    ]

@pytest.fixture
def lecture():
    return Lecture('WS2017/18', 'ÄäÖöÜüß, and things like éè', 'one More', 'y')


@pytest.fixture
def lectures():
    return [
            'Musik macht: schön',
            'Alles – manches – nichts',
            'You. And me',
            'Title / Or something else + more (nice)',
            'A question? Nice title!',
            'ÄäÖöÜüß, and things like éè'
        ]


class TestSemester(object):

    def test_read_survey_file(self, semester, lecturers, lectures,
                              lectures_by_lecturer):
        survey_file = 'tests/testfiles/example_semester_survey.txt'
        semester.read_survey_file(survey_file)
        assert len(semester.lecturers) == len(lecturers)
        for lecturer in semester.lecturers:
            lecturer_info = (lecturer.name, lecturer.gender, lecturer.mail)
            assert lecturer_info in lecturers
        assert semester.lecture_titles() == lectures
        assert semester.lectures[0].with_tutorial is True
        assert semester.lectures[1].with_tutorial is False
        assert semester.lectures[1].lecturer == 'Maier'
        assert semester.lectures[1].term == 'WS2017/18'

        for i, lecturer in enumerate(semester.lecturers):
            lecture_titles = [lecture.title for lecture in lecturer.lectures]
            assert lectures_by_lecturer[i][1] == lecture_titles

    def test_lecturer_names(self, semester, lecturers):
        for lecturer in lecturers:
            name = lecturer[0]
            gender = lecturer[1]
            mail = lecturer[2]
            semester.lecturers.append(Lecturer(name, mail, gender))
        lecturer_names = semester.lecturer_names()
        assert lecturer_names == ['Maier', 'Müller', 'Lastone', 'one More']


def test_lecturer(lecturers):
    for lecturer in lecturers:
        name = lecturer[0]
        gender = lecturer[1]
        mail = lecturer[2]
        lecturer = Lecturer(name, mail, gender)
        assert lecturer.name == name
        assert lecturer.gender == gender
        assert lecturer.mail == mail


class TestLecture(object):

    def test_get_evaluation_title(self, lecture):
        assert lecture.get_evaluation_title() == 'Evaluation ÄäÖöÜüß, and \
things like éè (one More) WS2017/18'

    def test_get_filename(self, lecture):
        assert lecture.get_filename(modus='participants') == 'Teilnehmer_\
AaOoUuss_and_things_like_ee_oneMore_WS201718.csv'
        assert lecture.get_filename(modus='results') == 'Ergebnisse_\
AaOoUuss_and_things_like_ee_oneMore_WS201718.pdf'

    def test_get_participants_from_csv_file(self, lecture):
        csv_file = 'tests/testfiles/example_participants.csv'
        lecture.get_participants_from_csv_file(csv_file)
        assert lecture.participants[0]['email'] == 'dg@example.com'
        assert lecture.participants[2]['lastname'] == 'von Adel'
        assert lecture.participants[1]['firstname'] == 'Anißa'
