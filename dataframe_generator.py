from feature_extractor import FeatureExtractor


class DataFrameGenerator:

    # def __init__(self, patient_data, index, columns):
    #     self.data = self.extract_features_from_data(patient_data, features=columns)
    #     self.data_frame = pd.DataFrame(self.data, index=index, columns=columns)

    def __init__(self, patient_json_files):
        cleaned_data = self.clean_all_patient_data(patient_json_files)
        self.standard_patient_list = set([])


    def clean_all_patient_data(self, patient_files):
        pass

    def generate_clean_text_patient(self, patient):
        patient = self.remove_empty_entries(patient)
        patient = self.extract_all_values_from_patient_into_set(patient)
        patient_word_list = self.generate_patient_word_list(patient)

    @staticmethod
    def generate_patient_word_list(patient):
        return None


    @staticmethod
    def remove_empty_entries(entry):
        if isinstance(entry, dict):
            return dict((k, DataFrameGenerator.remove_empty_entries(v)) for k, v in entry.items() if v and DataFrameGenerator.remove_empty_entries(v))
        elif isinstance(entry, list):
            return [DataFrameGenerator.remove_empty_entries(v) for v in entry if v and DataFrameGenerator.remove_empty_entries(v)]
        else:
            return entry

    def extract_all_values_from_patient_into_set(self, patient):
        patient_set = set([])
        for (key, val) in patient.items():
            if isinstance(val, str):
                patient_set.add(val)
            elif isinstance(val, dict):


    @staticmethod
    def extract_features_from_data(patient_list, features):
        return list(FeatureExtractor(patient, features=features).vector for patient in patient_list)