from django.http.response import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Articles, Biography, ClickLog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ArticleForm, BiographyForm_, UsernameForm
from django.views.generic import View
from .models import VerifiedUser
from django.db.models import Count
from django.contrib import messages
from django.db.models import Model
from django.contrib.auth.decorators import login_required
#from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.utils import timezone



# Create your views here.

def starting_page(request):
    all_posts = Articles.objects.all().order_by("-created_at")
    paginator = Paginator(all_posts, 10)
    
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        
    return render(request, "blog_write/starting_page.html", {
        "page_obj": page_obj
    })
    
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_click(request, click_by_type, url):
    ip_address = get_client_ip(request)  # Use the function to get the correct client IP
    new_click = ClickLog(ip_address=ip_address, url=url, click_by_type=click_by_type)
    try:
        new_click.save()
    except Exception as e:
        print(f'Error saving click log: {e}')

    
def full_article(request, slug):
    article_full = get_object_or_404(Articles, slug=slug)
    log_click(request, click_by_type='Article', url=request.build_absolute_uri())
    return render(request, "blog_write/full_article.html", {
        "article_full": article_full,
        "article_tags": article_full.tags.all()
    })
    
def top_five(request):
    latest_articles = Articles.objects.all().order_by("-created_at")[:5]
    return render(request, "blog_write/full_article.html", {
        "latest_articles": latest_articles
    })
    
def about(request):
    biography_full = Biography.objects.all()
    log_click(request, click_by_type='Article', url=request.build_absolute_uri())
    return render(request, "blog_write/about.html",{
        'biography_full': biography_full
    })

def article_create_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('full_article')
        else:
            form = ArticleForm()
        return render(request, 'full_article.html', {'form': form})

def numra(request):
    form = UsernameForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        try:
            master_username = VerifiedUser.objects.order_by('pk').first().user
        except AttributeError:
            master_username = None
        if username == master_username:
            request.session['verified_for_statistika'] = True
            request.session.set_expiry(210)  
            return redirect('statistika')
        else:
            messages.error(request, "Access denied. Incorrect username.")
    else:
        messages.error(request, "Please submit the form correctly.")
    return render(request, 'blog_write/numra.html', {'form': form})


class StatistikaView(View):
    def get(self, request, *args, **kwargs):
        if not request.session.get('verified_for_statistika', False):
            messages.error(request, "Please verify your user status to view statistics.")
            return redirect('numra')
        else:
            clicks_by_type = ClickLog.objects.values('click_by_type').annotate(total=Count('click_by_type')).order_by('-total')
            individual_clicks = ClickLog.objects.all().order_by('-timestamp')
            clicks_by_ip = ClickLog.objects.values('ip_address').annotate(total=Count('ip_address')).order_by('-total')
            
            paginator = Paginator(individual_clicks, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            return render(request, 'blog_write/statistika.html', {
                'clicks_by_type': clicks_by_type,
                'individual_clicks': individual_clicks,
                'clicks_by_ip': clicks_by_ip, 
                'page_obj': page_obj
            })
                       
@require_POST
def logout_view(request):
    request.session.flush()
    messages.info(request, "You have been successfully logged out.")
    return redirect('starting-page') 





