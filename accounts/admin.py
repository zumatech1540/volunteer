from django.contrib import admin

from .models import Gallery

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
    Gallery,
)

# ================= USER =================
admin.site.register(User)
admin.site.register(County)
admin.site.register(Constituency)
admin.site.register(Ward)
admin.site.register(PollingStation)


# ================= EVENT =================
admin.site.register(Event)
admin.site.register(EventParticipant)


# ================= TASK =================
admin.site.register(Task)
admin.site.register(TaskMessage)


# ================= NOTIFICATION =================
admin.site.register(Notification)


# ================= VOTER =================
admin.site.register(Voter)


# ================= GROUND VOICE =================
admin.site.register(GroundVoice)



@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'media_type',
        'uploaded_by',
        'is_approved',
        'created_at'
    )

    list_filter = (
        'media_type',
        'is_approved',
        'created_at'
    )

    search_fields = (
        'title',
        'description'
    )

    actions = ['approve_selected']

    def approve_selected(self, request, queryset):
        queryset.update(is_approved=True)