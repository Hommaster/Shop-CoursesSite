from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

from .models import PaymentCourses

from courses.models import Module
from django.urls import reverse

import stripe as stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    payment_id = request.session.get('payment_id')
    payment = get_object_or_404(
        PaymentCourses,
        id=payment_id,
    )
    modules = Module.objects.filter(course=payment.coursep)
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        session_data = {
            'mode': 'payment',
            'client_reference_id': payment_id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': [],
        }
        session_data['line_items'].append(
            {
                'price_data': {
                    'unit_amount': int(payment.price),
                    'currency': 'usd',
                    'product_data': {
                        'name': payment.coursep.title
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
