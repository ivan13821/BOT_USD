
from questions.class_question import Questions


def test():
    print('test')
    return 'testing...'







#(func, name, comment)
end_func = {
    'references/get_references': (Questions.references__get_references, 'Получить справку'),
    'references/get_status_references': (test, 'Посмотреть статус справки'),
    
    "department/ground": (Questions.department__get_department_ground, "Кафедра землеустройства"),
    "department/economik": (Questions.department__get_department_economik, "Кафедра экономики"),
    "department/social": (Questions.department__get_department_social, "Кафедра социалогии"),
    "department/math": (Questions.department__get_department_math, "Кафедра математики"),
    "department/info": (Questions.department__get_department_info, "Кафедра информатики"),
}









#(text, callback)
questions = {
    ('Справки', 'references'): {
        ('Получить справку', 'references/get_references'): end_func['references/get_references'],
        ('Посмотреть статус справки', 'references/get_status_references'): end_func['references/get_status_references']
    },
    ('Кафедра', "department", "кафедры, Кафедру"): {
        ("Кафедра землеустройства", "department/ground"): end_func["department/ground"],
        ("Кафедра экономики", "department/economik"): end_func["department/economik"],
        ("Кафедра социалогии", "department/social"): end_func["department/social"],
        ("Кафедра математики","department/math"): end_func["department/math"],
        ("Кафедра информатики", "department/info"): end_func["department/info"],
    }
}



