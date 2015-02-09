import xml.etree.ElementTree as ET

from marketo.wrapper import m_object_record


def wrap():
    return '<ns1:paramsListMObjects />'


def unwrap(response):
    root = ET.fromstring(response.text)
    objects = []

    for object_el in root.findall('.//objects'):
        activity = m_object_record.unwrap(object_el)
        objects.append(activity)

    return objects
