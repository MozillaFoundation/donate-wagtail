from .environment import env


class Salesforce(object):
    SALESFORCE_ORGID = env('SALESFORCE_ORGID')
    SALESFORCE_CASE_RECORD_TYPE_ID = env('SALESFORCE_CASE_RECORD_TYPE_ID')
