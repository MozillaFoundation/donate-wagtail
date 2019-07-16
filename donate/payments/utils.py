def freeze_personal_details_for_session(details):
    details = details.copy()
    details['amount'] = str(details['amount'])
    return details
