from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

from courses.models import Module


@login_required
def course_chat_room(request, course_id):
    try:
        course = request.user.courses_joined.get(id=course_id)
    except:
        return HttpResponseForbidden
    return render(request, 'chat/room.html', {'course': course})


@login_required
def module_chat_room(request, module_id):
    try:
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__students=request.user)
    except:
        return HttpResponseForbidden
    return render(
        request, 'chat/module_room.html',
        {
            'module': module,
        }
    )
