from datetime import datetime
from kanpai import Kanpai

class ChoiceValidator(Kanpai.Validator):

    def __assert_choice(self, data, attribs):
        if data is None:
            return self.validation_success(data)
        choices = attribs['choices']
        if choices.index(data) > -1:
            return self.validation_success(data)
        else:
            return self.validation_error(data, attribs['error'])
        

    def __init__(self, choices, error="Value not in choice"):
        if not type(choices) == list:
            raise ValueError(
                'value for choices must be a list')
        self.processors = []
        self.processors.append({
            'action': self.__assert_choice,
            'attribs': {
                'error': error,
                'choices': choices
            }
        })


    def __assert_required(self, data, attribs):
        if data is None:
            return self.validation_error(data, attribs['error'])
        return self.validation_success(data)
        

    def required(self):
        self.processors.append({
            'action': self.__assert_required,
            'attribs': {
                'error': 'This field is required'
            }
        })
        return self


class DateValiator(Kanpai.Validator):

    def __assert_date(self, data, attribs):
        if data is None:
            return self.validation_success(data)
        try:
            date = datetime.fromisoformat(data)
            return self.validation_success(date)
        except ValueError:
            return self.validation_error(data, attribs['error'])

    def __init__(self, error="Invalid date"):
        self.processors = []
        self.processors.append({
            'action': self.__assert_date,
            'attribs': {
                'error': error
            }
        })
    
    def __assert_required(self, data, attribs):
        if data is None:
            return self.validation_error(data, attribs['error'])
        return self.validation_success(data)
        

    def required(self):
        self.processors.append({
            'action': self.__assert_required,
            'attribs': {
                'error': 'This field is required'
            }
        })
        return self
