import operator

from django.core.management.base import BaseCommand
from location_service_api import commute_service_utils
from location_service_api.commute_service_client import CommuteServiceClient
from location_service_api.location_service_client import LocationServiceClient
from user_service_api.provider_profile_service_client import ProviderProfileServiceClient
from user_service_api.user_service_client import UserServiceClient

from alert_app.models import Alert, DAILY
from job_post_app.models import JobPost
# run custom admin command like this:
# cd ~/job-post-service/JobPostService && python manage.py generate_alert
from management.commands.email_client import EmailClient
from job_post_app.utils import generate_match
from collections import defaultdict


class Result(object):

    def __init__(self, id, alert=None, job_posts=None, email=None, user_id=None):
        self.id = id
        self.alert = alert
        self.job_posts = job_posts
        self.email = email
        self.user_id = user_id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Command(BaseCommand):
    help = 'generate alerts'

    commute_cache = dict()
    user_client = None
    provider_client = None
    location_client = None
    commute_client = None

    email_client = EmailClient()

    user_id_cmd = 'user_id'
    user_service_url_cmd = 'user_service_url'
    job_post_service_url_cmd = 'job_post_service_url'
    provider_profile_service_url_cmd = 'provider_profile_service_url'
    location_service_url_cmd = 'location_service_url'
    commute_service_url_cmd = 'commute_service_url'
    alert_freq_cmd = 'alert_freq'

    def add_arguments(self, parser):
        parser.add_argument(self.user_id_cmd, nargs='?', type=str, default=None)
        parser.add_argument(self.user_service_url_cmd, nargs='?', type=str, default=None)
        parser.add_argument(self.job_post_service_url_cmd, nargs='?', type=str, default=None)
        parser.add_argument(self.provider_profile_service_url_cmd, nargs='?', type=str, default=None)
        parser.add_argument(self.location_service_url_cmd, nargs='?', type=str, default=None)
        parser.add_argument(self.commute_service_url_cmd, nargs='?', type=str, default=None)
        parser.add_argument(self.alert_freq_cmd, nargs='?', type=str, default=DAILY)
        pass

    def handle(self, *args, **options):
        print "generating alerts..."

        url = options[self.user_service_url_cmd]
        self.user_client = UserServiceClient(url)

        url = options[self.provider_profile_service_url_cmd]
        self.provider_client = ProviderProfileServiceClient(url)

        url = options[self.location_service_url_cmd]
        self.location_client = LocationServiceClient(url)

        url = options[self.commute_service_url_cmd]
        self.commute_client = CommuteServiceClient(url)

        alert_freq = options[self.alert_freq_cmd]

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
            if matched_job_posts:
                results.append(Result(alert.alert_id.hex, alert, matched_job_posts))

        self.add_default_commute_info(results)
        results = self.filter_job_posts_with_commute(results)

        location_ids = []
        for result in results:
            query = result.alert.query
            location_ids.extend([j.location_id for j in result.job_posts])
            if query.location_id is not None:
                location_ids.append(query.location_id)
            user_id = query_id_to_user_id_d[query.query_id]
            email = email_d[user_id]
            result.email = email
            result.user_id = user_id

        # get list of location ids from final matched job posts
        locations = self.location_client.get(location_ids)
        location_id_to_location_dict = dict()
        for location in locations:
            location_id_to_location_dict[location['locationId'].replace('-', '')] = location
        for result in results:
            result.alert.query.location = location_id_to_location_dict[result.alert.query.location_id]
            for job_post in result.job_posts:
                job_post.location = location_id_to_location_dict[job_post.location_id]
        self.process(results)
        print "finished generating alerts"

    def add_default_commute_info(self, results):
        for result in results:
            for job_post in result.job_posts:
                job_post.transit_commute = 'N/A'
                job_post.drive_commute = 'N/A'

    # def generate_match(self, query, employers_by_text_dict, location_by_text_dict):
    #     qs = list()
    #
    #     query_set = JobPost.objects.all()
    #
    #     terms = query.terms
    #     if terms:
    #         full_text_search_terms = ' +'.join(terms)
    #         query_set = JobPost.full_text_search_objects.search(full_text_search_terms)
    #
    #     employer_names = query.employer_names
    #     if employer_names:
    #         # custom lookup
    #         employer_ids = self.get_employer_ids(employer_names, employers_by_text_dict)
    #         # https: // dev.mysql.com / doc / refman / 5.5 / en / fulltext - boolean.html
    #         qs.append(Q(**{'employer_profile_id__in': employer_ids}))
    #         # i.e. MATCH (employer_profile_id) AGAINST (e1 e2 e3 IN BOOLEAN MODE)
    #         # match either e1 e2 OR e3
    #
    #     location_names = query.locations
    #     if location_names:
    #         # custom lookup
    #         location_ids = self.get_location_ids(location_names, location_by_text_dict)
    #         qs.append(Q(**{'location_id__in': location_ids}))
    #         # d['title,description__search'] = ' +'.join(terms)
    #         # full text search of keywords,
    #         # i.e. MATCH (title,description) AGAINST (k1 +k2 +3 IN BOOLEAN MODE)
    #         # match k1 k2 AND k3
    #
    #     if query.last_updated:
    #         qs.append(Q(**{'modified__gte': query.last_updated_w_tz()}))
    #
    #     # if query.compensation and query.compensation_unit:
    #     #     d['compensation_amount__range'] = (query.compensation[0], query.compensation[1])
    #     #     d['compensation_duration'] = query.compensation_unit
    #     # if query.updated:
    #     #     d['modified__gt'] = query.updated
    #     # if query.has_contact != None:
    #     #     d['has_contact'] = query.has_contact
    #
    #     matched_job_posts = query_set.filter(reduce(operator.and_, qs))
    #     for job_post in matched_job_posts:
    #         job_post.location_id = job_post.location_id.hex
    #         job_post.employer_profile_id = job_post.employer_profile_id.hex
    #     return matched_job_posts

    def filter_job_posts_with_commute(self, results):
        """
            input - a list of tuple 'result' [(alert1, [matched_job_post1, matched_job_post2...]), ...]

            output - a list of tuple 'result' after filtering out job posts which do not satisfying commute restraint
        """
        origin_to_dests_d = defaultdict(set)
        alert_location_id_to_result = defaultdict(set)
        location_id_to_job_post = defaultdict(set)

        for result in results:
            alert = result.alert
            matched_job_posts = result.job_posts
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
                        origin_to_dests_d[query.location_id].add(job_post.location_id)
                        alert_location_id_to_result[alert.query.location_id].add(result)
                        location_id_to_job_post[job_post.location_id].add(job_post)
            result.job_posts = filtered_job_posts

        if origin_to_dests_d:
            for k in origin_to_dests_d:
                origin_to_dests_d[k] = list(origin_to_dests_d[k])
            d = self.commute_client.query_pair(origin_to_dests_d)
            for key in d:
                commute = d[key]
                self.commute_cache[key] = commute
                ele = key.split('-')
                alert_location_id = ele[0]
                job_post_location_id = ele[1]
                print('***' + job_post_location_id)
                for result in alert_location_id_to_result[alert_location_id]:
                    for job_post in location_id_to_job_post[job_post_location_id]:
                        if self.commute_less(result.alert.query, commute):
                            self.add_commute(commute, job_post)
                            print(result.alert.alert_id.hex + " " + job_post.job_post_id.hex)
                            result.job_posts.append(job_post)
        return results

    def add_commute(self, commute, job_post):
        job_post.transit_commute = commute['transitTime']
        job_post.drive_commute = commute['driveTime']

    def commute_less(self, query, commute_info):
        if query.commute:
            if commute_info['transitTime'] < query.commute or commute_info['driveTime'] < query.commute:
                return True
        return False

    # def get_employer_ids(self, employer_names, employers_by_name_dict):
    #     r = []
    #     for n in employer_names:
    #         r.extend(employers_by_name_dict[n])
    #     return r
    #
    # def get_location_ids(self, location_names, location_by_name_dict):
    #     r = []
    #     for n in location_names:
    #         r.extend(location_by_name_dict[n])
    #     return r

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
            # query.profile_id = query.profile_id.hex
            query_id_to_user_id_d[query.query_id] = alert_id_to_user_id_d[str(alert.alert_id)]
            if query.employer_names:
                query.employer_names = query.employer_names.split(',')
            else:
                query.employer_names = []
            if query.locations:
                query.locations = query.locations.split(',')
            else:
                query.locations = []
            query.terms = query.terms.split(',')
            queries.append(query)
        return queries, query_id_to_user_id_d
