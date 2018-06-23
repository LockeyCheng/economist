from userapp.views import login_required, super_admin_required, supervisor_required

from django.shortcuts import render
from userapp.models import User
#@login_required
def index(request):
    nickname = request.session.get('nickname', None)
    user = User.objects.get(pk=nickname) if User.objects.filter(pk=nickname).exists() else None
    return render(request, 'index.html', {'user': user})
