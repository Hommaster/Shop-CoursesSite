import redis
from django.conf import settings
from django.views.generic import ListView
from courses.models import Course


r = redis.Redis(port=settings.REDIS_PORT,
                host=settings.REDIS_HOST,
                db=settings.REDIS_DB)


class MainPage(ListView):
    template_name = 'main/main_page.html'
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.latest('-created')

        #create course ranking
        course_ranking = r.zrange('course_rating', 0, -1,
                                  desc=True)
        course_ranking_ids = [int(id) for id in course_ranking]

        #most viewed course
        most_viewed = list(Course.objects.filter(id__in=course_ranking_ids))
        most_viewed.sort(key=lambda x: course_ranking_ids.index(x.id))

        context['most_viewed'] = most_viewed

        course_content_raking = r.zrange('course_content_rating', 0, -1, desc=True)
        course_content_ranking_ids = [int(id) for id in course_content_raking]
        most_content = list(Course.objects.filter(id__in=course_content_ranking_ids))
        most_content.sort(key=lambda x: course_content_ranking_ids.index(x.id))
        context['most_content'] = most_content

        course_ranking_enroll = r.zrange('course_rating_enroll', 0, -1, desc=True)
        course_ranking_enroll_ids = [int(id) for id in course_ranking_enroll]
        most_enrolled = list(Course.objects.filter(id__in=course_ranking_enroll_ids))
        most_enrolled.sort(key=lambda x: course_ranking_enroll_ids.index(x.id))
        context['most_enrolled'] = most_enrolled

        return context
