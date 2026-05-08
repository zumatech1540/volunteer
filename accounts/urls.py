from django.urls import path
from . import views

urlpatterns = [

    # AUTH
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # DASHBOARDS
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('leader-dashboard/', views.leader_dashboard, name='leader_dashboard'),
    path('volunteer-dashboard/', views.volunteer_dashboard, name='volunteer_dashboard'),

    # PAGES
    path('about/', views.about, name='about'),
    path('volunteers/', views.volunteers, name='volunteers'),
    path('events/', views.events, name='events'),
    path('contact/', views.contact, name='contact'),

    # USERS / VOTERS
    path('manage-users/', views.manage_users, name='manage_users'),
    path('voter-list/', views.voter_list, name='voter_list'),
    path('voter-analytics/', views.voter_analytics_dashboard, name='voter_analytics'),
    path('register-voter/', views.register_voter, name='register_voter'),
    path('leader-charts/', views.voter_analytics_dashboard, name='leader_charts'),

    # AJAX
    path('ajax/constituencies/', views.load_constituencies, name='load_constituencies'),
    path('ajax/wards/', views.load_wards, name='load_wards'),
    path('ajax/polling/', views.load_polling_stations, name='load_polling'),

    # EVENTS
    path('create-event/', views.create_event, name='create_event'),
    path('leader-create-event/', views.leader_create_event, name='leader_create_event'),

    # TASKS
    path('assign-task/', views.assign_task, name='assign_task'),
    
    path('my-tasks/', views.my_tasks, name='my_tasks'),

    # NOTIFICATIONS
    path('notifications/', views.notifications, name='notifications'),
    path('bulk-sms/', views.bulk_sms, name='bulk_sms'),
    path('bulk-whatsapp/', views.bulk_whatsapp, name='bulk_whatsapp'),

    # OPTIONAL MISSING ROUTES (FIX YOUR ERRORS)
    path('admin-events-review/', views.events, name='admin_events_review'),

    path('download-users-excel/', views.admin_dashboard, name='download_users_excel'),

    path('user-tasks/<int:user_id>/', views.my_tasks, name='user_tasks_admin'),
    path('make-admin/<int:user_id>/', views.make_admin, name='make_admin'),
    path('make-leader/<int:user_id>/', views.make_leader, name='make_leader'),
    path('make-volunteer/<int:user_id>/', views.make_volunteer, name='make_volunteer'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path(
    'leader-charts/',
    views.voter_analytics_dashboard,
    name='leader_charts'
),
]