import version

VERSION = version.VERSION
__version__ = VERSION

import requests
import auth

from marketo.wrapper import get_lead, get_lead_activity, get_all_lead_activity, request_campaign, sync_lead, \
    get_multiple_leads_by_key


class Client:
    def __init__(self, soap_endpoint=None, user_id=None, encryption_key=None):

        if not soap_endpoint or not isinstance(soap_endpoint, str):
            raise ValueError('Must supply a soap_endpoint as a non empty string.')

        if not user_id or not isinstance(user_id, (str, unicode)):
            raise ValueError('Must supply a user_id as a non empty string.')

        if not encryption_key or not isinstance(encryption_key, str):
            raise ValueError('Must supply a encryption_key as a non empty string.')

        self.soap_endpoint = soap_endpoint
        self.user_id = user_id
        self.encryption_key = encryption_key

    def wrap(self, body):
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n' +
            '<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" ' +
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' +
            'xmlns:wsdl="http://www.marketo.com/mktows/" ' +
            'xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" ' +
            'xmlns:ins0="http://www.marketo.com/mktows/" ' +
            'xmlns:ns1="http://www.marketo.com/mktows/" ' +
            'xmlns:mkt="http://www.marketo.com/mktows/">\n' +
            auth.header(self.user_id, self.encryption_key) +
            '<env:Body>\n' +
            body +
            '</env:Body>\n' +
            '</env:Envelope>'
        )

    def request(self, body, new_start=None):
        self.handle_paging(body, new_start)
        envelope = self.wrap(body)
        # print '---'
        # print 'request: ' + envelope
        # print '---'

        response = requests.post(self.soap_endpoint,
                                 data=envelope,
                                 headers={
                                     'Connection': 'Keep-Alive',
                                     'Soapaction': '',
                                     'Content-Type': 'text/xml;charset=UTF-8',
                                     'Accept': '*/*'})
        # print '---'
        # print 'response: ' + response.content
        # print '---'

        return response

    def get_lead(self, email=None, key_value=None, key_type='EMAIL'):

        if email:
            key_value = email
            key_type = 'EMAIL'

        if not key_value or not isinstance(key_value, (str, unicode)):
            raise ValueError('Must supply a key_value(i.e. email) as a non empty string.')

        body = get_lead.wrap(key_value=key_value, key_type=key_type)
        response = self.request(body)

        # print response.text

        if response.status_code == 200:
            return get_lead.unwrap(response)
        else:
            raise Exception(response.text)

    def get_multiple_leads(self, key_values=None, key_type='EMAIL', limit=100):

        if not key_values:
            raise ValueError('Must supply a key_value(i.e. email) as a non empty string.')

        body = get_multiple_leads_by_key.wrap(key_values=key_values, key_type=key_type, limit=limit)
        response = self.request(body)
        if response.status_code == 200:
            return get_multiple_leads_by_key.unwrap(response)
        else:
            raise Exception(response.text)

    def get_lead_activity(self, email=None, key_value=None, key_type='EMAIL',
                          activity_types=None, limit=100, offset=0):

        if email:
            key_value = email
            key_type = 'EMAIL'

        if not key_value or not isinstance(key_value, (str, unicode)):
            raise ValueError('Must supply a key_value(i.e. email) as a non empty string.')

        body = get_lead_activity.wrap(key_type=key_type,
                                      key_value=key_value,
                                      activity_types=activity_types,
                                      batch_size=limit,
                                      offset=offset)

        response = self.request(body)
        print response.content

        if response.status_code == 200:
            return get_lead_activity.unwrap(response)
        else:
            raise Exception(response.text)

    def get_lead_changes(self, email=None, key_value=None, key_type='EMAIL',
                         activity_types=None, limit=100, offset=0):

        if email:
            key_value = email
            key_type = 'EMAIL'

        if not key_value or not isinstance(key_value, (str, unicode)):
            raise ValueError('Must supply a key_value(i.e. email) as a non empty string.')

        body = get_lead_activity.wrap(key_type=key_type,
                                      key_value=key_value,
                                      activity_types=activity_types,
                                      batch_size=limit,
                                      offset=offset)

        response = self.request(body)
        print response.content

        if response.status_code == 200:
            return get_lead_activity.unwrap(response)
        else:
            raise Exception(response.text)

    def get_all_lead_activity(self,
                              email=None,
                              key_value=None,
                              key_type='EMAIL',
                              activity_types=None,
                              oldest_created_at=None):

        if email:
            key_value = email
            key_type = 'EMAIL'

        if not isinstance(key_value, (str, unicode)):
            key_value = str(key_value)

        if not key_value or not isinstance(key_value, (str, unicode)):
            raise ValueError('Must supply a key_value(i.e. email) as a non empty string.')

        body = get_all_lead_activity.wrap(
            key_type=key_type,
            key_value=key_value,
            activity_types=activity_types,
            oldest_created_at=oldest_created_at
        )

        activity_arr = []
        while True:

            response = self.request(body)

            if not response.status_code == 200:
                raise Exception(response.text)

            new_start = None
            activities, new_start = get_all_lead_activity.unwrap(response)

            if activities:
                activity_arr += activities

            if not new_start or not len(new_start) > 0:
                break
            else:
                n_offset = new_start[0].find('offset').text
                n_latestCreatedAt = new_start[0].find('latestCreatedAt').text
                n_oldestCreatedAt = new_start[0].find('oldestCreatedAt').text

                body = get_all_lead_activity.wrap(
                    key_type=key_type,
                    key_value=key_value,
                    activity_types=activity_types,
                    oldest_created_at=n_oldestCreatedAt,
                    latest_created_at=n_latestCreatedAt,
                    offset_string=n_offset
                )

        if len(activity_arr) > 100:
            print 'woot: %s' % len(activity_arr)
        return activity_arr

    def request_campaign(self, campaign=None, lead=None):

        if not campaign or not isinstance(campaign, (str, unicode)):
            raise ValueError('Must supply campaign id as a non empty string.')

        if not lead or not isinstance(lead, (str, unicode)):
            raise ValueError('Must supply lead id as a non empty string.')

        body = request_campaign.wrap(campaign, lead)

        response = self.request(body)
        if response.status_code == 200:
            return True
        else:
            raise Exception(response.text)

    def sync_lead(self, email=None, attributes=None):

        if not email or not isinstance(email, (str, unicode)):
            raise ValueError('Must supply lead id as a non empty string.')

        if not attributes or not isinstance(attributes, tuple):
            raise ValueError('Must supply attributes as a non empty tuple.')

        body = sync_lead.wrap(email, attributes)

        response = self.request(body)

        if response.status_code == 200:
            return sync_lead.unwrap(response)
        else:
            raise Exception(response.text)

    def handle_paging(self, body, new_start):
        pass