import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from accounts.models import Profile
from courses.models import Course

from .models import PaymentCourses
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
                payment_course = PaymentCourses.objects.get(id=session.client_reference_id)
                course = get_object_or_404(
                    Course,
                    id=payment_course.coursep.id
                )
                profile = get_object_or_404(
                    Profile,
                    id=payment_course.profilep.id
                )
            except Profile.DoesNotExist or Course.DoesNotExist:
                return HttpResponse(status=400)
            profile.course.add(course)
            profile.save()
            payment_course.paid = True
            payment_course.save()
            course.students.add(profile.user)
            course.save()
            payment_completed.delay(course.id, profile.id)

    return HttpResponse(status=200)
