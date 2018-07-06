class FeatureExtractor:

    def __init__(self, data, features):
        self.string_features = {
            "UNKNOWN": 0,
            "MALE": 2,
            "FEMALE": 1,
            "PATIENT_REFUSAL": 3,
            "NOT_HISPANIC_OR_LATINO": 1,
            "HISPANIC_OR_LATINO": 2
        }
        self.vector = self.generate_vector(data=data, features=features)

    def generate_vector(self, data, features):
        vector = []

        for feature in features:
            value = data[feature]
            if isinstance(value, str):
                str_value = self.string_features.get(value)
                if str_value is None:
                    str_value = 0
                vector.append(str_value)
            elif isinstance(value, dict):
                vector.append(len(value))
            else:
                vector.append(len(value))
        return vector

        def create_vector_using_set(features, data):
        patient_value_dictionary = {}
        for set_value in features:
            for (patient_key, patient_value) in data.items():
                if patient_value == set_value :
                    if patient_value in patient_value_dictionary:
                        patient_value_dictionary[patient_value] = patient_value_dictionary[patient_value] + 1
                    else:
                        patient_value_dictionary[patient_value] = 1
                else:
                    if patient_value not in patient_value_dictionary:
                        patient_value_dictionary[set_value] = 0

        patient_vector = []
        for value in patient_value_dictionary.values():
            patient_vector.append(value)
        return patient_vector
