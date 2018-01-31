from django.db import models
from eventtools.models import BaseEvent, BaseOccurrence


class Gsoc(models.Model):
    count = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.count)


class GsocEvent(BaseEvent):
    title = models.TextField()

    def __str__(self):
        return self.title


class GsocOccurrence(BaseOccurrence):
    event = models.ForeignKey(GsocEvent)

    def __str__(self):
        return self.event


class Program(models.Model):
    year = models.IntegerField(primary_key=True)
    projects_accepted_count = models.IntegerField()
    org_accepted_count = models.IntegerField()
    state = models.CharField(max_length=100)
    is_current = models.BooleanField()
    org_signup_open = models.OneToOneField(GsocEvent, related_name='org_signup_open')
    org_approval = models.OneToOneField(GsocEvent, related_name='org_approval')
    orgs_published = models.OneToOneField(GsocEvent, related_name='org_published')
    student_signup_open = models.OneToOneField(GsocEvent, related_name='student_signup_open')
    slot_request = models.OneToOneField(GsocEvent, related_name='slot_request')
    slot_allocation_grace_period = models.OneToOneField(GsocEvent, related_name='slot_allocation_grace_period')
    project_acceptance = models.OneToOneField(GsocEvent, related_name='project_acceptance')
    project_decisions_finalization = models.OneToOneField(GsocEvent, related_name='project_decisions_finalization')
    first_work_period = models.OneToOneField(GsocEvent, related_name='first_work_period')
    first_evaluations = models.OneToOneField(GsocEvent, related_name='first_evaluations')
    second_work_period = models.OneToOneField(GsocEvent, related_name='second_work_period')
    second_evaluations = models.OneToOneField(GsocEvent, related_name='second_evaluations')
    third_work_period = models.OneToOneField(GsocEvent, related_name='third_work_period')
    final_week = models.OneToOneField(GsocEvent, related_name='final_week')
    final_evaluations_mentor = models.OneToOneField(GsocEvent, related_name='final_evaluations_mentor')
    post_program = models.OneToOneField(GsocEvent, related_name='post_program')
    community_bonding_period = models.OneToOneField(GsocEvent, related_name='community_bonding_period')
    coding_period = models.OneToOneField(GsocEvent, related_name='coding_period')
    results_announced = models.DateField()
    tax_forms_deadline = models.DateField()
    first_payments = models.DateField()
    second_payments = models.DateField()
    final_payments = models.DateField()
    first_evaluations_finalized = models.DateField()
    second_evaluations_finalized = models.DateField()
    final_evaluations_finalized = models.DateField()
    slot_allocation_finalized = models.DateField()
    second_enrollment_form_upload_deadline = models.DateField()
    gsoc = models.ForeignKey(Gsoc, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.year)


class Feature(models.Model):
    program = models.OneToOneField(Program)
    student_finals_can_be_submitted = models.BooleanField()
    org_payment_details_can_be_changed = models.BooleanField()
    admins_can_register = models.BooleanField()
    mentor_first_evals_can_be_submitted = models.BooleanField()
    students_can_edit_project = models.BooleanField()
    tax_forms_can_be_uploaded = models.BooleanField()
    accepted_projects_published = models.BooleanField()
    student_first_evals_can_be_submitted = models.BooleanField()
    second_enrollment_forms_can_be_submitted = models.BooleanField()
    enrollments_can_be_reviewed = models.BooleanField()
    mentor_second_evals_can_be_submitted = models.BooleanField()
    slots_can_be_assigned = models.BooleanField()
    second_eval_emails_can_be_sent = models.BooleanField()
    orgs_can_be_edited = models.BooleanField()
    mentor_finals_can_be_submitted = models.BooleanField()
    slot_allocation_emails_can_be_sent = models.BooleanField()
    projects_can_be_accepted = models.BooleanField()
    enrollments_can_undergo_second_review = models.BooleanField()
    orgs_can_be_accepted = models.BooleanField()
    students_can_register = models.BooleanField()
    second_enrollments_can_be_reviewed = models.BooleanField()
    second_enrollment_forms_can_be_re_submitted = models.BooleanField()
    org_members_can_edit_proposal = models.BooleanField()
    evaluations_in_progress = models.BooleanField()
    proposal_can_be_deleted = models.BooleanField()
    accepted_orgs_published = models.BooleanField()
    results_published = models.BooleanField()
    send_assignee_emails = models.BooleanField()
    org_members_can_view_final_proposals = models.BooleanField()
    orgs_can_register = models.BooleanField()
    student_second_evals_can_be_submitted = models.BooleanField()
    enrollment_forms_can_be_submitted = models.BooleanField()
    project_decisions_emails_can_be_sent = models.BooleanField()
    orgs_can_see_enrollment_status = models.BooleanField()
    proposal_in_progress = models.BooleanField()
    orgs_have_been_accepted = models.BooleanField()
    mentors_can_register = models.BooleanField()
    final_evaluations_emails_can_be_sent = models.BooleanField()
    slots_can_be_requested = models.BooleanField()
    org_accept_reject_emails_can_be_sent = models.BooleanField()
    org_payment_details_visible = models.BooleanField()
    students_can_submit_proposals = models.BooleanField()
    student_withdrawals_trigger_email = models.BooleanField()
    enrollment_forms_can_be_re_submitted = models.BooleanField()
    tax_forms_can_be_reviewed = models.BooleanField()
    first_eval_emails_can_be_sent = models.BooleanField()
    second_review_status_visible = models.BooleanField()
    project_decisions_can_be_finalized = models.BooleanField()
    student_home_address_is_editable = models.BooleanField()

    def __str__(self):
        return str(self.program)


class ProgramStatistic(models.Model):
    program = models.OneToOneField(Program)
    number_of_lines_of_code = models.IntegerField()
    homepage_start_button = models.CharField(max_length=100)
    homepage_intro_paragraph = models.TextField()
    number_of_mentors = models.IntegerField()
    number_of_student_and_mentor_countries = models.IntegerField()
    number_of_years = models.IntegerField()
    homepage_orgs_paragraph = models.TextField()
    homepage_students_paragraph = models.TextField()
    number_of_organizations = models.IntegerField()
    number_of_student_countries = models.IntegerField()

    def __str__(self):
        return str(self.program)


class Technology(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    logo = models.ImageField(upload_to='', blank=True)
    url = models.URLField(blank=True)
    summary = models.TextField(max_length=300, default='')
    technologies = models.ManyToManyField(Technology)
    topics = models.ManyToManyField(Topic)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Mentor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    summary = models.TextField(max_length=300, default='')
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    student = models.OneToOneField(Student)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
