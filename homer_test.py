#import required libraries
import json, sys
import pandas as pd
from pandas.io.json import json_normalize  
from Homer_db import Homer_db 
from Subscription import Subscription
from util import calc_trial_start_date, calc_sub_start_date, calc_exp_date, calc_current_status
import argparse

#custom argument parsing validation
class OperationAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        values = values.strip()
        if values not in ["insert", "create", "select", "delete", "count"]:
            db.get_logger().error("Incorrect operation entered, enter anyone from insert, create, select, delete, count")
            raise ValueError("Incorrect operation entered")
        setattr(namespace, self.dest, values)

class EnvAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        values = values.strip()
        if (values not in ["dev","prod"]):
            db.get_logger().error("Incorrect environment entered, either enter dev or prod")
            raise ValueError("Incorrect environment entered")
        setattr(namespace, self.dest, values)

#read given json file store in to record_list 
def read_json_data(file_path):
    try:
        with open(file_path) as json_data:
            record_list = json.load(json_data)
        return record_list
    except Exception as e:
        db.get_logger().debug("Invalied file path or file in use in other application")
        db.get_logger().error(e)
        raise   #Raising error to interrupt execution since code should not execute if data has not been imported properly
    
def insert_data(db, subsc, file_path):
    record_list = read_json_data(file_path)
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
        db.get_logger().debug("Insertion transaction could not complete, returned with error: ")
        db.get_logger().error(e)


#Get user distribution based on subcription
def fetch_subscription_count(db, subsc):
    types = ["Active Trial", "Expired Trial", "Active Subscription", "Expired Subscription"]
    user_distrib = {}
    for type in types:
        user_distrib[type] = subsc.get_subsc_count(db, type)
    db.get_logger().info(user_distrib)

def fetch_all_records(db, subsc, filepath=""):
    records = subsc.select_all(db)
    if(records.empty is False):
        records.to_csv(filepath+"\\homer_db_records.csv", index=False)
        db.get_logger().info("Records saved in homer_db_records.csv file")
    else:
        db.get_logger().error("No records exists in database")

def delete_all_records(db, subsc):
    subsc.delete_table(db)
    db.get_logger().info("Table deleted succesfully")

if __name__ == "__main__":
    db = Homer_db() # create database object
    subsc = Subscription() #subscription class - database methods

    # Constructing the argument parser
    argp = argparse.ArgumentParser()
    argp.add_argument("-file", required=True, help="Enter json file name and its path: xx/xx/abc.json")
    argp.add_argument("-env", required=True, default="dev", action=EnvAction, help="Enter runtmie environment, dev/prod")
    argp.add_argument("-op", required=True, action=OperationAction ,help="operation: insert, create, select, delete, count")
    argp.add_argument("--csvpath", required=False, help="Provide csv file path to store")

    args = vars(argp.parse_args()) # file, env, op= insert, create, select, delete, count
    db.set_env_var(args["env"])
    if((args['op']).lower() == "create"):
        subsc.create_table(db)
    
    elif((args['op']).lower() == "count"):
        fetch_subscription_count(db, subsc)

    elif((args['op']).lower() == "insert"):
        insert_data(db, subsc,args['file'])
    
    elif((args['op']).lower() == "select"):
        fetch_all_records(db, subsc, args['csvpath'])
    
    elif((args['op']).lower() == "delete"):
        delete_all_records(db, subsc)
    else:
        db.get_logger().error("Incorrect user operation entered: "+args['op'])
    print("Execution completed. Please check runtime logs for more info")
