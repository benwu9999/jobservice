# Create your views here.
import logging

from django.db.models import Q
from django.http import HttpResponse
from location_service_api import commute_service_utils
from location_service_api.commute_service_client import CommuteServiceClient
from location_service_api.location_service_client import LocationServiceClient
from user_service_api.provider_profile_service_client import ProviderProfileServiceClient
from user_service_api.user_service_client import UserServiceClient

from admin_site.settings import PROVIDER_PROFILE_SERVICE_URL, LOCATION_SERVICE_URL, COMMUTE_SERVICE_URL, \
    USER_SERVICE_URL
from job_post_app.utils import generate_match
from job_post_app.management.commands.email_client import EmailClient


def index(request):
    return HttpResponse("application service api")


from rest_framework import generics, status
from models import Alert, Query, MONTHLY, WEEKLY, DAILY
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import AlertSerializer

logger = logging.getLogger(__name__)


class AlertConfigList(generics.ListCreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    def post(self, request, *args, **kwargs):
        try:
            alert_d = request.data
            # alert_d['employer_profile_id'] = alert_d.pop('employer_profile')['profile_id']
            # alert_d['location_id'] = alert_d.pop('location')['location_id']
            if 'alert_id' not in alert_d:
                okStatus = status.HTTP_201_CREATED
            else:
                okStatus = status.HTTP_200_OK

            if alert_d['query']['terms']:
                alert_d['query']['terms'] = ','.join(alert_d['query']['terms'])
            else:
                alert_d['query']['terms'] = None

            if alert_d['query']['employer_names']:
                alert_d['query']['employer_names'] = ','.join(alert_d['query']['employer_names'])
            else:
                alert_d['query']['employer_names'] = None

            if alert_d['query']['locations']:
                alert_d['query']['locations'] = ','.join(alert_d['query']['locations'])
            else:
                alert_d['query']['locations'] = None
            query = Query(**alert_d.pop('query'))
            query.save()

            alert_d['query'] = query

            alert = Alert(**alert_d)
            alert.save()

            return Response(AlertSerializer(alert).data, status=okStatus)

        except Exception as e:
            print '%s (%s)' % (e, type(e))
            return Response(e.message)


class AlertConfigDetail(generics.RetrieveUpdateDestroyAPIView):
    # override the default lookup field "PK" with the lookup field for this model
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer


class AlertSearchByIds(APIView):
    permission_classes = ()

    def get(self, request, format=None):
        if 'ids' in request.query_params:
            q = Q(pk__in=request.query_params['ids'].split(','))
            z = AlertSerializer(Alert.objects.filter(q), many=True)
            return Response(z.data)
        return Response([])


class AlertFreqList(APIView):
    frequencies = [DAILY, WEEKLY, MONTHLY];

    def get(self, request, format=None):
        return Response(AlertFreqList.frequencies)


class GenerateEmail(APIView):
    permission_classes = ()

    email_client = EmailClient()
    user_client = UserServiceClient(USER_SERVICE_URL);
    provider_client = ProviderProfileServiceClient(PROVIDER_PROFILE_SERVICE_URL)
    location_client = LocationServiceClient(LOCATION_SERVICE_URL)
    commute_client = CommuteServiceClient(COMMUTE_SERVICE_URL)
    commute_cache = dict()

    def get(self, request, format=None):
        print "generating alerts..."
        data = request.query_params

        alert_freq = data.get('alert_freq', 'daily')

        alerts = self.get_alert(alert_freq)
        alert_ids = [a.alert_id.hex for a in alerts]

        # [user -> [alert_id_1, alert_id_2, ... ]
        user_alerts_d = self.user_client.get_user_and_alerts(alert_ids=alert_ids)

        email_d = dict()
        for v in user_alerts_d.values():
            user = v['user']
            email_d[user['userId']] = user['email']

        queries, query_id_to_user_id_d = self.get_query(user_alerts_d, alerts)

        employer_text = set()
        for q in queries:
            if q.employer_names:
                employer_text.update(q.employer_names)
        employers_by_text_dict = self.provider_client.search_by_text(employer_text, True)

        location_names = set()
        for q in queries:
            if q.locations:
                location_names.update(q.locations)
        location_by_text_dict = self.location_client.search_by_text(location_names, True)

        results = []

        for alert in alerts:
            query = alert.query
            matched_job_posts = generate_match(query, employers_by_text_dict, location_by_text_dict)
            for job_post in matched_job_posts:
                job_post.location_id = job_post.location_id.hex
                job_post.employer_profile_id = job_post.employer_profile_id.hex
            print "final result"
            for m in matched_job_posts:
                print m
            results.append([alert, matched_job_posts])

        results = self.filter_job_posts_with_commute(results)

        location_ids = []
        for result in results:
            query = result[0].query
            location_ids.extend([j.location_id for j in result[1]])
            user_id = query_id_to_user_id_d.get(query.query_id)
            email = email_d.get(user_id)
            result.append(email)

        # get list of location ids from final matched job posts
        locations = self.location_client.get(location_ids)
        location_id_to_location_dict = dict()
        for location in locations:
            location_id_to_location_dict[location['locationId'].replace('-', '')] = location
        for result in results:
            for job_post in result[1]:
                job_post.location = location_id_to_location_dict[job_post.location_id]
        self.process(results)
        return Response(alert_freq)

    def filter_job_posts_with_commute(self, results):
        """
            input - a list of tuple 'result' [(alert1, [matched_job_post1, matched_job_post2...]), ...]

            output - a list of tuple 'result' after filtering out job posts which do not satisfying commute restraint
        """
        origin_to_dests_d = dict()
        location_id_to_result = dict()
        location_id_to_job_post = dict()

        for result in results:
            alert = result[0]
            matched_job_posts = result[1]
            filtered_job_posts = []
            query = alert.query
            if not query.commute:
                filtered_job_posts = matched_job_posts
            else:
                for job_post in matched_job_posts:

                    key = commute_service_utils.get_commute_info_id(query.location_id, job_post.location_id)
                    # if commute already in cache, compared the cached value
                    if key in self.commute_cache and self.commute_less(query, self.commute_cache[key]):
                        self.add_commute(self.commute_cache[key], job_post)
                        filtered_job_posts.append(job_post)
                    # else query commute service and create map of
                    # [location id of job posts -> list of job posts associated with the location id]
                    else:
                        if query.location_id not in origin_to_dests_d:
                            origin_to_dests_d[query.location_id] = list()
                        origin_to_dests_d[query.location_id].append(job_post.location_id)
                        if job_post.location_id not in location_id_to_result:
                            location_id_to_result[job_post.location_id] = []
                        location_id_to_result[job_post.location_id].append(result)
                        if job_post.location_id not in location_id_to_job_post:
                            location_id_to_job_post[job_post.location_id] = []
                        location_id_to_job_post[job_post.location_id].append(job_post)
            result[1] = filtered_job_posts

        if origin_to_dests_d:
            d = self.commute_client.query_pair(origin_to_dests_d)
            for key in d:
                commute = d[key]
                self.commute_cache[key] = commute
                job_post_location_id = key.split('-')[1]
                for result in location_id_to_result[job_post_location_id]:
                    for job_post in location_id_to_job_post[job_post_location_id]:
                        if self.commute_less(result[0].query, commute):
                            self.add_commute(commute, job_post)
                            result[1].append(job_post)
        return results

    def add_commute(self, commute, job_post):
        job_post.transit_commute = commute['transitTime']
        job_post.drive_commute = commute['driveTime']

    def commute_less(self, query, commute_info):
        if query.commute:
            if commute_info['transitTime'] < query.commute or commute_info['driveTime'] < query.commute:
                return True
        return False

    def process(self, results):
        self.email_client.send(results)
        # save(results)
        pass

    def get_alert(self, alert_freq):
        return Alert.objects.filter(frequency=alert_freq)

    def get_query(self, user_alert_dict, alerts):
        """
        :param user_alert_dict: [user -> [alert_id_1, alert_id_2, ...]
        :return:
        """
        alert_id_to_user_id_d = dict()
        for user_id in user_alert_dict.keys():
            v = user_alert_dict[user_id]
            alert_ids = v['alertIds']
            for alert_id in alert_ids:
                alert_id_to_user_id_d[alert_id] = user_id

        query_id_to_user_id_d = dict()
        queries = []
        for alert in alerts:
            query = alert.query
            query.query_id = query.query_id.hex
            query.location_id = query.location_id.hex
            query.profile_id = query.profile_id.hex
            query_id_to_user_id_d[query.query_id] = alert_id_to_user_id_d.get(str(alert.alert_id))
            if query.employer_names:
                query.employer_names = query.employer_names.split(',')
            if query.locations:
                query.locations = query.locations.split(',')
            if query.terms:
                query.terms = query.terms.split(',')
            queries.append(query)
        return queries, query_id_to_user_id_d
