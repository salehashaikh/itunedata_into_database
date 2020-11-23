#import required libraries
import json, sys
import pandas as pd
from pandas.io.json import json_normalize  
from Homer_db import Homer_db 
from Subscription import Subscription
from util import calc_trial_start_date, calc_sub_start_date, calc_exp_date, calc_current_status

db = Homer_db() # create database object
subsc = Subscription() #subscription class - database methods
subsc.create_table(db) 

#read given json file store in to record_list   
try:
    with open('data.json') as json_data:
        record_list = json.load(json_data)
except Exception as e:
    db.get_logger().debug("Not able to find the file")
    db.get_logger().error(e)
    raise   #Raising error to interrupt execution since code should not execute if data has not been imported properly

try:
    for record in record_list:
        trial_Start_date = calc_trial_start_date(pd.json_normalize(record_list[record]))
        sub_start_date = calc_sub_start_date(pd.json_normalize(record_list[record]))
        if(sub_start_date == None):
                sub_start_date is None
        exp_date = calc_exp_date(pd.json_normalize(record_list[record]))
        curr_sta = calc_current_status(pd.json_normalize(record_list[record]))
        values = (
        [(json.dumps(d),) for d in record_list[record]],
        trial_Start_date,
        sub_start_date, exp_date, curr_sta
        )
        subsc.insert_values(db, values)
except Exception as e:
    db.close_failure() #this includes transaction rollback
    db.get_logger().debug("Insertion transaction could not complete, returned with error: ")
    db.get_logger().error(e)
finally:
    db.close_success() #commit the changes and close connection and cursor

#Get user distribution based on subcription
def fetch_subscription_count():
    types = ["Active Trial", "Expired Trial", "Active Subscription", "Expired Subscription"]
    user_distrib = {}
    for type in types:
        user_distrib[type] = subsc.get_subsc_count(db, type)
    db.get_logger().info(user_distrib)
fetch_subscription_count()
