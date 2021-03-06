from django.contrib import admin
from .models import OHQueue


class OHQueueAdmin(admin.ModelAdmin):
    model = OHQueue
    fieldsets = (
        ('Basic Information:', {'fields': ('name', 'description'), 'description': "name is limited to 32 characters and description is limited to 150 characters"}),
        ('Times Open:', {'fields': ('monday_times', 'tuesday_times', 'wednesday_times', 'thursday_times', 'friday_times', 'saturday_times', 'sunday_times'),
        'description': 'See github.com/mike2151/Online-OH-queue#OHQueueSetUp for how to format schedules.'}),
        ('Additional Information:', {'fields': ('show_ewt',), 'description': "show_ewt: Field that determines whether or not the estimated wait time should show for a queue"}),
    )

admin.site.register(OHQueue, OHQueueAdmin)
