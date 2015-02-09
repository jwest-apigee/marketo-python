import xml.etree.ElementTree as ET

import lead_activity


valid_types = [
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


def wrap(key_value=None,
         key_type='EMAIL',
         offset=0,
         batch_size=100,
         activity_types=None):
    if not key_type in valid_types:
        raise ValueError('Invalid Key Type: [%s]' % key_type)

    if not activity_types:
        activity_types = [
            'VisitWebpage',
            'FillOutForm',
            'ClickLink',
            'SendEmail',
            'EmailDelivered',
            'EmailBounced',
            'UnsubscribeEmail',
            'OpenEmail',
            'ClickEmail',
            'NewLead',
            'ChangeDataValue',
            'LeadAssigned',
            'NewSFDCOpprtnty',
            'Wait',
            'RunSubflow',
            'RemoveFromFlow',
            'PushLeadToSales',
            'CreateTask',
            'ConvertLead',
            'ChangeScore',
            'ChangeOwner',
            'AddToList',
            'RemoveFromList',
            'SFDCActivity',
            'EmailBouncedSoft',
            'PushLeadUpdatesToSales',
            'DeleteLeadFromSales',
            'SFDCActivityUpdated',
            'SFDCMergeLeads',
            'MergeLeads',
            'ResolveConflicts',
            'AssocWithOpprtntyInSales',
            'DissocFromOpprtntyInSales',
            'UpdateOpprtntyInSales',
            'DeleteLead',
            'SendAlert',
            'SendSalesEmail',
            'OpenSalesEmail',
            'ClickSalesEmail',
            'AddtoSFDCCampaign',
            'RemoveFromSFDCCampaign',
            'ChangeStatusInSFDCCampaign',
            'ReceiveSalesEmail',
            'InterestingMoment',
            'RequestCampaign',
            'SalesEmailBounced',
            'ChangeLeadPartition',
            'ChangeRevenueStage',
            'ChangeRevenueStageManually',
            'ComputeDataValue',
            'ChangeStatusInProgression',
            'ChangeFieldInProgram',
            'EnrichWithDatacom',
            'ChangeSegment',
            'ResolveRuleset',
            'SmartCampaignTest',
            'SmartCampaignTestTrigger'
        ]

    activities_str = ''

    for activity in activity_types:
        activities_str += '<activityType>%s</activityType>\n' % activity

    response_str = """
    <ns1:paramsGetLeadActivity>
        <leadKey>
            <keyType>{key_type}</keyType>
            <keyValue>{key_value}</keyValue>
        </leadKey>

        <activityFilter>
            <includeTypes>
            {activities_str}
            </includeTypes>
        </activityFilter>

        <startPosition>
            <offset>{offset}</offset>
        </startPosition>
        <batchSize>{batch_size}</batchSize>
    </ns1:paramsGetLeadActivity>
    """.format(
        key_type=key_type,
        key_value=key_value,
        offset=offset,
        batch_size=batch_size,
        activities_str=activities_str)

    return response_str


def unwrap(response):
    root = ET.fromstring(response.text)
    activities = []

    for activity_el in root.findall('.//activityRecord'):
        activity = lead_activity.unwrap(activity_el)
        activities.append(activity)

    return activities
