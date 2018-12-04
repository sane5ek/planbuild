from django.db import models

# Create your models here.

class Request(models.Model):
    """Model representing a types of requests (e.g. to share your fields)"""
    name = models.CharField(max_length=100)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
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

class Field(models.Model):

    column_in_load = models.PositiveIntegerField('Column in load')
    column_in_plan = models.PositiveIntegerField('Column in plan')
    name_in_load = models.CharField('Name in load', max_length=100)
    name_in_plan = models.CharField('Name in plan', max_length=100)
    type_of_load = models.ForeignKey('Load', on_delete=models.CASCADE)
    font_size = models.PositiveSmallIntegerField('Font size')
    advanced = models.CharField('Advanced', max_length=3)
    owner = models.ForeignKey('builder_auth.CustomUser', null=True, default=None, on_delete=models.SET_NULL)

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
    horizontal_align = models.CharField('Horizontal align', max_length=1, choices=HORIZONTAL_ALIGN, blank=True, default='h')
    width = models.PositiveIntegerField('Width')
    height = models.PositiveIntegerField('Height')
    value = models.CharField('Value', max_length=500)
    owner = models.ForeignKey('builder_auth.CustomUser', null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return 'Cell {0}:{1} for template'.format(self.column, self.row)

class UploadFile(models.Model):
    file = models.FileField(upload_to='files/%Y/%m/%d')
    owner = models.ForeignKey('builder_auth.CustomUser', null=True, default=None, on_delete=models.SET_NULL)