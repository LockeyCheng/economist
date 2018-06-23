from django.shortcuts import render

# Create your views here.
import logging
import json,os
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.db.models import CharField, TextField, FloatField, BigIntegerField, IntegerField,DateTimeField
from django.views.generic import DetailView, ListView, UpdateView, View
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.db.models import Q
from .models import User
from django.utils import timezone
import hashlib
from PIL import Image

logger = logging.getLogger(__name__)

def login_required(func):
    def wrapper(request, *args, **kwargs):
        # 从request中获取登录时保存的nickname
        nickname = request.session.get('nickname', None)
        if nickname:
            request.session.set_expiry(9000)
            return func(request, *args, **kwargs)
        else:
            return redirect('/account/login?next={0}'.format(request.path))
    return wrapper

def super_admin_required(func):
    def wrapper(request, *args, **kwargs):
        # 从request中获取登录时保存的nickname
        nickname = request.session.get('nickname', None)
        user = User.objects.get(pk=nickname) if User.objects.filter(pk=nickname).exists() else None
        if user.role == 'admin':
            return func(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper

def supervisor_required(func):
    def wrapper(request, *args, **kwargs):
        # 从request中获取登录时保存的nickname
        nickname = request.session.get('nickname', None)
        user = User.objects.get(pk=nickname) if User.objects.filter(pk=nickname).exists() else None
        if user.role == 'supervisor' or user.role == 'admin':
            return func(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper

def make_thumb(infile,thumbnail_dir):
    size = (156, 156)
    if not os.path.exists(thumbnail_dir):
        os.mkdir(thumbnail_dir)
    outfile = os.path.join( thumbnail_dir, os.path.basename(infile))
    try:
        im = Image.open(infile)
        im.thumbnail(size)
        im.save(outfile, "JPEG")
        return True
    except IOError as err:
        print("cannot create thumbnail for", infile,err)
        return False

class LoginManager(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        nickname = request.POST['nickname']
        nt_password = request.POST['nt_password']

        user = User.objects.get(pk=nickname) if User.objects.filter(pk=nickname).exists() else None
        pass_auth = False
        if user is not None and user.verify_password(nt_password):
            pass_auth = True
        else:
            return JsonResponse({'result': 'Error', 'message': 'Username or Password is incorrect.'})

class LogoutManager(View):
    @method_decorator(login_required)
    def get(self, request):
        del request.session['nickname']
        return redirect('/account/login/')

class UserProfile(View):
    @method_decorator(login_required)
    def get(self, request):
        nickname = request.session.get('nickname', None)
        user = User.objects.get(pk=nickname) if User.objects.filter(pk=nickname).exists() else None
        return render(request, 'profile.html', {'user': user})

    @method_decorator(login_required)
    def put(self, request):
        """
        Edit user api
        """
        data = json.loads(request.body)
        nickname = request.session.get('nickname', None)
        if not nickname:
            return JsonResponse({'result': 'Error', 'message': 'User Session Error!'})
        try:
            user = User.objects.get(nickname=nickname)#data["nickname"])
        except User.DoesNotExist:
            return self.error("User does not exist")

        user.department = data["department"]
        user.email = data["email"]
        user.password = data["password"]
        try:
            user.save()
        except Exception as err:
            return JsonResponse({'result': 'Error', 'message': str(err)})
        #User.objects.filter(user=user).update(real_name=data["real_name"])
        return JsonResponse({'result': 'Success', 'message': 'Modify Success!'})


class Useravatar(View):
    def __init__(self):
        self.thumbnail_dir = os.path.join(STATIC_ROOT, 'avatar/thumbnails')
        self.dest_dir = os.path.join(STATIC_ROOT, 'avatar/origin_imgs')

    @method_decorator(login_required)
    def post(self, request):
        nickname = request.session.get('nickname', 'default')
        user = User.objects.get(pk=nickname) if User.objects.filter(pk=nickname).exists() else None
        avatarImg = request.FILES['avatar']
        if not os.path.exists(self.dest_dir):
            os.mkdir(self.dest_dir)
        dest = os.path.join(self.dest_dir, nickname+"_avatar.jpg")
        with open(dest, "wb+") as destination:
            for chunk in avatarImg.chunks():
                destination.write(chunk)
        if make_thumb(dest,self.thumbnail_dir):
            avartaPath = os.path.join(STATIC_URL, 'avatar/thumbnails', nickname + "_avatar.jpg")
        else:
            avartaPath = os.path.join(STATIC_URL, 'avatar/origin_imgs', nickname + "_avatar.jpg")

        User.objects.filter(nickname=nickname).update(avatar=avartaPath)
        return render(request, 'profile.html', {'user': user})

class UserList(View):
    @method_decorator(login_required,super_admin_required)
    def get(self, request):
        search = request.GET.get('search', '')
        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10)
        char_fields = [f for f in User._meta.fields if isinstance(f, CharField) or isinstance(f, TextField)]
        queries = [Q(**{f.name + "__contains": search}) for f in char_fields]
        qs = Q()
        for query in queries:
            qs = qs | query
        count = User.objects.filter(qs).count()
        results = User.objects.filter(qs)[int(offset):(int(offset) + int(limit))]
        return JsonResponse({"total": count, "rows": list(results.values())}, safe=False)

class libraryAdmin(View):
    methods = [login_required, super_admin_required]
    @method_decorator(methods)
    def get(self,request):
        nickname = request.session.get('nickname', None)
        user = User.objects.get(pk=nickname) if User.objects.filter(pk=nickname).exists() else None

        return render(request, 'library.html', {'user': user})

class UserAdmin(View):
    methods = [login_required,super_admin_required]
    @method_decorator(methods)
    def post(self, request):
        data = json.loads(request.body)
        user_nickname = data['nickname']
        if User.objects.filter(pk=user_nickname).exists():
            return JsonResponse({'code': '-1', 'message': 'User alreay exist!'})
        new_user = User(
            nickname= user_nickname,
            password = hashlib.md5(data['password']).hexdigest(),
            department=data["department"],
            email=data["email"],
            created_at = timezone.now(),
            role=data["role"]
        )
        try:
            new_user.save()
        except Exception as err:
            return JsonResponse({'code': '-1', 'message': 'Failed to add user.' + str(err)})

        return JsonResponse({'code': '0', 'message': 'New user added!'})


    @method_decorator(methods)
    def put(self, request):
        data = json.loads(request.body)
        try:
            for item in data:
                status = data[item]
                User.objects.filter(nickname=item).update(role=status)
        except Exception as err:
            return JsonResponse({'code': '-1', 'message': 'Modify failed.'+str(err)})
        return JsonResponse({'code': '0', 'message': 'Modify successfully.'})

    @method_decorator(methods)
    def get(self, request):
        """
        User list api / Get user by id
        """
        nickname = request.session.get('nickname', None)
        user = User.objects.get(pk=nickname) if User.objects.filter(pk=nickname).exists() else None
        users = User.objects.all().order_by("-created_at")
        return render(request, 'admin.html', {'users':users, 'user': user})

    def delete_one(self, user_id):
        try:
            user = User.objects.get(nickname=user_id)
            user.delete()
        except User.DoesNotExist:
            return JsonResponse({'code': -1,'message':'invalid params',id:user_id})

    @method_decorator(methods)
    def delete(self, request):
        json_data = json.loads(request.body)
        ids = json_data['ids']
        if not ids:
            return JsonResponse({'code': -1,'message':'invalid params','msg':ids})
        for user_id in ids.split(","):
            if user_id and (user_id !=request.session.get('nickname')):
                try:
                    user = User.objects.get(nickname=user_id)
                    user.delete()
                except Exception as err:
                    return JsonResponse({'code': 1, 'message': 'Delete exception','id':user_id})
        return JsonResponse({'code': 0,'message':'Successfully deleted!'})

