import datetime


def clean_labor(date, classification_rate, straight_hours, ot_hours):
    ''' edit the scrapped data so it fits into database properly.'''
    if clean_classification_rate(classification_rate) and clean_st_hours(straight_hours):
        classification, rate = clean_classification_rate(classification_rate)
        date = us_date_to_ymd(date)
        return [date, classification, rate, float(straight_hours), float(ot_hours)]


def clean_classification_rate(class_rate):
    '''separate the rate and classification string into two entities.'''

    if(len(class_rate.split('--$')) == 2):
        classification, rate = class_rate.split('--$')
        return [classification, rate]
    return False


def clean_st_hours(hours):
    return float(hours) <= 8


def clean_mileage(date, type, miles):
    date = us_date_to_ymd(date)
    return [date, clean_type(type), clean_miles(miles)]


def clean_type(type):
    ''' sort mileage type into ojm or commute based on if ojm is in string '''
    if 'ojm' in type.lower():
        return 'ojm'
    else:
        return 'commute'


def clean_miles(miles):
    ''' remove mi from mileage number '''
    return float(miles.split(' ')[0])


def us_date_to_ymd(date):
    return datetime.datetime.strptime(date, '%m/%d/%Y').strftime("%Y%m%d")
