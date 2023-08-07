from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages

from .forms import RegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


def registrate(request,):
    if request.methods == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/registrate_done.html',
                          {'new_user': new_user})
    else:
        user_form = RegistrationForm()
        return render(request,
                      'account/registrate.html',
                      {'user_form': user_form}
                      )


@login_required
def edit(request):
    if request.methods == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно изменён!')
        else:
            messages.error(request, 'Произошла ошибка при изменении данных, проверьте введенные данные!')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',
                  {
                      'user_form': user_form,
                      'profile_form': profile_form,
                  })
