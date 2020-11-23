import pandas as pd

# Class for queries:
class Subscription:
    def select_all(self, db):
        try:
            db.query("select * from itunes_subscription;")  #fetch all sql query
            results = db.get_cur().fetchall()
            columns = ["id", "transactions", "trial_start_date", "subscription_start_date", "expiration_date","current_status"]
            records = pd.DataFrame(columns=columns, index = [i for i in range(0,len(results))]) #setting dataframe columns and indexes
            row = 0 #Initializing index to iterate while inserting data in dataframe
            for result in results:  #Iterating over results fetched from database 
                records["id"].iloc[row] = result[0]
                records["transactions"].iloc[row] = result[1]
                records["trial_start_date"].iloc[row] = result[2]
                records["subscription_start_date"].iloc[row] = result[3]
                records["expiration_date"].iloc[row] = result[4]
                records["current_status"].iloc[row] = result[5]
                row+=1  #Increasing index of dataframe
                db.get_logger().debug("select_all: Row added to dataframe")
            return records
        except Exception as e:
            db.close_failure() #this includes transaction rollback
            db.get_logger().debug("Select all transaction could not complete, returned with error: ")
            db.get_logger().error(e)
            return None #returning Nonce since exception occured
        finally:
            db.get_logger().debug("select_all: All records fetched from database")
            db.close_success() #commit the changes and close connection and cursor
    
    def get_subsc_count(self, db, status):
        try:
            db.query("select count(*) from itunes_subscription where current_status = %s;", (status,))
            results = db.get_cur().fetchall()
            return results[0][0]
        except Exception as e:
            db.close_failure() #this includes transaction rollback
            db.get_logger().debug("Get count transaction could not complete, returned with error: ")
            db.get_logger().error(e)
            return None #returning None, since exception has occured
        finally:
            db.close_success() #commit the changes and close connection and cursor

    # Create a table in to database
    def create_table(self, db):
        try:
            db.query(''' DROP TABLE IF EXISTS itunes_subscription;
            CREATE TABLE itunes_subscription(
            Id INT GENERATED ALWAYS AS IDENTITY,
            transactions json[],
            trial_start_date timestamptz,
            Sub_start_date timestamptz,
            Expiration_date timestamptz NOT NULL,
            current_status text
                );''')
        except Exception as e:
            db.close_failure() #this includes transaction rollback
            db.get_logger().debug("Create table transaction could not complete, returned with error: ")
            db.get_logger().error(e)
        finally:
            db.close_success()

    def insert_values(self, db, values):
        try:
            SQL_INSERT_QUERY = """INSERT INTO itunes_subscription (
                                transactions,
                                trial_start_date,
                                Sub_start_date,
                                Expiration_date,
                                current_status
                                ) VALUES (%s::json[],%s, %s, %s, %s)"""
            db.query(SQL_INSERT_QUERY, values)
        except Exception as e:
            db.get_logger().debug("Insert transaction could not complete, returned with error: ")
            db.get_logger().error(e)
            raise  #raising error again to carch by parent try..except block
        #db.close_success() - not recomeended to close database connection here, 
        # since we are processing entries in bulk and connection should close at the end to preserve the atomicity of transaction