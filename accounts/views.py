# ================= DJANGO CORE =================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from .models import ExpenseLog, EventBudget, EventParticipant
from django.http import JsonResponse

from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import json
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Gallery

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, County, Constituency, Ward, PollingStation
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Count, Q
from .models import User, Event, Task, EventParticipant
from django.db.models import Count, Sum
from .models import Event, Task, User, EventParticipant, EventBudget
import pandas as pd
from django.http import HttpResponse
from django.db.models import Sum
from .models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .models import Voter
from .utils import send_sms
from .utils import send_whatsapp_message
from .models import GroundVoice

from django.shortcuts import render
from .models import Project, Event
from django.contrib.auth.decorators import login_required

from .models import Voter, Ward, SMSLog
from .utils import send_sms
from .forms import EventBudgetForm



# ================= MODELS =================
from .models import (
    User,
    County,
    Constituency,
    Ward,
    PollingStation,
    Event,
    Task,
    TaskMessage,
    Notification,
    Voter
)

# ================= FORMS =================
from .forms import (
    RegisterForm,
    EventForm,
    TaskForm,
    VoterForm
)

# ================= DECORATORS =================
from .decorators import (
    admin_required,
    coordinator_required,
    volunteer_required
)

# ================= UTILITIES =================



def home(request):
    projects = Project.objects.all()
    recent_events = Event.objects.order_by('-date')[:6]

    context = {
        "projects": projects,
        "recent_events": recent_events,
        "total_communities": 10,
        "total_volunteers": 100,
        "total_projects": 25,
    }

    return render(request, "accounts/home.html", context)

# REGISTER




from django.contrib import messages
from django.contrib.auth import login
from .models import User, County, Constituency, Ward, PollingStation


from .models import Constituency

def register_view(request):

    constituencies = Constituency.objects.all()

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        constituency_id = request.POST.get("constituency")
        ward_id = request.POST.get("ward")
        polling_station_id = request.POST.get("polling_station")

        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        volunteer_role = request.POST.get("volunteer_role")
        other_role = request.POST.get("other_volunteer_role")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        user.role = "volunteer"
        user.phone = phone

        user.constituency_id = constituency_id or None
        user.ward_id = ward_id or None
        user.polling_station_id = polling_station_id or None

        user.volunteer_role = volunteer_role
        user.other_volunteer_role = other_role

        user.save()

        login(request, user)
        return redirect("volunteer_dashboard")

    return render(request, "accounts/register.html", {
        "constituencies": constituencies
    })

from django.http import JsonResponse
from .models import Constituency, Ward, PollingStation


def load_constituencies(request):
    county_id = request.GET.get('county_id')
    data = list(Constituency.objects.filter(county_id=county_id).values('id', 'name'))
    return JsonResponse(data, safe=False)


def load_wards(request):
    constituency_id = request.GET.get('constituency_id')
    data = list(Ward.objects.filter(constituency_id=constituency_id).values('id', 'name'))
    return JsonResponse(data, safe=False)


def load_polling_stations(request):
    ward_id = request.GET.get('ward_id')
    data = list(PollingStation.objects.filter(ward_id=ward_id).values('id', 'name'))
    return JsonResponse(data, safe=False)

# LOGIN





def login_view(request):

    if request.method == "POST":

        username = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ================= SAFETY FIX =================
            # Ensure superuser always behaves as admin
            if user.is_superuser:
                user.role = "admin"
                user.save()

            # ================= REDIRECT LOGIC =================
            if user.is_superuser or user.role == "admin":
                return redirect("admin_dashboard")

            elif user.role == "coordinator":
                return redirect("leader_dashboard")

            else:
                return redirect("volunteer_dashboard")

        else:
            messages.error(request, "Invalid login details")

    return render(request, "accounts/login.html")


def about(request):
    return render(request, 'accounts/about.html')

def volunteers(request):
    return render(request, 'accounts/volunteers.html')

def events(request):
    return render(request, 'accounts/events.html')
def vision(request):
    return render(request, 'accounts/vision.html')

def achievements(request):
    return render(request, 'accounts/achievements.html')

def gallery(request):
    return render(request, 'accounts/gallery.html')

def contact(request):
    return render(request, 'accounts/contact.html')

def notifications(request):
    return render(request, 'accounts/notifications.html')


def gallery_view(request):

    gallery_items = Gallery.objects.all()

    return render(request, 'accounts/gallery.html', {
        'gallery_items': gallery_items
    })

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("login")





from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# 🛡️ ADMIN DASHBOARD



@login_required
@admin_required
def admin_dashboard(request):

    users = User.objects.all()
    events = Event.objects.all()
    tasks = Task.objects.all()
    budgets = EventBudget.objects.select_related('event')

    # ================= USERS =================
    total_members = users.count()
    total_voters = users.filter(role='volunteer').count()

    # ================= EVENTS =================
    total_events = events.count()
    pending_events = events.filter(approval_status='pending').count()
    total_attendance = EventParticipant.objects.count()

    # ================= TASKS =================
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    in_progress_tasks = tasks.filter(status='in_progress').count()
    pending_tasks = tasks.filter(status='pending').count()

    # ================= FINANCE (FIXED) =================

    total_budget = budgets.aggregate(
        total=Sum('total_budget')
    )['total'] or 0

    total_spent = sum(b.actual_spent for b in budgets)

    total_variance = total_budget - total_spent

    # ================= CONTEXT =================
    context = {
        'users': users,
        'members': users,
        'total_members': total_members,
        'total_voters': total_voters,

        'events': events,
        'total_events': total_events,
        'pending_events': pending_events,
        'total_attendance': total_attendance,

        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'pending_tasks': pending_tasks,

        # FINANCE FIXED
        'budgets': budgets,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'total_variance': total_variance,
    }

    return render(request, 'accounts/admin_dashboard.html', context)

# 👨‍🏫 LEADER DASHBOARD



@login_required
@coordinator_required
def leader_dashboard(request):

    # ================= EVENTS =================
    events = Event.objects.filter(
        created_by=request.user
    ).order_by('-date')

    total_events = events.count()

    pending_events = events.filter(
        approval_status='pending'
    ).count()

    approved_events = events.filter(
        approval_status='approved'
    ).count()

    # ================= MEMBERS =================
    members = User.objects.filter(
        role__in=['volunteer', 'Coordinator']
    )[:10]

    total_members = User.objects.count()

    # ================= TASKS =================
    tasks = Task.objects.filter(
        assigned_by=request.user
    )

    total_tasks = tasks.count()

    pending_tasks = tasks.filter(
        status='pending'
    ).count()

    in_progress_tasks = tasks.filter(
        status='in_progress'
    ).count()

    completed_tasks = tasks.filter(
        status='completed'
    ).count()

    # ================= VOTERS =================
    total_voters = 0
    supporters = 0
    undecided = 0
    opponents = 0
    ward_analysis = []

    try:
        voters = Voter.objects.all()

        total_voters = voters.count()

        supporters = voters.filter(
            support_status='supporter'
        ).count()

        undecided = voters.filter(
            support_status='undecided'
        ).count()

        opponents = voters.filter(
            support_status='opponent'
        ).count()

        ward_analysis = voters.values(
            'ward__name'
        ).annotate(

            total=Count('id'),

            supporters=Count(
                'id',
                filter=Q(support_status='supporter')
            ),

            undecided=Count(
                'id',
                filter=Q(support_status='undecided')
            ),

            opponents=Count(
                'id',
                filter=Q(support_status='opponent')
            ),
        )

    except:
        pass

    # ================= PROJECTS =================
    projects = []

    try:
        projects = Project.objects.all()[:5]
    except:
        pass

    # ================= NOTIFICATIONS =================
    notifications = [

        "New volunteers registered",

        f"{pending_events} events waiting approval",

        f"{pending_tasks} pending tasks remaining",

    ]

    context = {

        # notifications
        'notifications': notifications,

        # events
        'events': events,
        'total_events': total_events,
        'pending_events': pending_events,
        'approved_events': approved_events,

        # members
        'members': members,
        'total_members': total_members,

        # tasks
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,

        # voters
        'total_voters': total_voters,
        'supporters': supporters,
        'undecided': undecided,
        'opponents': opponents,
        'ward_analysis': ward_analysis,

        # projects
        'projects': projects,
    }

    return render(
        request,
        'accounts/leader_dashboard.html',
        context
    )


# 🙋 VOLUNTEER DASHBOARD

@login_required
def volunteer_dashboard(request):

    user = request.user

    tasks = Task.objects.filter(assigned_to=user).order_by('-created_at')

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status="completed").count()
    pending_tasks = tasks.filter(status="pending").count()

    # progress %
    completed_percent = 0
    if total_tasks > 0:
        completed_percent = round((completed_tasks / total_tasks) * 100, 1)

    events = Event.objects.all().order_by('date')[:5]

    notifications = Notification.objects.filter(user=user).order_by('-created_at')[:10]

    context = {
        "tasks": tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "completed_percent": completed_percent,
        "events": events,
        "notifications": notifications,
    }

    return render(request, "accounts/volunteer_dashboard.html", context)


def events(request):

    if request.user.is_superuser:
        events = Event.objects.all()
    else:
        events = Event.objects.filter(approval_status='approved')

    return render(request, 'accounts/events.html', {
        'events': events
    })
# 🙋                                        create_event
@login_required
def create_event(request):

    if request.user.role not in ['admin', 'coordinator']:
        return redirect('home')

    form = EventForm()

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user

            # 🔥 RULE-BASED APPROVAL SYSTEM
            if request.user.role == 'admin':
                event.approval_status = 'approved'
                event.approved_by = request.user
                event.approved_at = timezone.now()

            elif request.user.role == 'coordinator':
                event.approval_status = 'pending'

            event.save()

            return redirect('events')

    return render(request, 'accounts/create_event.html', {'form': form})

@login_required
@coordinator_required
def leader_create_event(request):

    if request.method == "POST":

        title = request.POST.get("title")
        location = request.POST.get("location")
        date = request.POST.get("date")
        description = request.POST.get("description")

        # 🔥 FIX: get uploaded image
        image = request.FILES.get("image")

        Event.objects.create(
            title=title,
            location=location,
            date=date,
            description=description,
            image=image,   # ✅ ADD THIS LINE

            approval_status="pending",
            created_by=request.user
        )

        return redirect("leader_dashboard")

    return render(request, "accounts/create_event.html")


@login_required
def approve_event(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    event.approval_status = 'approved'
    event.approved_by = request.user
    event.approval_date = timezone.now()
    event.save()

    # TODO: notification system later
    return redirect('admin_dashboard')

@login_required
def reject_event(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    event.approval_status = 'rejected'
    event.rejected_by = request.user
    event.approval_date = timezone.now()
    event.save()

    return redirect('admin_dashboard')


@login_required
def delete_event(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    # optional audit trail
    event.deleted_by = request.user
    event.save()

    event.delete()

    return redirect('admin_dashboard')




from django.utils import timezone

@login_required
def join_event(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    today = timezone.now().date()

    # ❌ EVENT NOT LIVE
    if event.date != today:

        if event.date > today:
            return JsonResponse({
                "success": False,
                "message": "⏳ You can only join this event on the event day."
            })

        else:
            return JsonResponse({
                "success": False,
                "message": "❌ This event has already ended."
            })

    # ✅ CHECK IF ALREADY JOINED
    already_joined = EventParticipant.objects.filter(
        event=event,
        user=request.user
    ).exists()

    if already_joined:
        return JsonResponse({
            "success": False,
            "message": "✔ You already joined this event."
        })

    # ✅ JOIN EVENT
    EventParticipant.objects.create(
        event=event,
        user=request.user
    )

    return JsonResponse({
        "success": True,
        "message": "🎉 Successfully joined live event.",
        "count": EventParticipant.objects.filter(event=event).count()
    })

@login_required
@admin_required
def manage_users(request):

    query = request.GET.get('q')

    if query:
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.all()

    return render(request, 'accounts/manage_users.html', {'users': users})


@login_required
@admin_required
def change_role(request, user_id, role):

    user = get_object_or_404(User, id=user_id)

    user.role = role
    user.save()

    return redirect('manage_users')


@login_required
def delete_user(request, user_id):

    user = get_object_or_404(User, id=user_id)

    # 🚨 safety check: prevent deleting yourself
    if request.user.id == user.id:
        messages.error(request, "You cannot delete your own account.")
        return redirect("manage_users")

    user.delete()

    messages.success(request, "User deleted successfully.")

    return redirect("manage_users")





@login_required
def make_admin(request, user_id):

    user = get_object_or_404(User, id=user_id)

    user.role = "admin"
    user.is_staff = True
    user.is_superuser = False  # keep controlled unless you really want full Django admin access

    user.save()

    return redirect("manage_users")


@login_required
@admin_required
def make_coordinator(request, user_id):

    user = get_object_or_404(User, id=user_id)

    constituencies = Constituency.objects.all()

    if request.method == "POST":

        constituency_id = request.POST.get("constituency")

        if not constituency_id:
            messages.error(request, "Please select constituency")
            return redirect("make_coordinator", user_id=user.id)

        user.role = "coordinator"
        user.managed_constituency_id = constituency_id
        user.save()

        messages.success(request, "Coordinator assigned successfully")
        return redirect("manage_users")

    return render(request, "accounts/assign_coordinator.html", {
        "user": user,
        "constituencies": constituencies
    })


@login_required
@admin_required
def make_volunteer(request, user_id):

    user = get_object_or_404(User, id=user_id)

    user.role = "volunteer"

    user.managed_constituency = None

    user.is_staff = False
    user.is_superuser = False

    user.save()

    messages.success(request, "User changed to volunteer")

    return redirect("manage_users")

@login_required
@admin_required
def assign_task(request):

    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()

            # 🔔 NOTIFICATION (MUST BE INSIDE FUNCTION)
            create_notification(
                user=task.assigned_to,
                title="New Task Assigned",
                message=f"You have been assigned: {task.title}",
                notification_type="task_assigned",
                task=task
            )

            return redirect('admin_dashboard')

    return render(request, 'accounts/assign_task.html', {'form': form})

@login_required
def my_tasks(request):

    tasks = Task.objects.filter(assigned_to=request.user)

    return render(request, 'accounts/my_tasks.html', {'tasks': tasks})



@login_required
def update_task_status(request, task_id, status):

    task = get_object_or_404(Task, id=task_id)

    # 🔐 SECURITY: only assigned user can update
    if task.assigned_to != request.user:
        return redirect('home')

    # 🔒 VALIDATE STATUS (prevents fake URLs like /done123)
    valid_statuses = ['pending', 'in_progress', 'completed']
    if status not in valid_statuses:
        return redirect('my_tasks')

    # ================= UPDATE TASK =================
    task.status = status
    task.save()

    # ================= NOTIFICATIONS =================

    # Notify task creator (leader/admin)
    create_notification(
        user=task.assigned_by,
        title="Task Status Updated",
        message=f"{task.assigned_to.first_name} updated '{task.title}' to {status}",
        notification_type="task_completed" if status == "completed" else "message",
        task=task
    )

    # Optional: notify user when completed
    if status == "completed":
        create_notification(
            user=task.assigned_to,
            title="Task Completed",
            message=f"You marked '{task.title}' as completed",
            notification_type="task_completed",
            task=task
        )

    return redirect('my_tasks')




@login_required
def task_chat(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    # 🔒 Security: only assigned people can access chat
    if request.user != task.assigned_to and request.user != task.assigned_by:
        return redirect('home')

    # ================= SEND MESSAGE =================
    if request.method == "POST":
        message_text = request.POST.get('message')

        if message_text:  # prevent empty messages

            msg = TaskMessage.objects.create(
                task=task,
                sender=request.user,
                message=message_text
            )

            # 🔔 NOTIFY OTHER USER
            other_user = (
                task.assigned_to
                if request.user != task.assigned_to
                else task.assigned_by
            )

            create_notification(
                user=other_user,
                title="New Task Message",
                message=f"Message on: {task.title}",
                notification_type="message",
                task=task
            )

        return redirect('task_chat', task_id=task.id)

    # ================= LOAD CHAT =================
    messages = task.messages.all().order_by('created_at')

    return render(request, 'accounts/task_chat.html', {
        'task': task,
        'messages': messages
    })


def start_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # only assigned user or admin/leader can start
    if request.user != task.assigned_to and not request.user.is_staff:
        messages.error(request, "You are not allowed to start this task.")
        return redirect('my_tasks')

    task.status = 'in_progress'
    task.save()

    messages.success(request, "Task started successfully.")
    return redirect('my_tasks')


def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user != task.assigned_to and not request.user.is_staff:
        messages.error(request, "You are not allowed to complete this task.")
        return redirect('my_tasks')

    task.status = 'completed'
    task.save()

    messages.success(request, "Task marked as completed 🎉")
    return redirect('my_tasks')



def notifications(request):
    notes = Notification.objects.filter(user=request.user)
    return render(request, "accounts/notifications.html", {"notifications": notes})




@login_required
def register_voter(request):

    if request.method == "POST":

        Voter.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST.get('last_name'),
            phone=request.POST['phone'],
            ward_id=request.POST.get('ward'),
            polling_station_id=request.POST.get('polling_station'),
            created_by=request.user
        )

        messages.success(request, "Voter successfully registered!")
        return redirect('leader_dashboard')

    return render(request, 'accounts/register_voter.html', {
        'wards': Ward.objects.all(),
        'stations': PollingStation.objects.all()
    })




@login_required
def voter_dashboard(request):

    user = request.user

    # ================= ACCESS CONTROL =================
    if user.role not in ['admin', 'coordinator']:
        return redirect('home')

    # ================= DATA FILTERING =================
    if user.role == "coordinator":
        voters = Voter.objects.filter(created_by=user)
    else:
        voters = Voter.objects.all()

    # ================= STATS =================
    supporters = voters.filter(support_status="supporter").count()
    undecided = voters.filter(support_status="undecided").count()
    opponents = voters.filter(support_status="opponent").count()

    ward_data = voters.values('ward__name').annotate(
        total=Count('id'),
        supporters=Count('id', filter=Q(support_status='supporter')),
        undecided=Count('id', filter=Q(support_status='undecided')),
        opponents=Count('id', filter=Q(support_status='opponent')),
    )

    return render(request, "accounts/voter_dashboard.html", {
        "voters": voters,
        "supporters": supporters,
        "undecided": undecided,
        "opponents": opponents,
        "ward_data": ward_data,
    })

@login_required
def voter_list(request):

    user = request.user

    if user.role not in ['admin', 'coordinator']:
        return redirect('home')

    if user.role == "coordinator":
        voters = Voter.objects.filter(created_by=user)
    else:
        voters = Voter.objects.all()

    return render(request, 'accounts/voter_list.html', {
        'voters': voters
    })




@login_required
def bulk_sms(request):

    if request.user.role not in ['admin', 'coordinator'] and not request.user.is_superuser:
        messages.error(request, "Access denied")
        return redirect("home")

    wards = Ward.objects.all()

    if request.method == "POST":

        sms_type = request.POST.get("sms_type")

        ward_id = request.POST.get("ward")

        support_status = request.POST.get("support_status")

        individual_phone = request.POST.get("individual_phone")

        message = request.POST.get("message")

        voters = Voter.objects.all()

        # ================= SEND BY WARD =================
        if sms_type == "ward" and ward_id:
            voters = voters.filter(ward_id=ward_id)

        # ================= SUPPORT STATUS =================
        elif sms_type == "supporters":
            voters = voters.filter(
                support_status=support_status
            )

        # ================= INDIVIDUAL =================
        elif sms_type == "individual":

            send_sms(
                [individual_phone],
                message
            )

            messages.success(
                request,
                "SMS sent successfully"
            )

            return redirect("bulk_sms")

        # ================= BULK/PERSONALIZED =================
        phone_numbers = []

        for voter in voters:

            personalized_message = message.replace(
                "{name}",
                voter.full_name
            )

            send_sms(
                [voter.phone_number],
                personalized_message
            )

            phone_numbers.append(voter.phone_number)

        # ================= SAVE LOG =================
        SMSLog.objects.create(
            sender=request.user,
            recipient_count=len(phone_numbers),
            message=message,
            ward_id=ward_id if ward_id else None,
            support_status=support_status
        )

        messages.success(
            request,
            f"SMS sent to {len(phone_numbers)} recipients"
        )

        return redirect("bulk_sms")

    context = {
        "wards": wards
    }

    return render(
        request,
        "accounts/bulk_sms.html",
        context
    )

@login_required
def bulk_whatsapp(request):

    if request.method == "POST":

        message = request.POST.get("message")
        filter_type = request.POST.get("filter")

        # FILTER VOTERS
        if filter_type == "supporter":
            voters = Voter.objects.filter(support_status="supporter")

        elif filter_type == "undecided":
            voters = Voter.objects.filter(support_status="undecided")

        else:
            voters = Voter.objects.all()

        # SEND MESSAGES
        success_count = 0

        for v in voters:
            if v.phone:
                result = send_whatsapp_message(v.phone, message)
                success_count += 1

        return render(request, "accounts/bulk_whatsapp.html", {
            "success_count": success_count
        })

    return render(request, "accounts/bulk_whatsapp.html")





@login_required
@coordinator_required
def voter_analytics_dashboard(request):

    # ================= GLOBAL STATS =================
    total_voters = Voter.objects.count()

    supporters = Voter.objects.filter(support_status='supporter').count()
    undecided = Voter.objects.filter(support_status='undecided').count()
    opponents = Voter.objects.filter(support_status='opponent').count()

    # ================= WARD ANALYSIS =================
    ward_stats = Voter.objects.values('ward__name').annotate(
        total=Count('id'),
        supporters=Count('id', filter=Q(support_status='supporter')),
        undecided=Count('id', filter=Q(support_status='undecided')),
        opponents=Count('id', filter=Q(support_status='opponent')),
    ).order_by('-total')

    # ================= POLLING STATION ANALYSIS =================
    station_stats = Voter.objects.values('polling_station__name').annotate(
        total=Count('id'),
        supporters=Count('id', filter=Q(support_status='supporter')),
        undecided=Count('id', filter=Q(support_status='undecided')),
        opponents=Count('id', filter=Q(support_status='opponent')),
    ).order_by('-total')

    # ================= INSIGHTS =================
    strongest_ward = ward_stats.first()
    weakest_ward = ward_stats.last()

    context = {
        'total_voters': total_voters,
        'supporters': supporters,
        'undecided': undecided,
        'opponents': opponents,

        'ward_stats': ward_stats,
        'station_stats': station_stats,

        'strongest_ward': strongest_ward,
        'weakest_ward': weakest_ward,
    }

    return render(request, 'accounts/leader_charts.html', context)




def download_users_excel(request):

    # Get user data
    users = User.objects.all().values(
        'first_name',
        'last_name',
        'email',
        'username',
        'role',
        'phone'
    )

    # Convert to DataFrame
    df = pd.DataFrame(users)

    # Create response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename=users_data.xlsx'

    # Save Excel file
    df.to_excel(response, index=False)

    return response


def submit_ground_voice(request):

    if request.method == 'POST':

        subject = request.POST.get('subject')
        message = request.POST.get('message')
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        GroundVoice.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=name,
            phone=phone,
            subject=subject,
            message=message
        )

        messages.success(request, 'Grievance submitted successfully.')

        return redirect('submit_ground_voice')

    return render(request, 'accounts/ground_voice.html')

@login_required
def admin_ground_voice(request):

    grievances = GroundVoice.objects.all().order_by('-created_at')

    return render(request, 'accounts/admin_ground_voice.html', {
        'grievances': grievances
    })

def resolve_ground_voice(request, pk):

    grievance = get_object_or_404(GroundVoice, id=pk)

    grievance.status = 'resolved'
    grievance.save()

    return redirect('admin_ground_voice')
    



@login_required
@admin_required
def event_budget_dashboard(request):

    budgets = EventBudget.objects.select_related('event')

    total_budget = sum(b.total_budget for b in budgets)
    total_spent = sum(b.actual_spent for b in budgets)
    total_variance = total_budget - total_spent

    form = EventBudgetForm()

    if request.method == "POST":
        form = EventBudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("event_budget_dashboard")

    return render(request, "accounts/event_budget_dashboard.html", {
        "budgets": budgets,
        "form": form,
        "total_budget": total_budget,
        "total_spent": total_spent,
        "total_variance": total_variance
    })


ALLOWED_FIELDS = ["total_budget"]

@login_required
@admin_required
def update_budget_inline(request, pk):

    budget = get_object_or_404(EventBudget, id=pk)

    if request.method == "POST":

        field = request.POST.get("field")
        value = request.POST.get("value")

        if field in ALLOWED_FIELDS:
            setattr(budget, field, value)
            budget.save()

            return JsonResponse({
                "success": True,
                "field": field,
                "value": value,
                "variance": float(budget.variance),
                "total_spent": float(budget.actual_spent)
            })

    return JsonResponse({"success": False})



from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt



@login_required
def add_expense(request, budget_id):

    budget = get_object_or_404(EventBudget, id=budget_id)

    if request.method == "POST":

        category = request.POST.get("category")

        # if OTHER selected
        if category == "other":
            category = request.POST.get("other_category")

        ExpenseLog.objects.create(
            budget=budget,
            category=category,
            amount=request.POST.get("amount"),
            description=request.POST.get("description"),
            created_by=request.user
        )

        return redirect("event_budget_dashboard")

    return render(request, "accounts/add_expense.html", {
        "budget": budget
    })

@login_required
@admin_required
def approve_expense(request, expense_id):

    expense = get_object_or_404(ExpenseLog, id=expense_id)

    expense.approved = True
    expense.save()

    return redirect("event_budget_dashboard")





from reportlab.pdfgen import canvas
from django.http import HttpResponse

@login_required
def export_event_budget_pdf(request, budget_id):

    budget = get_object_or_404(EventBudget, id=budget_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{budget.event.title}_report.pdf"'

    p = canvas.Canvas(response)

    p.drawString(100, 800, f"EVENT: {budget.event.title}")
    p.drawString(100, 780, f"TOTAL BUDGET: {budget.total_budget}")
    p.drawString(100, 760, f"TOTAL SPENT: {budget.actual_spent}")
    p.drawString(100, 740, f"VARIANCE: {budget.variance}")

    y = 700

    for e in budget.expenses.all():
        p.drawString(100, y, f"{e.category} - {e.amount} - {e.description}")
        y -= 20

    p.showPage()
    p.save()

    return response

@login_required
@admin_required
def create_event_budget(request):

    # GET ALL EVENTS
    events = Event.objects.all()

    if request.method == "POST":

        event_id = request.POST.get("event")
        total_budget = request.POST.get("total_budget")

        print("EVENT ID:", event_id)
        print("TOTAL BUDGET:", total_budget)

        # CHECK EMPTY
        if not event_id:
            return render(request,
                "accounts/create_event_budget.html",
                {
                    "events": events,
                    "error": "Please select event"
                }
            )

        # GET EVENT
        event = get_object_or_404(Event, id=event_id)

        # PREVENT DUPLICATE
        if EventBudget.objects.filter(event=event).exists():

            return render(request,
                "accounts/create_event_budget.html",
                {
                    "events": events,
                    "error": "Budget already exists"
                }
            )

        # CREATE BUDGET
        EventBudget.objects.create(
            event=event,
            total_budget=total_budget
        )

        return redirect("event_budget_dashboard")

    return render(request,
        "accounts/create_event_budget.html",
        {
            "events": events
        }
    )

# views.py




# DISPLAY (ONLY APPROVED FOR VOLUNTEERS)
from django.http import JsonResponse
from .models import Gallery


def gallery(request):

    items = Gallery.objects.filter(is_approved=True)

    return render(request, 'accounts/gallery.html', {
        'gallery_items': items
    })


def upload_gallery(request):

    if request.method == "POST":

        user = request.user
        role = getattr(user, "role", None)

        # ONLY ADMIN + COORDINATOR
        if role not in ["admin", "coordinator"]:
            return JsonResponse({"message": "Permission denied"}, status=403)

        image = request.FILES.get("image")
        video_url = request.POST.get("video_url")
        caption = request.POST.get("description")

        Gallery.objects.create(
            image=image,
            video_url=video_url,
            description=caption,
            uploaded_by=user,
            is_approved=True
        )

        return JsonResponse({"message": "Uploaded successfully"})

    return JsonResponse({"message": "Invalid request"}, status=400)


def delete_gallery(request, pk):

    user = request.user
    role = getattr(user, "role", None)

    if role not in ["admin", "coordinator"]:
        return JsonResponse({"message": "Permission denied"}, status=403)

    Gallery.objects.filter(id=pk).delete()

    return JsonResponse({"message": "Deleted"})