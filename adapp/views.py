from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Advertisement
import base64
from django.utils import timezone
from django.db.models import Q


# Create your views here.

def index(request):
    if request.method == 'POST':  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)#查询数据库
        if user is not None:
            login(request, user)
            return redirect('/adapp/')#转换为get
        return redirect('/adapp/?error=true')

    context = {}
    if request.user:
        context['username'] = request.user.username
    if request.GET.get('error', '') != '':
        context['error'] = True
    return render(request, 'index.html', context)


def logout_view(request):
    logout(request)
    return redirect('/adapp/')

def register_view(request):
    if request.method == 'POST':
        User = get_user_model()
        username = request.POST['username']
        if not username:
            return redirect('/adapp/register/?message=用户名不能为空')
        if User.objects.filter(username=username).count():
            return redirect('/adapp/register/?message=用户名存在')
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if not password1:
            return redirect('/adapp/register/?message=密码不能为空')
        if (password1 != password2):
            message = '密码不一致，注册失败'
        else:
            User = get_user_model()
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            message = '注册成功'
        return redirect('/adapp/register/?message='+message) 
    message = request.GET.get('message', '')       
    return render(request, 'register.html', {'message':message})  

def ads_view(request):
    context = {'page': 'ad'}
    if request.user:
        context['username'] = request.user.username
    search = request.GET.get('search', '')   
    #ads = Advertisement.objects.order_by('pub_date')
    #if search:
       # #a = []
        #for a in ads:


    if search:
        ads = Advertisement.objects.filter(Q(owner__username__icontains=search)|Q(text__icontains=search)).order_by('-pub_date')
    else:
        ads = Advertisement.objects.order_by('-pub_date') 
    print (search)
    context['ads'] = ads
    return render(request, 'ads.html', context)

def new_ad_view(request):
    if request.method == 'POST':
        if not request.user:
            return redirect('/adapp/new_ad')
        ad = Advertisement()
        ad.owner = request.user
        ad.text = request.POST.get('text','')
        ad.image = ''
        if request.FILES.get('image', None):
            image_file = request.FILES['image']
            ad.image = base64.b64encode(image_file.read())
        ad.pub_date = timezone.now()    
        ad.save()
        return redirect('/adapp/ads')

    context = {'page': 'ad'}
    if request.user:
        context['username'] = request.user.username
    return render(request, 'new_ad.html', context)

def ad_view(request, ad_id):
    context = {'page': 'ad'}
    if request.user:
        context['username'] = request.user.username
    ads = Advertisement.objects.order_by('-pub_date')
    ad = None
    pre = None
    nxt = None
    counter = 0
    length = len(list(ads))
    for a in ads:
        if a.id == ad_id:
            ad = a
            if counter > 0:
                pre = ads[counter-1]
            if counter < length-1:
                nxt = ads[counter+1]
        counter = counter+1
    context['pre'] = pre
    context['nxt'] = nxt      
    #ad = get_object_or_404(Advertisement, pk=ad_id)
    context['ad'] = ad
    if ad.image:
        context['ad_image'] = "data:image/png;base64,%s" % (ad.image[2:-1],)

    return render(request, 'ad.html', context)

def ad_edit(request, ad_id):
    if request.method == 'POST':
        context = {'page':'ad'}
        ad = get_object_or_404(Advertisement, pk=ad_id)
        ad.owner = request.user
        ad.text = request.POST.get('text', '')
        if request.FILES.get('image', None):
            image_file = request.FILES['image']
            image_str = image_file.read()
            if image_str:
                ad.image = base64.b64encode(image_str)
        ad.save()    
        return redirect('/adapp/ad/' + str(ad_id))
    if request.user:
        context = {'page': 'ad'}
        context['username'] = request.user.username
        ad = get_object_or_404(Advertisement, pk=ad_id)
        context['ad'] = ad
        if ad.image:
            context['ad_image'] = "data:image/png;base64,%s" % (ad.image[2:-1],)
    return render(request, 'edit.html', context)    

def ad_delete(request, ad_id):
    if request.method == 'POST':
        ad = get_object_or_404(Advertisement, pk=ad_id)
        if request.user == ad.owner:
            ad.delete()
            return redirect('/adapp/ads')





         
        

        

    


# To create a new user:
# User = get_user_model()
# user = User.objects.create_user(username, email, password)
# user.save()


