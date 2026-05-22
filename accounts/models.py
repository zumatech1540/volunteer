from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models import Sum




from django.utils import timezone

@property
def category_summary(self):
    return self.expenses.values('category').annotate(
        total=Sum('amount')
    )


image = models.ImageField(upload_to='projects/', blank=True, null=True)
# =====================================================
# LOCATION MODELS
# =====================================================

class County(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Constituency(models.Model):
    county = models.ForeignKey(
        'accounts.County',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Ward(models.Model):
    constituency = models.ForeignKey(
        'accounts.Constituency',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PollingStation(models.Model):
    ward = models.ForeignKey(
        'accounts.Ward',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=150)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class CoordinatorProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    constituency = models.ForeignKey('accounts.Constituency', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - Coordinator"
# =====================================================
# CUSTOM USER MODEL
# =====================================================



class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('coordinator', 'Coordinator'),
        ('volunteer', 'Volunteer'),
    )

    VOLUNTEER_ROLE_CHOICES = (
        ('fundraising', 'Fundraising Support'),
        ('door_to_door', 'Door-to-door Campaign'),
        ('mobilising_voters', 'Mobilising Voters'),
        ('social_media', 'Social Media Support'),
        ('recruiting', 'Recruiting Volunteers'),
        ('materials', 'Distributing Campaign Materials'),
        ('data_collection', 'Data Collection'),
        ('community_listening', 'Community Listening'),
        ('barazas', 'Holding Barazas & Household Meetings'),
        ('other', 'Other'),
    )

    # ================= BASIC =================
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='volunteer'
    )

    phone = models.CharField(max_length=20, blank=True, null=True)

    # ================= LOCATION =================
    county = models.ForeignKey(
        'accounts.County',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    constituency = models.ForeignKey(
        'accounts.Constituency',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    ward = models.ForeignKey(
        'accounts.Ward',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    polling_station = models.ForeignKey(
        'accounts.PollingStation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    managed_constituency = models.ForeignKey(
        'accounts.Constituency',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='coordinators'
    )

    # ================= NEW: VOLUNTEER INTEREST =================
    volunteer_role = models.CharField(
        max_length=50,
        choices=VOLUNTEER_ROLE_CHOICES,
        null=True,
        blank=True
    )

    other_volunteer_role = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    # ================= OPTIONAL PROFILE CONTROL =================
    is_profile_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.username
# =====================================================
# EVENTS
# =====================================================


class Event(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField()

    # 🔥 ADD THIS (IMAGE FIX)
    image = models.ImageField(
        upload_to='events/',
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_events'
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_events'
    )

    approval_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    # ================= AUTO STATUS SYSTEM =================
    @property
    def status(self):
        today = timezone.now().date()

        if self.date > today:
            return "UPCOMING"
        elif self.date == today:
            return "LIVE"
        else:
            return "ENDED"

# =====================================================
# EVENT PARTICIPANTS
# =====================================================

class EventParticipant(models.Model):

    event = models.ForeignKey(
        'accounts.Event',
        on_delete=models.CASCADE,
        related_name='participants'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"


# =====================================================
# TASKS
# =====================================================

class Task(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    title = models.CharField(max_length=200)

    description = models.TextField(
        blank=True,
        null=True
    )

    
    assigned_to = models.ManyToManyField(
    settings.AUTH_USER_MODEL,
    related_name='assigned_tasks'
)

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    event = models.ForeignKey(
        'accounts.Event',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.status})"


# =====================================================
# TASK MESSAGES
# =====================================================

class TaskMessage(models.Model):

    task = models.ForeignKey(
        'accounts.Task',
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='task_messages'
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username} - {self.task.title}"


# =====================================================
# NOTIFICATIONS
# =====================================================

class Notification(models.Model):

    TYPE_CHOICES = (
        ('task_assigned', 'Task Assigned'),
        ('message', 'New Message'),
        ('task_completed', 'Task Completed'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    title = models.CharField(max_length=255)

    message = models.TextField()

    notification_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES
    )

    is_read = models.BooleanField(default=False)

    task = models.ForeignKey(
        'accounts.Task',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


# =====================================================
# VOTERS
# =====================================================

class Voter(models.Model):

    SUPPORT_STATUS = (
        ('supporter', 'Supporter'),
        ('undecided', 'Undecided'),
        ('opponent', 'Opponent'),
    )

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        unique=True
    )

    id_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    ward = models.ForeignKey(
        'accounts.Ward',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voters'
    )

    polling_station = models.ForeignKey(
        'accounts.PollingStation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voters'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_voters'
    )

    support_status = models.CharField(
        max_length=20,
        choices=SUPPORT_STATUS,
        default='undecided'
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}"

# =====================================================
# SMS LOG
# =====================================================
class SMSLog(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    recipient_count = models.IntegerField(default=0)

    message = models.TextField()

    ward = models.ForeignKey(
        Ward,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    support_status = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SMS by {self.sender}"

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    status = models.CharField(max_length=20, default="ongoing")



class EventBudget(models.Model):

    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name="budget"
    )

    total_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.title} Budget"

    @property
    def total_expenses(self):
        return self.expenses.aggregate(
            total=models.Sum('amount')
        )['total'] or 0

    @property
    def actual_spent(self):
        return self.total_expenses

    @property
    def variance(self):
        return self.total_budget - self.actual_spent

    @property
    def category_summary(self):
        return self.expenses.values('category').annotate(
            total=Sum('amount')
        )


        
class ExpenseLog(models.Model):

    CATEGORY_CHOICES = (
        ('transport', 'Transport'),
        ('food', 'Food'),
        ('venue', 'Venue'),
        ('materials', 'Materials'),
        ('other', 'Other'),
    )

    budget = models.ForeignKey(
        EventBudget,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    description = models.CharField(max_length=255)

    receipt = models.ImageField(upload_to="receipts/", blank=True, null=True)

    approved = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # force budget refresh (safe + simple)
        if self.budget_id:
            self.budget.refresh_from_db()

    def __str__(self):
        return f"{self.category} - {self.amount}"

class GroundVoice(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    subject = models.CharField(max_length=255)
    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Gallery(models.Model):

    MEDIA_TYPE = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    title = models.CharField(max_length=255, blank=True, null=True)

    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE, default='image')

    image = models.ImageField(upload_to='gallery/', blank=True, null=True)

    video_url = models.URLField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)  # caption

    uploaded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']