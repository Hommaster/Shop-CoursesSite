import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from accounts.models import Profile
from courses.models import Course

from .models import Payment
from .tasks import payment_completed


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                profile = Profile.objects.get(id=session.client_reference_id)
                course = Course.objects.get(id=session.course_reference_id)
            except Profile.DoesNotExist or Course.DoesNotExist:
                return HttpResponse(status=400)
            payment = get_object_or_404(
                Payment,
                profile=profile,
                course=course
            )
            profile.course = course
            profile.save()
            payment.paid = True
            payment.save()
            payment_completed.delay(course.id, profile.id)

    return HttpResponse(status=200)
