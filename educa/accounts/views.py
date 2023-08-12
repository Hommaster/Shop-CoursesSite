from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import DetailView

from .forms import RegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

from courses.models import Course


def registrate(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request,
                          'account/registrate_done.html',
                          {'new_user': new_user})
        else:
            return render(request,
                          'account/registrate.html',
                          {'user_form': user_form}
                          )
    else:
        user_form = RegistrationForm()
        return render(request,
                      'account/registrate.html',
                      {'user_form': user_form}
                      )


@login_required
def edit(request):
    if request.method == 'POST':
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


class ProfileView(DetailView):
    model = Profile
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.filter(students=self.request.user)
        context['courses'] = courses
        count = Profile.objects.annotate(
            total_courses=Count('course')
        )
        context['count_course'] = count
        return context
