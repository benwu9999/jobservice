import json
import urllib2
import os

class ApplicationServiceClient:

    URL = os.getenv('APPLICATION_SVC_URL', 'http://127.0.0.1:8000/application/');

    def get(self, application_id):
        if not application_id:
            return None;
        parsed = json.load(urllib2.urlopen(self.URL + application_id))
        return json.dumps(parsed, indent=4, sort_keys=True)

    def get_ids(self):
        pass

if __name__ == '__main__':
    client = ApplicationServiceClient();
    test_id = 'fb876c21-1da3-48c4-8761-ced53509f37d'
    json = client.get(test_id)
    print(json)
