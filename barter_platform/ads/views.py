from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from ads.models import Ad, ExchangeProposal
from django.contrib.auth.decorators import login_required
from ads.forms import AdForm, AuthForm, LoginForm, ExchangeForm
from django.db.models import Q
from django.core.paginator import Paginator


def index_page(request):
    return render(request, 'ads/index.html')


def ads_page(request):
    all_ads = Ad.objects.all()
    category = request.GET.get('category')
    condition = request.GET.get('condition')
    search_query = request.GET.get('q', '')

    if category:
        all_ads = all_ads.filter(category=category)

    if condition:
        all_ads = all_ads.filter(condition=condition)

    if search_query:
        all_ads = all_ads.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    paginator = Paginator(all_ads, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ads/ad_list.html', {
        'page_obj': page_obj,
        'category': category,
        'condition': condition,
        'search_query': search_query,
    })


def proposal_page(request):
    proposals = ExchangeProposal.objects.select_related('user', 'ad_sender', 'ad_receiver', 'ad_receiver__user')

    status = request.GET.get('status')
    sender_id = request.GET.get('sender', '')
    receiver_id = request.GET.get('receiver', '')

    if status:
        proposals = proposals.filter(status=status)

    if sender_id:
        proposals = proposals.filter(user__id=sender_id)

    if receiver_id:
        proposals = proposals.filter(ad_receiver__user__id=receiver_id)

    return render(request, 'ads/proposals_list.html', {
        'proposals': proposals,
        'status': status,
        'sender_id': sender_id,
        'receiver_id': receiver_id,
    })


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ads_list')
    else:
        form = AdForm()
    return render(request, 'ads/create_ad.html', {'form': form})


@login_required
def create_proposal(request):
    if request.method == 'POST':
        form = ExchangeForm(request.POST, user=request.user)  # передаём user
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.user = request.user
            proposal.status = 'W'
            proposal.save()
            return redirect('proposals_list')
    else:
        form = ExchangeForm(user=request.user)

    return render(request, 'ads/create_proposal.html', {'form': form})


@login_required
def update_proposal_status(request, pk, status):
    proposal = get_object_or_404(ExchangeProposal, pk=pk)
    if proposal.ad_receiver.user != request.user:
        return redirect('proposals_list')
    if status in ['Y', 'N']:
        proposal.status = status
        proposal.save()
    return redirect('proposals_list')


def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, 'ads/ad_detail.html', {'ad': ad})


@login_required()
def edit_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    if ad.user != request.user:
        messages.error(request, 'Вы можете редактировать только свои объявления')
        return redirect('ads_list')

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление успешно обновлено!')
            return redirect('ads_list')
    else:
        form = AdForm(instance=ad)

    return render(request, 'ads/edit_ad.html', {'form': form, 'ad': ad})


@login_required()
def delete_ad(request, pk):
    ad = Ad.objects.get(pk=pk)

    if ad.user != request.user:
        messages.error(request, 'Вы можете удалять только свои объявления.')
        return redirect('ads_list')
    else:
        ad.delete()
        messages.success(request, 'Объявление успешно удалено.')
        return redirect('ads_list')


def register(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('ads_list')
    else:
        form = AuthForm()
    return render(request, 'ads/registration/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы вошли!')
            return redirect('ads_list')
        else:
            messages.error(request, 'Неправильный логин или пароль.')
            return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'ads/registration/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('ads_list')

