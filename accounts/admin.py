from django.contrib import admin 
from .models import (
    User,
    County,
    Constituency,
    Ward,
    PollingStation,
    Event,
    EventParticipant,
    Task,
    TaskMessage,
    Notification,
    Voter,
    GroundVoice,
)


admin.site.register(User)
admin.site.register(County)
admin.site.register(Constituency)
admin.site.register(Ward)
admin.site.register(PollingStation)
admin.site.register(Event)
admin.site.register(EventParticipant)
admin.site.register(Task)
admin.site.register(TaskMessage)
admin.site.register(Notification)
admin.site.register(Voter)
admin.site.register(GroundVoice)