import xml.etree.ElementTree as ET


class SurveyXML(object):

    def __init__(self, survey_xml_file):
        self.survey_xml_file = survey_xml_file
        self.tree = ET.parse(survey_xml_file)
        self.root = self.tree.getroot()

    def list_items_as_text(self, items, tag='text'):
        items_list = []
        for item in items:
            items_list.append(item.find(tag).text)
        return items_list

    def get_groups(self):
        groups = self.root.findall('section')
        return groups

    def get_group_name(self, group):
        return group.find('sectionInfo').find('text').text

    def get_group_questions(self, group):
        questions = group.findall('question')
        return questions

    def get_question_name(self, question):
        return question.find('text').text

    def get_sub_question_names(self, question):
        sub_questions = question.findall('subQuestion')
        sub_question_names = [sub_question.find('text').text
                              for sub_question in sub_questions]
        return sub_question_names

    def get_response_names(self, question):
        responses = question.iter('label')
        response_names = [response.text for response in responses]
        return response_names

    def get_survey_structure(self):
        structure = []
        for group in self.get_groups():
            group_info = {
                'group_name': self.get_group_name(group),
                'questions': []
            }
            questions = self.get_group_questions(group)
            for question in questions:
                question_info = {
                    'question_name': self.get_question_name(question),
                    'question_responses': self.get_response_names(question),
                    'sub_questions': self.get_sub_question_names(question)
                }
                question_type = self.get_question_type(question_info)
                question_info['question_type'] = question_type
                group_info['questions'].append(question_info)
            structure.append(group_info)
        return structure

    def get_question_type(self, question_info):
        if question_info['sub_questions'] == []:
            if question_info['question_responses'] == [None]:
                question_type = 'text'
            elif question_info['question_responses'] == [
                '1', '2', '3', '4', '5']:
                question_type = 'gesamtnote'
            else:
                if 'Sonstiges' in question_info['question_responses']:
                    question_type = 'multiple_choice'
                elif question_info['question_responses'] == ['Ja', 'Nein']:
                    question_type = 'yes_no'
                else:
                    question_type = 'single_choice'
        else:
            if question_info['question_responses'] == [
                '1', '2', '3', '4', '5']:
                question_type = 'matrix_five_points'
            elif question_info['question_responses'] == ['Ja', 'Nein']:
                question_type = 'yes_no'
            else:
                question_type = 'matrix'
        return question_type