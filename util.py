import pytz
from datetime import datetime

#convert string to date formate 
def cov_into_date(df_date):
    date_format="%Y-%m-%d %H:%M:%S"
    date_list = ' '.join((df_date).split()[0:2])
    return datetime.strptime(date_list, date_format)
    
#convert into naive timestamp
def with_location(df_date):
    gmt = pytz.timezone("Etc/GMT")
    return gmt.localize(cov_into_date(df_date)).astimezone(gmt)
    

#Calculate trial start date where 'is_trial_period' is True
def calc_trial_start_date(df):
    return with_location((df[df['is_trial_period']=='true']['purchase_date']).iloc[0])


# Calculate subscription start date which is equal to 'purchase_date' for the transaction that immediately follows a trail
def calc_sub_start_date(df):
    if((df.shape)[0] >1):
        df = df.iloc[1]
        return with_location(df['purchase_date'])
    else:
        return None

# Calculate the expire date which is equal to last transaction's expire date
def calc_exp_date(df):
    return with_location((df.iloc[df.shape[0]-1])['expires_date'])

# This function checks if the date is future date or not.
def is_future_date(df_date):
    exp_date = cov_into_date(df_date)
    if(exp_date > datetime.now()):
        return True
    else:
        return False

# Using is_future_date function calculate the current status
def calc_current_status(df):
    if((df.shape)[0] <= 1):
        if(is_future_date(df.iloc[0]['expires_date'])):
            return "Active Trial"
        else:
            return "Expired Trial"
    else:
        last_rec = (df.iloc[df.shape[0]-1])['expires_date']
        if(is_future_date(last_rec)):
            return "Active Subscription"
        else:
            return "Expired Subscription"
