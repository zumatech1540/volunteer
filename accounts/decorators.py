from functools import wraps
from django.shortcuts import redirect


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)

        return redirect('home')

    return wrapper


def leader_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated and request.user.role == 'leader':
            return view_func(request, *args, **kwargs)

        return redirect('home')

    return wrapper


def volunteer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated and request.user.role == 'volunteer':
            return view_func(request, *args, **kwargs)

        return redirect('home')

    return wrapper