from project.service.bm_service import insert_data, last_record
from project import db
import random

max_repeat = random.randint(5, 10)

def define_type(function):
    def wrapped(type):
        global max_repeat

        if type == "fine":
            wrapped.calls = 0
            max_repeat = random.randint(5,10)
            return function('fine')

        if type == 'new':
            wrapped.calls += 1
            if wrapped.calls > max_repeat or wrapped.calls == 1:
                return function('new')
            else: 
                return function('repeat')

        if type == 'repeat':
            wrapped.calls += 1
            return function('repeat')

    wrapped.calls = 0
    return wrapped

@define_type
def generate_data(type):
    #import ipdb; ipdb.set_trace()
    data = {}
    if type == 'fine':
        data = {
            'breathing': True,
            'sleeping': True,
            'crying': False,
            'time_no_breathing': 0
        }

    elif type == 'repeat':
        data = last_record()
        if not data['breathing']: 
            data['time_no_breathing'] += 1

    elif type == 'new': 
        data['breathing'] = random.choices([True, False], [1, 0], k=1)[0]
        data['crying'] = False if not data['breathing'] else random.choices([True, False], [1.0, 0.0], k=1)[0]
        data["sleeping"] = False if data['crying'] else random.choices([True, False], [0, 1.0], k=1)[0]
        data['time_no_breathing'] = 0
    insert_data(data)
