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


def wrap(key_values=None, key_type='EMAIL', limit=100):
    if not key_values:
        raise ValueError('No Key Values Specified')

    if not key_type in valid_lead_keys:
        raise ValueError('Specified key_type=[{key_type}] is not valid!'.format(key_type=key_type))

    key_values_str = ''

    for key_value in key_values:
        key_values_str += '<stringItem>{key_value}</stringItem>'.format(key_value=key_value)

    return """
    <ns1:paramsGetMultipleLeads>
        <leadSelector xsi:type="ns1:LeadKeySelector">
            <keyType>{key_type}</keyType>
            <keyValues>
                {key_values_str}
            </keyValues>
        </leadSelector>
        <batchSize>{limit}</batchSize>
    </ns1:paramsGetMultipleLeads>
    """.format(key_type=key_type,
               key_values_str=key_values_str,
               limit=limit)


def unwrap(response):
    root = ET.fromstring(response.text)

    records = []

    for record_el in root.findall('.//leadRecord'):
        record = lead_record.unwrap(record_el)
        records.append(record)

    return records
