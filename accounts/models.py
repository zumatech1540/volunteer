from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

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


# =====================================================
# CUSTOM USER MODEL
# =====================================================

class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('leader', 'Leader'),
        ('volunteer', 'Volunteer'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='volunteer'
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

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

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
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
        related_name="budget_info"
    )

    estimated_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    actual_spent = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.title} Budget"