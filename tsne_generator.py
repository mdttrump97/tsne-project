import os
import json
import numpy as np
import time

from ggplot import *
from dataframe_generator import DataFrameGenerator
from nci_match_pap_common import mongo_connection, logging_configuration
from sklearn.decomposition import PCA

from sklearn.manifold import TSNE




class TSNEGenerator:

    def __init__(self):
        self.match_database = mongo_connection.MongoConnection().match_database
        self.patient_projection_document = self.load_patient_projection_document()
        self.logger = logging_configuration.LoggingConfiguration().logger

    def run(self, perplexity, color_field):
        print("Retrieving patients from MongoDB")
        patient_files = self.retrieve_all_patients_from_database()
        print("Creating Dataframe from Patient Data")
        forget_list = ['patientSequenceNumber', "_id"]
        columns = list(key for key, value in self.patient_projection_document.items() if str(key) not in forget_list)
        index = range(0, len(patient_files))
        df = DataFrameGenerator(patient_data=patient_files, columns=columns, index=index).data_frame

        self.run_tsne(perplexity=perplexity, color_field=color_field, patient_files=patient_files, columns=columns,df=df)
        # self.run_pca(df=df, columns=columns, length=len(patient_files), color_field=color_field)

    def run_tsne(self, perplexity, color_field, patient_files, columns, df):
        index = range(0, len(patient_files))
        print(df[columns].values)
        n_sne = 276
        rndperm = np.random.permutation(df.shape[0])

        for column in columns:
            time_start = time.time()
            tsne = TSNE(n_components=2, verbose=1, perplexity=perplexity, n_iter=300)
            tsne_results = tsne.fit_transform(df.loc[index[:n_sne], columns].values)

            for value in df[columns].values:
                print(value)

            print('t-SNE done! Time elapsed: {} seconds'.format(time.time() - time_start))

            df_tsne = df.loc[rndperm[:n_sne], :].copy()
            df_tsne['x-tsne'] = tsne_results[:, 0]
            df_tsne['y-tsne'] = tsne_results[:, 1]

            chart = ggplot(df_tsne, aes(x='x-tsne', y='y-tsne', color=column)) \
                    + geom_point(size=70) \
                    + ggtitle("tSNE dimensions colored by " + str(column) + " Perplexity: " + str(perplexity))
            print(chart)

    def run_pca(self, df, columns, length, color_field):
        index = range(0, length)
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(df[columns].values)
        print(df[columns].values)
        df['pca-one'] = pca_result[:, 0]
        df['pca-two'] = pca_result[:, 1]
        #df['pca-three'] = pca_result[:, 2]
        print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))
        chart = ggplot(df.loc[index[:276], :], aes(x='pca-one', y='pca-two', color=color_field)) \
                + geom_point(size=75) \
                + ggtitle("First and Second Principal Components colored by "+ str(color_field))
        print(chart)

    @staticmethod
    def load_patient_projection_document():
        file_path = os.path.join(os.path.dirname(__file__), "patient_projection_document.json")
        with open(file_path) as projection_document_json:
            return json.load(projection_document_json)

    def retrieve_all_patients_from_database(self):
        patient_data = self.match_database.patient.find({}, self.patient_projection_document)
        return list(patient for patient in patient_data)


if __name__ == "__main__":
        TSNEGenerator().run(perplexity=30, color_field='diseases')

