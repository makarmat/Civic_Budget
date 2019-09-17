from django.contrib import admin
from projects.models import Originator, Project, Cost, Voter


# Register your models here.

@admin.register(Originator)
class OriginatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'pesel', 'phone', 'email', 'post_code')
    list_editable = ('phone', 'post_code', 'email')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'end_date', 'region', 'subject', 'description_short',
                    'description_long', 'originator', 'applied', 'comment', 'verified', 'votes')
    list_editable = ('name', 'start_date', 'end_date', 'region', 'subject', 'description_short', 'description_long',
                     'applied', 'comment', 'verified', 'votes')


@admin.register(Cost)
class CostAdmin(admin.ModelAdmin):
    list_display = ('id', 'cost_name', 'grant_cost', 'other_cost', 'whole_cost', 'originator')
    list_editable = ('cost_name', 'grant_cost', 'other_cost', 'whole_cost')


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'pesel', 'phone', 'email', 'post_code')
