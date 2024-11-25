
from questions.class_question import Questions


def test():
    print('test')
    return 'testing...'

#(text, callback)
questions = {
    ('Справки', 'references'): {
        ('Получить справку', 'references/get_references'): Questions.references__get_references,
        ('Посмотреть статус справки', 'references/get_status_references'): test
    },
    ('Кафедра', "department"): {
        ("Кафедра землеустройства", "department/ground"): Questions.department__get_department_ground
    }
}




