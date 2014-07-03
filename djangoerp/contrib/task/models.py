#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from djangoerp.models import ERPModel
from djangoerp.fields import WorkflowField
from djangoerp.settings import BASE_MODULE
from django.utils.timezone import now
from djangoerp.categories import PROJECT

from .workflows import GoalWorkflow
from .workflows import TaskWorkflow

from math import floor

@python_2_unicode_compatible
class AbstractGoal(ERPModel):
    """
    """
    state = WorkflowField()

    project = models.ForeignKey(BASE_MODULE["PROJECT"], null=True, blank=True)
    referee = models.ForeignKey(BASE_MODULE["EMPLOYEE"], null=True, blank=True)

    summary = models.CharField(_("Summary"), max_length=255, null=True, blank=False, )
    description = models.TextField(_("Description"), null=True, blank=True, )

    billable = models.BooleanField(_("Is billable"), default=False)
    completed = models.BooleanField(_("Completed"), default=False, editable=False)

    class Meta(ERPModel.Meta): # only needed for abstract models
        verbose_name = _('Goal')
        verbose_name_plural = _('Goals')
        ordering = ['project__name','summary']
        abstract = True


    def erpget_customer(self):
        if self.project:
            return self.project.customer
        return None


    def erpget_project(self):
        return self.project


    def __str__(self):
        return '#%s: %s' % (self.pk, self.summary)


    def get_states(self):
        active_states = 0
        states = {
            "hold": 0.,
            "review": 0.,
            "done": 0.,
        }

        for state, count in self.task_set.values_list('state').annotate(count=models.Count('state')).order_by():
            if state in ["new","open","started"]:
                active_states += count

            if state in ["hold",]:
                states["hold"] += count
                active_states += count

            if state in ["review",]:
                states["review"] += count
                active_states += count

            if state in ["finished",]:
                states["done"] += count
                active_states += count

        if active_states == 0:
          return states

        states['hold'] = '%4.2f' % (floor(10000*states["hold"]/active_states)/100)
        states['done'] = '%4.2f' % (floor(10000*states["done"]/active_states)/100)
        states['review'] = '%4.2f' % (floor(10000*states["review"]/active_states)/100)

        return states


    class ERPMeta:
        has_logging = False
        category = PROJECT
        workflow = GoalWorkflow
        workflow_field = 'state'


class Goal(AbstractGoal):
    pass


@python_2_unicode_compatible
class AbstractTask(ERPModel):
    """
    """

    state = WorkflowField()

    project = models.ForeignKey(BASE_MODULE["PROJECT"], null=True, blank=True)
    employee = models.ForeignKey(BASE_MODULE["EMPLOYEE"], null=True, blank=True)

    goal = models.ForeignKey(BASE_MODULE["GOAL"], null=True, blank=True)

    summary = models.CharField(_("Summary"), max_length=255, null=True, blank=False, )
    description = models.TextField(_("Description"), null=True, blank=True, )

    due_date = models.DateField(_('Due date'), null=True, blank=True)

    work_date = models.DateTimeField(null=True, editable=False)
    seconds_on = models.PositiveIntegerField(null=True, default=0, editable=False)
    completed = models.BooleanField(_("Completed"), default=False, editable=False)


    class Meta(ERPModel.Meta): # only needed for abstract models
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['due_date', 'summary']
        abstract = True

    def __str__(self):
        return '#%s: %s' % (self.pk, self.summary)

    def clean(self):
        # overwrite the project with the goals project
        if self.goal:
            self.project = self.goal.project

    def get_project_queryset(self, qs):
        if self.goal:
            return qs.filter(goal=self.goal)
        else:
            return qs

    def get_goal_queryset(self, qs):
        if self.project:
            return qs.filter(project=self.project)
        else:
            return qs

    def due_days(self):
        if self.due_date:
            time = now().date()
            if time >= self.due_date:
                return 0
            return (self.due_date - time).days

    class ERPMeta:
        has_files = True
        has_comments = True
        workflow = TaskWorkflow
        workflow_field = 'state'
        category = PROJECT


class Task(AbstractTask):
    pass
