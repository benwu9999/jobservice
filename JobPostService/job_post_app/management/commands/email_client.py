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
from management.commands import alert_generator_util

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        [os.path.join(os.path.dirname(__file__), 'view')]),
    extensions=['jinja2.ext.i18n'])

env.install_gettext_translations(i18n)


class EmailClient:
    def __init__(self):
        pass

    template = env.get_template('email_template.html')

    key = 'key-992449508ab9bedb746eb2b72af6e01f'
    sandbox = 'sandbox4ce17324a56c48e28aa83dcb313ed504.mailgun.org'
    MAX_BATCH_SIZE = 1000

    def send(self, all_results):
        chunks = [all_results[x:x + self.MAX_BATCH_SIZE] for x in xrange(0, len(all_results), self.MAX_BATCH_SIZE)]
        for results in chunks:
            self._send_mails(results)

    def _send_mails(self, results):
        recpt_variables_d = defaultdict(dict)
        emails = list()
        for result in results:
            alert = result[0]
            matches = result[1]
            email = result[2]
            recpt_variables_d[email]['alert_name'] = 'Oneseek job post matches for alert "{0}"'.format(alert.name)
            recpt_variables_d[email]['email_text'] = self._get_email_text(matches)
            emails.append(email)
            # "recipient-variables": ('{"bob@example.com": {"first":"Bob", "id":1}, '
            #                         '"alice@example.com": {"first":"Alice", "id": 2}}')

        request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(self.sandbox)
        recpt_variables = json.dumps(recpt_variables_d)
        request = requests.post(
            request_url,
            auth=("api", self.key),
            data={"from": "hello@example.com",
                  "to": emails,
                  "subject": "%recipient.alert_name%",
                  "text": 'html version of email failed to display',
                  "html": '%recipient.email_text%',
                  "recipient-variables": recpt_variables
                  }
        )

        print('Status: {0}'.format(request.status_code))
        print('Body:   {0}'.format(request.text))

    def _get_email_text(self, matches):
        i18n.setLocale("zh_TW")
        d = dict()
        job_posts = list()
        for m in matches:
            location_str = alert_generator_util.format_location(m.location)
            job_post = {'description': m.title + ' - ' + m.description,
                        'location': location_str,  # seems Gmail automatically links a valid location to Google map
                        'location_link': alert_generator_util.get_location_link(location_str),
                        'transit_commute': m.transit_commute,
                        'drive_commute': m.drive_commute
                        }
            job_posts.append(job_post)
        d['job_posts'] = job_posts

        jinja = self.template.render(d).encode('utf-8')
        with open("temp.mjml", "w") as text_file:
            text_file.write(jinja)

        email_text = getoutput("mjml --stdout %s" % ("temp.mjml"))
        return email_text

    @staticmethod
    def _to_str(matches):
        string = ''
        for match in matches:
            string += str(match)
        return string
