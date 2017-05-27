# from django.core.management.base import BaseCommand, CommandError
# from JobPostService.job_post_app.models import Query
# import json
#
# class Command(BaseCommand):
#     help = 'generate alerts'
#
#     user_emails = {}
#     employer_ids = {}
#     location_ids = {}
#     commute_client = None
#
#     def add_arguments(self, parser):
#         parser.add_argument('user_id', nargs='+', type=str)
#         parser.add_argument('job_post_service_url', nargs='+', type=str)
#
#     def handle(self, *args, **options):
# #         if 'poll_id' in options:
# #         else:
#         url = options['user_service_url']
#         user_client = UserServiceClient(url);
#
#         url = options['provider_profile_service_url']
#         provider_client = ProviderProfileClient(url)
#
#         url = options['location_service_url']
#         location_client = LocationClient(url)
#
#         url = options['commute_service_url']
#         commute_client = CommuteClient(url)
#
#         queries = self.get_query()
#         users = user_client.get([q.user_id for q in queries])
#         for u in users:
#             user_emails[u.id] = u.email
#
#         employers = provider_client.get([name for q.employer_names in queries for name in q.employer_names])
#         for e in employers:
#             if e.name not in employer_ids:
#                 employer_ids[e.name] = []
#             employer_ids[e.name].append(e.id)
#
#         locations = provider_client.get([location for q.locations in queries for location in q.locations])
#         for l in locations:
#             if l.name not in location_ids:
#                 location_ids[l.name] = []
#             location_ids[l.name].append(l.id)
#
#         results = []
#         for query in queries:
#             matches = self.generate_match(query)
#             email = user_emails[query.user_id]
#             results.append((email, query, matches))
#         self.process(results)
#
#     def generate_match(self, query):
#         query_dict = self.convert_to_dict(query)
#         all_job_posts = JobPost.objects.all().fiter(query_dict)
#         if query.commute and query.commute_unit:
#             query.commute, query.commute_time, query.commute_option
#             self.filter_job_posts_with_commute(all_job_posts, query)
#
#     def convert_to_dict(self, query):
#         keywords = json.loads(query.keywords)
#         if keywords:
#             # custom lookup
#             d['title,description__search'] = keywords[0].join(' +')
#             # full text search of keywords,
#             # i.e. MATCH (title,description) AGAINST (k1 +k2 +3 IN BOOLEAN MODE)
#             # match k1 k2 AND k3
#         employer_names = json.loads(query.keywords)
#         if employer_names:
#             # custom lookup
#             employer_ids = self.get_employer_ids(employer_names)
#             d['employer_profile_id__search'] = employer_ids.join(' ')
#             # i.e. MATCH (employer_profile_id) AGAINST (e1 e2 e3 IN BOOLEAN MODE)
#             # match either e1 e2 OR e3
#         if query.locations:
#             # custom lookup
#             location_ids = self.get_location_ids(query.locations)
#             d['location_id__contains'] = location_ids.join(' ')
#         if query.compensation and query.compensation_unit:
#             d['compensation_amount__range'] = (query.compensation[0], query.compensation[1])
#             d['compensation_duration'] = query.compensation_unit
#         if query.updated:
#             d['updated__gt'] = query.updated
#         if query.has_contact != None:
#             d['has_contact'] = query.has_contact
#         return d
#
#     def filter_job_posts_with_commute(self, job_posts, query):
#         filtered_job_posts = []
#         location_pairs_to_query = []
#         commute_svc_query_job_posts = []
#         for job_post in job_posts:
#             cache_key = query.location_ids[0] + '-' + job_post.location_id
#             if cache_key in commute_cache and self.commute_less(query, commute_cache[cache_key]):
#                 filtered_job_posts.append(job_post)
#             else:
#                 location_pairs_to_query.append((query.location_ids[0], job_post.location_id))
#                 commute_svc_query_job_posts.append(job_post)
#         d = commute_client.query(location_pairs_to_query)
#         for job_post in commute_svc_query_job_posts:
#             key = query.location_ids[0] + '-' + job_post.location_id
#             commute_cache[key] = d[key]
#             if key in d and self.commute_less(query, d[key]):
#                 filtered_job_posts.append(job_post)
#         return filtered_job_posts
#
#     def commute_less(self, query, commute_info):
#         if query.commute_options.contains('transit') and commute_info.transit_time < query.commute_info.transit_time
#             return True
#         if query.commute_options.contains('drive') and commute_info.drive_time < query.commute_info.drive_time
#             return True
#         return False
#
#     def get_employer_ids(self, employer_names):
#         r = []
#         for n in employer_names:
#             r.extend(employer_ids[n])
#         return r
#
#     def get_location_ids(self, locations):
#         r = []
#         for n in locations:
#             r.extend(location_ids[n])
#         return r
#
#     def process(self, results):
#         email_client = EmailClient()
#         email_client.send(results) # 3)
#         # save(results)
#
#     def get_query(self):
#         return Query.objects.all().fiter(active=True)
#
#
# class EmailClient:
#
#     def __init__(self):
#         self.template_engine = TemplateEngine()
#         self.api = "https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages"
#         self.auth = ("api", "YOUR_API_KEY")
#         self.from = "admin@oneseek.com"
#
#
#     def send(self, results):
#         for r in results:
#             email = r[0]
#             query = r[1]
#             matches = r[2]
#             msg = self.template_engine.render(matches)
#             subject = self.template_engine.subject();
#             requests.post(self.api, self.auth,
#                 data={"from": self.from,
#                       "to": [email],
#                       "subject": subject,
#                       "text": msg,
#                 })
