import os
import sys
import ast
import pandas as pd
import pickle
from books_recommender.logger.log import logging
from books_recommender.config.configuration import AppConfiguration
from books_recommender.exception.exception_handler import AppException



class Datavalidation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.data_validation_config = app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e
        
    
    def preprocess_data(self):
        try:
            ratings = pd.read_csv(self.data_validation_config.ratings_csv_file, sep=";", on_bad_lines='skip',encoding='latin-1')
            books = pd.read_csv(self.data_validation_config.books_csv_file,sep=';', on_bad_lines='skip',encoding='latin-1')

            logging.info(f"Shape of rating data file: {ratings.shape}")
            logging.info(f"Shape of books data file:{books.shape}")

            # Here Image URL column is important for the poster, hence we will keep it
            books = books[['ISBN','Book-Title','Year-Of-Publication','Publisher','Image-URL-L']]
            # Lets rename the column names in books
            books.rename(columns={"Book-Title":'Title',
                                'Book-Author':"Author",
                                "Year-Of-Publication":'Year',
                                "Publisher":"Publisher",
                                "Image-URL-L":"Image_url"},inplace=True)
            
            # Lets rename the column names in ratings
            ratings.rename(columns={"User-ID":'user_id',
                                'Book-Rating':'rating'},inplace=True)
            
            # Storing users who had rated atleast more than 200 books
            x = ratings['user_id'].value_counts() > 200
            y = x[x].index
            ratings = ratings[ratings['user_id'].isin(y)]

            # merge ratings with books
            ratings_with_books = ratings.merge(books, on='ISBN')
            number_rating = ratings_with_books.groupby('Title')['rating'].count().reset_index()
            number_rating.rename(columns={'rating':'num_of_rating'},inplace=True)
            final_rating = ratings_with_books.merge(number_rating, on='Title')

            # books which got atleast 50 rating of user
            final_rating = final_rating[final_rating['num_of_rating'] >=50]

            # drop the duplicates
            final_rating.drop_duplicates(['user_id','Title'],inplace=True)
            logging.info(f"Shape of the final clean dataset: {final_rating.shape}")

            # save the clean data for transformation
            os.makedirs(self.data_validation_config.clean_data_dir, exist_ok=True)
            final_rating.to_csv(os.path.join(self.data_validation_config.clean_data_dir,'clean_data.csv'),index=False)
            logging.info(f"Saved the clean data to {self.data_validation_config.clean_data_dir}")

            # save final rating objects for web app
            os.makedirs(self.data_validation_config.serialized_objects_dir,exist_ok=True)
            pickle.dump(final_rating,open(os.path.join(self.data_validation_config.serialized_objects_dir,"final_rating.pkl"),'wb'))
            logging.info(f"Saved the final_rating serialization object to {self.data_validation_config.serialized_objects_dir}")

        except Exception as e:
            raise AppException(e,sys) from e
        


    def initiate_data_validation(self):
        try:
            logging.info(f"{'='*20}Data Validation log started.{'='*20} ")
            self.preprocess_data()
            logging.info(f"{'='*20} Data Validation log completed.{'='*20}\n\n")
        except Exception as e:
            raise AppException(e,sys) from e