from wheat.entity.config_entity import DataIngestionConfig
import sys,os
from wheat.exception import WheatException
from wheat.logger import logging
from wheat.entity.artifact_entity import DataIngestionArtifact
import pandas as pd
from sklearn.model_selection import train_test_split

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig ):
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise WheatException(e,sys)
    

    def download_wheat_data(self,) -> str:
        try:
            #extraction remote url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)
            logging.info(f"Downloading file from :[{download_url}] into :[{raw_data_dir}]")

            # Read the file from the url using pandas
            wheat_data_frame = pd.read_csv(download_url)
            # Write it to the file system
            # print(wheat_data_frame.head())
            wheat_data_frame.to_csv(os.path.join(raw_data_dir,"wheat.csv"),index=False)
            
            logging.info(f"File :[{raw_data_dir}] has been downloaded successfully.")
            return raw_data_dir

        except Exception as e:
            raise WheatException(e,sys) from e
    
    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            wheat_file_path = os.path.join(raw_data_dir,file_name)


            logging.info(f"Reading csv file: [{wheat_file_path}]")
            wheat_data_frame = pd.read_csv(wheat_file_path)
            

            logging.info(f"Splitting data into train and test")

            # Train test split
            train_set, test_set = train_test_split(wheat_data_frame, test_size=0.2, random_state=42)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        file_name)

            if train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                train_set.to_csv(train_file_path,index=False)

            if test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                test_set.to_csv(test_file_path,index=False)
            

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise WheatException(e,sys) from e

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            raw_data_dir =  self.download_wheat_data()
            return self.split_data_as_train_test()
        except Exception as e:
            raise WheatException(e,sys) from e
    
    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")
