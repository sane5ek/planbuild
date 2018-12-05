from django.db import models
import openpyxl as xlsx
from openpyxl.utils.cell import column_index_from_string
import pyexcel as p

from builder.utils import get_absolute_path


# Create your models here.

class RequestType(models.Model):
    """Model representing a types of requests (e.g. to share your fields)"""
    name = models.CharField(max_length=100)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

class Request(models.Model):
    sender = models.ForeignKey('builder_auth.CustomUser', related_name='Request_sender', null=False, default=0, on_delete=models.CASCADE)
    receiver = models.ForeignKey('builder_auth.CustomUser', related_name='Request_receiver', null=False, default=0, on_delete=models.CASCADE)
    type = models.ForeignKey('builder.RequestType', null=False, default=0, on_delete=models.CASCADE)
    create_date = models.DateField('Date of setting sender request', null=False, default="1998-04-11")
    answer_date = models.DateField('Date of getting receiver answer', null=True, default=None)
    result = models.ForeignKey('builder.RequestResultType', null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return "From {0} to {1} type {2}".format(self.sender, self.receiver, self.type)

class RequestResultType(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Load(models.Model):
    """Model representing a types of loads (e.g. 1_1M)"""
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Post(models.Model):
    """Model representing of a types posts (e.g. Teacher)"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ScienceDegree(models.Model):
    """Model representing a types of science degrees (e.g. )"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ScienceTitle(models.Model):
    """Model representing a types of science titles (e.g. )"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class FieldManager(models.Manager):
    def FillTemplate(self, subjects, courses, diplomas, plan_filename, template_filename):
        plan_path = get_absolute_path(plan_filename)
        template_path = get_absolute_path(template_filename)

class Field(models.Model):
    column_in_load = models.PositiveIntegerField('Column in load')
    column_in_plan = models.PositiveIntegerField('Column in plan')
    name_in_load = models.CharField('Name in load', max_length=100)
    name_in_plan = models.CharField('Name in plan', max_length=100)
    type_of_load = models.ForeignKey('Load', null=False, default=1, on_delete=models.CASCADE)
    owner = models.ForeignKey('builder_auth.CustomUser', null=True, default=None, on_delete=models.SET_NULL)
    load_type = models.BooleanField('Load type', default=False)

    objects = FieldManager()

    def __str__(self):
        return 'Field {0} for {1}'.format(self.name_in_load, self.type_of_load.name)

class Cell(models.Model):
    column = models.PositiveIntegerField('Column')
    row = models.PositiveIntegerField('Row')
    column_span = models.PositiveIntegerField('Column span')
    row_span = models.PositiveIntegerField('Row span')
    advanced = models.CharField('Advanced', max_length=3)
    font_size = models.PositiveSmallIntegerField('Font size')
    direction = models.BooleanField('Direction')

    VERTICAL_ALIGN = (
        ('t', 'Top'),
        ('m', 'Middle'),
        ('b', 'Bottom'),
    )

    HORIZONTAL_ALIGN = (
        ('l', 'Left'),
        ('c', 'Center'),
        ('r', 'Right')
    )

    vertical_align = models.CharField('Vertical align', max_length=1, choices=VERTICAL_ALIGN, blank=True, default='m')
    horizontal_align = models.CharField('Horizontal align', max_length=1, choices=HORIZONTAL_ALIGN, blank=True,
                                        default='h')
    width = models.PositiveIntegerField('Width')
    height = models.PositiveIntegerField('Height')
    value = models.CharField('Value', max_length=500)
    owner = models.ForeignKey('builder_auth.CustomUser', null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return 'Cell {0}:{1} for template'.format(self.column, self.row)

class UploadFile(models.Model):
    file = models.FileField(upload_to='files/%Y/%m/%d')
    owner = models.ForeignKey('builder_auth.CustomUser', null=True, default=None, on_delete=models.SET_NULL)

    def convert_file_to_xlsx(self):
        if self.file.name.endswith('xls'):
            # xls to xlsx
            p.save_book_as(file_name=self.file.name,
                           dest_file_name=self.file.name + 'x')
            self.file.name += 'x'
            self.save()

        elif not str(self.file).endswith('xlsx'):
            raise ValueError('Not Excel file')

class SubjectManager(models.Manager):
    def _get_subjects_start_column(self, worksheet):
        for i in range(1, 15):
            if worksheet['A' + str(i)].value == 'Дисциплина':
                for j in range(i + 1, 20):
                    if worksheet['A' + str(j)].value != None:
                        return j

    def _get_course_and_semester(self, worksheet):
        course = 0
        semester = 0
        for i in worksheet:
            for j in i:
                if j.value == 'Курс':
                    course = j.column
                if j.value == 'Семестр':
                    semester = j.column
        return (course, semester)

    def set_objects_from_excel(self, path, owner):

        #delete old subjects
        self.filter(owner=owner).delete()

        path = get_absolute_path(path)

        wb = xlsx.load_workbook(path, data_only=True)
        ws = wb.active

        subjects_starts = self._get_subjects_start_column(ws)
        # TODO: counting semester in ZAO
        course, semester = self._get_course_and_semester(ws)

        # если ячейка строковая и без цвета - это предмет
        subjects = []
        for i in ws.iter_rows(min_row=subjects_starts, min_col=1, max_col=1):
            if i[0].data_type == 's' and not isinstance(i[0].font.color.rgb, str):
                current_subj = Subject()
                current_subj.row_number = i[0].row
                current_subj.name = i[0].value
                if semester != 0:
                    current_subj.semester = \
                        list(ws.iter_cols(min_col=column_index_from_string(semester), min_row=i[0].row,
                                          max_col=column_index_from_string(semester), max_row=i[0].row))[0][0].value
                    if current_subj.semester is None:
                        current_subj.semester = 0
                else:
                    current_subj.semester = 0
                if course != 0:
                    current_subj.course = \
                        list(ws.iter_cols(min_col=column_index_from_string(course), min_row=i[0].row,
                                          max_col=column_index_from_string(course), max_row=i[0].row))[0][0].value
                    if current_subj.course is None:
                        current_subj.course = 0
                else:
                    current_subj.course = 0
                current_subj.owner = owner
                subjects.append(current_subj)
        self.bulk_create(subjects)

    def get_objects_json(self, owner):
        subjects = self.filter(owner=owner)
        json = []
        for subject in subjects:
            subj = {}
            subj['number'] = subject.row_number
            subj['subject'] = subject.name
            subj['semester'] = subject.semester
            subj['course'] = subject.course
            json.append(subj)
        return json

class Subject(models.Model):
    semester = models.CharField(max_length=3, blank=False)
    course = models.CharField(max_length=3, blank=False)
    name = models.CharField(max_length=50, blank=False)
    row_number = models.IntegerField(null=False)
    owner = models.ForeignKey('builder_auth.CustomUser', null=True, default=None, on_delete=models.SET_NULL)

    objects = SubjectManager()

    def __str__(self):
        return 'Subject {0} for {1} course {2} semester'.format(self.name, self.course, self.semester)
