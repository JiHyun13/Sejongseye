from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import PloggingGroup, Profile
from .forms import JoinForm, ProfileUpdateForm, GroupJoinForm

# Home view
def home(request):
    return render(request, 'community_templates/home.html')

# Community List View
def community_list(request):
    groups = PloggingGroup.objects.all()
    context = {
        'groups': groups
    }
    return render(request, 'community_templates/community_list.html', context)

# Group Detail View
def group_detail(request, group_id):
    group = get_object_or_404(PloggingGroup, id=group_id)
    form = GroupJoinForm()
    if request.method == 'POST':
        form = GroupJoinForm(request.POST)
        if form.is_valid():
            group.members.add(request.user)
            messages.success(request, '그룹에 가입되었습니다.')
            return redirect('community_list')
    context = {
        'group': group,
        'form': form
    }
    return render(request, 'community_templates/group_detail.html', context)

# Profile View
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필이 성공적으로 업데이트되었습니다.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'form': form
    }
    return render(request, 'community_templates/profile.html', context)

# Join View (Sign Up)
def join(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '회원가입이 완료되었습니다. 로그인해주세요.')
            return redirect('login')
    else:
        form = JoinForm()
    context = {
        'form': form
    }
    return render(request, 'community_templates/join.html', context)
