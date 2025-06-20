from datetime import datetime
import os
import logging

# this module runs only once per interpreter session

#get logfile's name 
LOG_FILE=f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"

#create the logs directory if does not exist
logs_path=os.path.join("..","logs")
os.makedirs(logs_path,exist_ok=True)

#comple log file path for the loggings to get logged :D)
LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

#configuring the root logger
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="%(asctime)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

#testing the logging
# if __name__=="__main__":
#     logging.info("Set-up root logger")