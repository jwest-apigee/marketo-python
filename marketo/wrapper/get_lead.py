import xml.etree.ElementTree as ET

import lead_record

valid_lead_keys = [
    'IDNUM',
    'COOKIE',
    'EMAIL',
    'LEADOWNEREMAIL',
    'SFDCACCOUNTID',
    'SFDCCONTACTID',
    'SFDCLEADID',
    'SFDCLEADOWNERID',
    'SFDCOPPTYID'
]


def wrap(key_value=None, key_type='EMAIL'):
    if not key_value:
        raise ValueError('key_value is None!')

    if not key_type in valid_lead_keys:
        raise ValueError('Specified key_type=[{key_type}] is not valid!'.format(key_type=key_type))

    return """
    <ns1:paramsGetLead>
        <leadKey>
            <keyType>{key_type}</keyType>
            <keyValue>{key_value}</keyValue>
        </leadKey>
    </ns1:paramsGetLead>
    """.format(key_type=key_type,
               key_value=key_value)


def unwrap(response):
    root = ET.fromstring(response.text.encode('utf8'))
    leads = []

    leads_xml_arr = root.findall('.//leadRecord')

    for lead_el in leads_xml_arr:
        lead = lead_record.unwrap(lead_el)
        leads.append(lead)

    return leads