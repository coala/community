#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models


class Student(models.Model):

    identifier = models.IntegerField(primary_key=True)
    display_name = models.CharField(max_length=100)
    program_year = models.ManyToManyField('ProgramYear')

    def __str__(self):
        return self.display_name


class Organization(models.Model):

    identifier = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='', blank=True)
    url = models.URLField(blank=True)
    summary = models.TextField(max_length=300, default='')
    mentors = models.ManyToManyField('Mentor')

    def __str__(self):
        return self.name


class Task(models.Model):

    task_status = (
        (1, 'Draft'),
        (2, 'Published'),
    )

    identifier = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1500)
    status = models.IntegerField(choices=task_status, default=1)
    max_instances = models.IntegerField(default=1)
    mentors = models.ManyToManyField('Mentor')
    tags = models.ManyToManyField('Tag')
    is_beginner = models.BooleanField(default=False)
    categories = models.ManyToManyField('Category')
    time_to_complete_in_days = models.IntegerField(default=3)
    external_url = models.URLField()
    metadata = models.TextField()
    last_modified = models.DateField()
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TaskInstance(models.Model):

    instance_status = (
        (1, 'CLAIMED'),
        (2, 'ABANDONED'),
        (3, 'SUBMITTED'),
        (4, 'NEEDS_WORK'),
        (5, 'OUT_OF_TIME'),
        (6, 'COMPLETED'),
    )

    identifier = models.IntegerField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    status = models.IntegerField(choices=instance_status)
    completion_date = models.DateField()
    deadline = models.DateField()
    modified = models.DateField()

    def __str__(self):
        return self.task+':'+self.student


class ProgramYear(models.Model):

    year = models.IntegerField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.start_date+'-'+self.end_date


class Mentor(models.Model):

    email_id = models.EmailField(primary_key=True)

    def __str__(self):
        return self.email_id


class Tag(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):

    choice = (
        (1, 'Coding'),
        (2, 'User Interface'),
        (3, 'Documentation & Training'),
        (4, 'Quality Assurance'),
        (5, 'Outreach & Research'),
    )
    identifier = models.IntegerField(choices=choice, primary_key=True)

    def __str__(self):
        return str(self.identifier)
