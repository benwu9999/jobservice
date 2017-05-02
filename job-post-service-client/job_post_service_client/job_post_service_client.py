import json
import urllib2

class JobPostServiceClient:

    URL = 'http://127.0.0.1:8000/jobPost'

    def get(self, job_post_id):
        if not job_post_id:
            return None;
        parsed = json.load(urllib2.urlopen("http://127.0.0.1:8000/jobPost/" + job_post_id))
        return json.dumps(parsed, indent=4, sort_keys=True)

    def get_ids(self):
        pass

if __name__ == '__main__':
    client = JobPostServiceClient();
    test_job_post_id = 'fb876c21-1da3-48c4-8761-ced53509f37d'
    json = client.get(test_job_post_id)
    print(json)
