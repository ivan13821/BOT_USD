
from questions.class_question import Questions


def test():
    print('test')
    return 'testing...'

#(text, callback, comment)
questions = {
    ('Справки', 'references', "справку, Справка"): {
        ('Получить справку', 'references/get_references', "Взять справку"): Questions.references__get_references,
        ('Посмотреть статус справки', 'references/get_status_references', "Когда будет готова справка, статус справки"): test
    },
    ('Кафедра', "department", "кафедры, Кафедру"): {
        ("Кафедра землеустройства", "department/ground", "кафедру"): Questions.department__get_department_ground
    }
}




