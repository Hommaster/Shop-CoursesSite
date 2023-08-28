from django.shortcuts import render, get_object_or_404, redirect

from .models import Payment

from accounts.models import Profile
from courses.models import Course
from django.urls import reverse

import stripe as stripe


def payment_process(request):
    profile_id = request.session.get('profile_id')
    course_id = request.session.get('course_id')
    profile = get_object_or_404(
        Profile,
        id=profile_id
    )
    course = get_object_or_404(
        Course,
        id=course_id
    )
    pay_course = get_object_or_404(
        Payment,
        course=course,
        profile=profile
    )
    if request.method == 'POST':
        success_url = request.build_success_uri(reverse('payment:completed'))
        cancel_url = request.build_cancel_uri(reverse('payment:canceled'))
        session_data = {
            'mode': 'payment',
            'client_reference_id': profile_id,
            'course_reference_id': course_id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        session_data['line_items'].append(
            {
                'price_data': {
                    'unit_amount': int(pay_course.price),
                    'currency': 'usd',
                    'product_data': {
                        'name': course.title
                    },
                },
                'quantity': 1,
            }
        )
        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
