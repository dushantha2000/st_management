{
    'name': "Student Management",   # must needed
    'version': '0.1',    # must needed
    'summary': 'Manage student records',
    'category': 'School',
    'author': 'Dushantha',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/student_views.xml',
        'views/course_views.xml',
        'views/fees_views.xml',
        'views/menu_views.xml',
    ],


    'installable': True,
    'application': True,
}