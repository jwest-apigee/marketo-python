import xml.etree.ElementTree as ET
import datetime

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

all_activity_types = [
    'AddToList',
    'AddtoSFDCCampaign',
    'AssocWithOpprtntyInSales',
    'ChangeDataValue',
    'ChangeFieldInProgram',
    'ChangeLeadPartition',
    'ChangeOwner',
    'ChangeRevenueStage',
    'ChangeRevenueStageManually',
    'ChangeScore',
    'ChangeSegment',
    'ChangeStatusInProgression',
    'ChangeStatusInSFDCCampaign',
    'ClickEmail',
    'ClickLink',
    'ClickSalesEmail',
    'ComputeDataValue',
    'ConvertLead',
    'CreateTask',
    'DeleteLead',
    'DeleteLeadFromSales',
    'DissocFromOpprtntyInSales',
    'EmailBounced',
    'EmailBouncedSoft',
    'EmailDelivered',
    'EnrichWithDatacom',
    'FillOutForm',
    'InterestingMoment',
    'LeadAssigned',
    'MergeLeads',
    'NewLead',
    'NewSFDCOpprtnty',
    'OpenEmail',
    'OpenSalesEmail',
    'PushLeadToSales',
    'PushLeadUpdatesToSales',
    'ReceiveSalesEmail',
    'RemoveFromFlow',
    'RemoveFromList',
    'RemoveFromSFDCCampaign',
    'RequestCampaign',
    'ResolveConflicts',
    'ResolveRuleset',
    'RunSubflow',
    'SalesEmailBounced',
    'SendAlert',
    'SendEmail',
    'SendSalesEmail',
    'SFDCActivity',
    'SFDCActivityUpdated',
    'SFDCMergeLeads',
    'SmartCampaignTest',
    'SmartCampaignTestTrigger'
    'UnsubscribeEmail',
    'UpdateOpprtntyInSales',
    'VisitWebpage',
    'Wait',
]


def string_or_date(oldest_created_at):
    if isinstance(oldest_created_at, str):
        return oldest_created_at
    if isinstance(oldest_created_at, datetime.datetime):
        return oldest_created_at.strftime('%Y-%m-%dT%H:%M:%S')


def wrap(
        key_value=None,
        key_type='EMAIL',
        batch_size=100,
        activity_types=None,
        oldest_created_at=None,
        latest_created_at=None,
        offset_string=None
):
    if not key_type in valid_types:
        raise ValueError('Invalid Key Type: [%s]' % key_type)

    if not activity_types:
        activity_types = all_activity_types

    start_position = ''

    if oldest_created_at:
        start_position += '<oldestCreatedAt>%s</oldestCreatedAt>' % string_or_date(oldest_created_at)

    if latest_created_at:
        start_position += '<latestCreatedAt>%s</latestCreatedAt>' % string_or_date(latest_created_at)

    if offset_string:
        start_position += '<offset>%s</offset>' % offset_string

    if len(start_position) > 0:
        new_start_str = '<startPosition>%s</startPosition>' % start_position
    else:
        new_start_str = ''

    activities_str = ''

    for activity in activity_types:
        activities_str += '<activityType>%s</activityType>' % activity

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
        {new_start_str}
    </ns1:paramsGetLeadActivity>
    """.format(
        key_type=key_type,
        key_value=key_value,
        batch_size=batch_size,
        activities_str=activities_str,
        new_start_str=new_start_str
    )

    return response_str


def unwrap(response):
    root = ET.fromstring(response.text.encode('utf8'))
    activities = []

    remaining_count_list = root.findall('.//remainingCount')

    for activity_el in root.findall('.//activityRecord'):
        activity = lead_activity.unwrap(activity_el)
        activities.append(activity)

    remaining = 0

    if len(remaining_count_list) > 0:
        remaining = int(remaining_count_list[0].text)

    if remaining > 0 and len(activities) > 0:
        # print 'retrieved [%s] with [%s] remaining' % (len(activities), remaining)
        new_start = root.findall('.//newStartPosition')
    else:
        new_start = None

    return activities, new_start
