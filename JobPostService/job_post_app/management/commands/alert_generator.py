import json

from django.core.management.base import BaseCommand, CommandError


# from JobPostService.job_post_app.models import Query
# import json
#

# run custom admin command like this:
# cd ~/job-post-service/JobPostService && python manage.py generate_alert
class Command(BaseCommand):
    help = 'generate alerts'

    #
    #     user_emails = {}
    #     employer_ids = {}
    #     location_ids = {}
    #     commute_client = None
    #
    commute_cache = dict();
    user_client = None;
    provider_client = None;
    location_client = None;
    commute_client = None;

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=str)
        parser.add_argument('job_post_service_url', nargs='+', type=str)
        parser.add_argument('provider_profile_service_url', nargs='+', type=str)
        parser.add_argument('location_service_url', nargs='+', type=str)
        parser.add_argument('commute_service_url', nargs='+', type=str)
        pass


    def handle(self, *args, **options):
        print "hello world"
        self.stdout.write("Hello")

        url = options['user_service_url']
        self.user_client = UserServiceClient(url);

        url = options['provider_profile_service_url']
        self.provider_client = ProviderProfileClient(url)

        url = options['location_service_url']
        self.location_client = LocationClient(url)

        url = options['commute_service_url']
        self.commute_client = CommuteClient(url)

        queries = self.get_query()
        user_ids = frozenset([q.user_id for q in queries])
        users = self.user_client.get(user_ids)
        users_dict = dict()
        for u in users:
            users_dict[u.id] = u.email

        employer_names = set()
        for q in queries:
            employer_names.update(q.employer_names)
        kwargs = dict()
        kwargs['name'] = employer_names
        employers_by_name_dict = self.provider_client.search_by_name(**kwargs)

        location_names = set()
        for q in queries:
            location_names.update(q.locations)
        kwargs = dict()
        kwargs['name'] = location_names
        location_by_name_dict = self.location_client.search_by_name(**kwargs)

        results = []
        for query in queries:
            matches = self.generate_match(query, employers_by_name_dict, location_by_name_dict)
            email = users_dict[query.user_id]
            results.append((email, query, matches))
        self.process(results)

    def generate_match(self, query, employers_by_name_dict, location_by_name_dict):
        query_dict = self.convert_to_dict(query, employers_by_name_dict, location_by_name_dict)
        matches = JobPost.objects.fiter(**query_dict)
        if query.commute and query.commute_unit:
            # query.commute, query.commute_time, query.commute_option
            self.filter_job_posts_with_commute(matches, query)
        return matches

    def convert_to_dict(self, query, employers_by_name_dict, location_by_name_dict):
        d = dict()
        keywords = query.keywords
        if keywords:
            # custom lookup
            d['title,description__search'] = ' +'.join(keywords)
            # full text search of keywords,
            # i.e. MATCH (title,description) AGAINST (k1 +k2 +3 IN BOOLEAN MODE)
            # match k1 k2 AND k3
        employer_names = query.employer_names
        if employer_names:
            # custom lookup
            employer_ids = self.get_employer_ids(employer_names, employers_by_name_dict)
            d['employer_profile_id__search'] = ','.join(employer_ids)
            # i.e. MATCH (employer_profile_id) AGAINST (e1 e2 e3 IN BOOLEAN MODE)
            # match either e1 e2 OR e3
        if query.locations:
            # custom lookup
            location_ids = self.get_location_ids(query.locations, location_by_name_dict)
            d['location_id__contains'] = ','.join(location_ids)
            query.location_ids = location_ids
        if query.compensation and query.compensation_unit:
            d['compensation_amount__range'] = (query.compensation[0], query.compensation[1])
            d['compensation_duration'] = query.compensation_unit
        if query.updated:
            d['modified__gt'] = query.updated
        if query.has_contact != None:
            d['has_contact'] = query.has_contact
        return d


    def filter_job_posts_with_commute(self, job_posts, query):
        filtered_job_posts = []
        location_pairs_to_query = []
        job_posts_by_location_id = dict()
        for job_post in job_posts:
            # list of location ids of the user
            for location_id in query.commute_location_ids:
                key = query.location_id + '-' + job_post.location_id
                # if commute already in cache, compared the cached value
                if key in self.commute_cache and self.commute_less(query, self.commute_cache[key]):
                    filtered_job_posts.append(job_post)
                # else query commute service and create map of
                # [location id of job posts -> list of job posts associated with the location id]
                else:
                    location_pairs_to_query.append((location_id, job_post.location_id))
                    if job_post.location_id not in job_posts_by_location_id:
                        job_posts_by_location_id[job_post.location_id] = []
                    job_posts_by_location_id[job_post.location_id].append(job_post)
        d = self.commute_client.query(location_pairs_to_query)
        for key in d:
            commute = d[key]
            if self.commute_less(query, commute):
                job_posts = job_posts_by_location_id[key.split('-')[1]]
                filtered_job_posts.extend(job_posts)
        return filtered_job_posts


    def commute_less(self, query, commute_info):
        if query.commute_options.contains('transit') and commute_info.transit_time < query.commute_info.transit_time:
            return True
        if query.commute_options.contains('drive') and commute_info.drive_time < query.commute_info.drive_time:
            return True
        return False


    def get_employer_ids(self, employer_names, employers_by_name_dict):
        r = []
        for n in employer_names:
            r.extend(employers_by_name_dict[n])
        return r


    def get_location_ids(self, locations, location_by_name_dict):
        r = []
        for n in locations:
            r.extend(location_by_name_dict[n])
        return r


    def process(self, results):
        email_client = EmailClient()
        email_client.send(results)  # 3)
        # save(results)


    def get_query(self):
        return Query.objects.fiter(active=True)


class EmailClient:
    def __init__(self):
        self.template_engine = TemplateEngine()
        self.api = "https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages"
        self.auth = ("api", "YOUR_API_KEY")
        self.from_email = "admin@oneseek.com"

    def send(self, results):
        for r in results:
            email = r[0]
            query = r[1]
            matches = r[2]
            msg = self.template_engine.render(matches)
            subject = self.template_engine.subject();
            requests.post(self.api, self.auth, data={"from": self.from_email, "to": [email], "subject": subject, "text": msg})