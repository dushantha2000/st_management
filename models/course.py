from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CourseCourse(models.Model):
    _name = 'course.course'
    _description = 'Course Management'


    # log note handling
    _inherit = ['mail.thread', 'mail.activity.mixin']



    name = fields.Char(string='Course Name', required=True, tracking=True)
    code = fields.Char(string='Course Code', required=True, tracking=True)
    description = fields.Text(string='Description')
    duration = fields.Char(string='Duration', help="6 Months, 1 Year" , tracking=True  )

    # Standard price for the course
    standard_price = fields.Float(string='Standard Fee', required=True, tracking=True)

    # List of students enrolled
    student_ids = fields.Many2many('student.student', 'student_course_rel', 'course_id', 'student_id', string='Enrolled Students', tracking=True)

    # Status of the course
    active = fields.Boolean(string='Active', default=True , tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed')
    ], string='Status', default='draft', tracking=True)


    _sql_constraints = [
        ('unique_course_code', 'unique(code)', 'Course Code must be unique!')
    ]

    # status change
    def action_publish(self):
        self.state = 'published'

    def action_close(self):
        self.state = 'closed'
