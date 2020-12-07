# class for the connection to the postgres
import psycopg2, configparser
import logging
from logging.config import fileConfig
#fileConfig('log_config.ini') #, defaults={'logfilename': '/homer_log.log'}
logging.config.fileConfig('log_config.ini', defaults={'logfilename': 'homer_logs.log'}, disable_existing_loggers=False)

config = configparser.ConfigParser()
config.read('db_credentials.ini')

class Homer_db():
    __cur = None
    __conn = None
    __logger = logging.getLogger("main")
    __env = "dev_server"
    def __init__(self):
        try:
            self.__conn = psycopg2.connect(database=config[self.__env]['database'],
                                            user=config[self.__env]['user'], 
                                            password=config[self.__env]['password'])
            self.__cur = self.__conn.cursor()
            self.__logger.debug("Home_cb class's constructor called")
        except Exception as e:
            self.__logger.debug("Exception occured in constructor of Homer_db class")
            self.__logger.error(e)

    def query(self,query, values=None):
        try:
            if(values == None):
                self.get_cur().execute(query)
            else:
                self.get_cur().execute(query, values)
        except Exception as e:
            self. __logger.error(e)
            raise  #raising error to parent function call
        
    
    def close_success(self):
        self.__conn.commit()
        self.__cur.close()
        self.__conn.close()
        self.__logger.info("close_success: Connection closed")

    def close_failure(self):
        self.__conn.rollback()
        self.__cur.close()
        self.__conn.close()
        self.__logger.info("close_failure: Connection closed")
    
    def get_cur(self):
        if(self.__cur.closed):
            self.__cur = self.get_conn().cursor()
        return self.__cur
    
    def get_conn(self):
        if(self.__conn.closed == 1): 
            self.__conn= psycopg2.connect(database=config[self.__env]['database'],
                                    user=config[self.__env]['user'], 
                                    password=config[self.__env]['password'])
        return self.__conn
    
    def get_logger(self):
        return self.__logger

    def set_env_var(self, env):
        self.__env = env+"_server"
