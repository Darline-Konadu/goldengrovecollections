from django.contrib import messages
from django.shortcuts import redirect

class MustLogin:
    def __init__(self, view_func):
        self.view_func = view_func

    def __call__(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to view this page')
            return redirect('accounts:login')
        return self.view_func(request, *args, **kwargs)