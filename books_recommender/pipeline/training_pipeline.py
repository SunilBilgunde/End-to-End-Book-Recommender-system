from books_recommender.components.stage_00_data_ingestion import DataIngestion
from books_recommender.components.stage_01_data_validation import Datavalidation






class TrainingPipeline:
    def __init__(self):
        self.data_ingestion  =DataIngestion()
        self.data_validation = Datavalidation()

    def start_training_pipeline(self):
        """
        starts the training pipeline
        :return: none
        """
        self.data_ingestion.initiate_data_ingestion()
        self.data_validation.initiate_data_validation()