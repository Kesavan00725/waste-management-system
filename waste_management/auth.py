from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from mongoengine.errors import DoesNotExist
from .models import User

def require_login(view_func):
    """
    Decorator for views that require the user to be logged in 
    (any role: Admin or Citizen).
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.warning(request, "Please log in to access this page.")
            return redirect('login')
            
        try:
            # Verify user still exists in DB
            user = User.objects.get(id=request.session['user_id'])
            request.user_obj = user # Attach to request for convenience
            return view_func(request, *args, **kwargs)
        except DoesNotExist:
            # Session is stale
            request.session.flush()
            messages.error(request, "Session expired or user deleted. Please log in again.")
            return redirect('login')
            
    return _wrapped_view

def require_admin(view_func):
    """
    Decorator for views that require the user to be an Admin.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')
            
        if request.session.get('role') != 'Admin':
            messages.error(request, "Access Denied: Administrator privileges required.")
            # If they are a citizen trying to access admin routes, bounce to citizen dashboard
            if request.session.get('role') == 'Citizen':
                return redirect('citizen_dashboard')
            return redirect('login')
            
        try:
            user = User.objects.get(id=request.session['user_id'])
            if user.role != 'Admin':
                messages.error(request, "Access Denied.")
                return redirect('citizen_dashboard')
                
            request.user_obj = user
            return view_func(request, *args, **kwargs)
        except DoesNotExist:
            request.session.flush()
            return redirect('login')
            
    return _wrapped_view

def require_citizen(view_func):
    """
    Decorator for views that require the user to be a Citizen.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')
            
        if request.session.get('role') != 'Citizen':
            # If an admin tries to hit a specific citizen route, send them to main dashboard
            if request.session.get('role') == 'Admin':
                return redirect('dashboard')
            return redirect('login')
            
        try:
            user = User.objects.get(id=request.session['user_id'])
            request.user_obj = user
            return view_func(request, *args, **kwargs)
        except DoesNotExist:
            request.session.flush()
            return redirect('login')
            
    return _wrapped_view
