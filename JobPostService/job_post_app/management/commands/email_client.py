# curl -s --user 'api:key-992449508ab9bedb746eb2b72af6e01f' \
# https://api.mailgun.net/v3/sandbox4ce17324a56c48e28aa83dcb313ed504.mailgun.org/messages \
# -F from='Excited User <mailgun@sandbox4ce17324a56c48e28aa83dcb313ed504.mailgun.org>' \
# -F to=benwu9999@gmail.com -F subject='Hello' -F text='Testing some Mailgun awesomness!'
import json
from commands import getoutput

import requests
from collections import defaultdict
import os
import jinja2
import i18n
import alert_generator_util
from admin_site.settings import UI_JOB_POST_URL_PREFIX

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__), 'view')]),
    extensions=['jinja2.ext.i18n'])

env.install_gettext_translations(i18n)


class EmailClient:
    template_url = 'email_template.html'
    template = env.get_template(template_url)
    key = 'key-992449508ab9bedb746eb2b72af6e01f'
    sandbox = 'sandbox4ce17324a56c48e28aa83dcb313ed504.mailgun.org'
    MAX_BATCH_SIZE = 1000

    def __init__(self):
        pass

    def send(self, all_results):
        chunks = [all_results[x:x + self.MAX_BATCH_SIZE] for x in xrange(0, len(all_results), self.MAX_BATCH_SIZE)]
        for results in chunks:
            self._send_mails(results)

    def _send_mails(self, results):
        recpt_variables_d = defaultdict(dict)
        emails = list()
        for result in results:
            alert = result.alert
            matches = result.job_posts
            email = result.email
            if email and matches:
                if True:  # for English emails
                    # if email not in recpt_variables_d:
                    #     recpt_variables_d[email]['alerts'] = []
                    recpt_variables_d[email]['subject'] = 'Oneseek job post matches for '.format(
                        alert.name.encode('utf8'))
                    if 'alerts' not in recpt_variables_d[email]:
                        recpt_variables_d[email]['alerts'] = dict()
                    recpt_variables_d[email]['alerts'][alert.alert_id.hex] = {
                        'user_id' : result.user_id,
                        'alert_name': alert.name,
                        'alert_location': alert.query.location,
                        'matches': matches}
                emails.append(email)
            # "recipient-variables": ('{"bob@example.com": {"first":"Bob", "id":1}, '
            #                         '"alice@example.com": {"first":"Alice", "id": 2}}')

        for email_dict in recpt_variables_d.values():
            email_dict['email_text'] = self._get_email_text(email_dict.pop('alerts'))

        if emails:
            request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(self.sandbox)
            recpt_variables = json.dumps(recpt_variables_d)
            request = requests.post(
                request_url,
                auth=("api", self.key),
                data={"from": "hello@example.com",
                      "to": emails,
                      "subject": "%recipient.subject%",
                      "text": 'html version of email failed to display',
                      "html": '%recipient.email_text%',
                      "recipient-variables": recpt_variables
                      }
            )
            print('Status: {0}'.format(request.status_code))
            print('Body:   {0}'.format(request.text))
        else:
            print('no email sent')

    def _get_email_text(self, alerts_dict):
        i18n.setLocale("zh_TW")

        d = {'data': defaultdict(dict)}
        for alert_id, entry in alerts_dict.iteritems():
            job_posts = list()
            for m in entry['matches']:
                location_str = alert_generator_util.format_location(m.location)
                job_post = {
                            'job_post_id': UI_JOB_POST_URL_PREFIX + m.job_post_id.hex + '?userId=' + entry['user_id'],
                            'title': m.title,
                            'description': m.description,
                            'email': 'blah@blahcom',
                            'phone': '6463883224',
                            'location': location_str,  # seems Gmail automatically links a valid location to Google map
                            'location_link': alert_generator_util.get_location_link(location_str),
                            'transit_commute': m.transit_commute,
                            'drive_commute': m.drive_commute,
                            'created_time': m.created.strftime('%Y-%m-%d')
                            }
                job_posts.append(job_post)
            d['data'][alert_id]['alert_location'] = self._to_location_str(entry['alert_location'])
            d['data'][alert_id]['alert_name'] = entry['alert_name']
            d['data'][alert_id]['job_posts'] = job_posts

        jinja = self.template.render(d).encode('utf-8')
        with open("temp.mjml", "w") as text_file:
            text_file.write(jinja)

        email_text = getoutput("mjml --stdout %s" % ("temp.mjml"))
        return email_text

    @staticmethod
    def _to_location_str(location_d):
        return "(" + location_d['name'] + ") " + location_d['streetAddress'] + ", " + location_d['city'] + ", " + location_d['state'] + ", " + str(location_d['zipCode']);

    @staticmethod
    def _to_str(matches):
        string = ''
        for match in matches:
            string += str(match)
        return string
