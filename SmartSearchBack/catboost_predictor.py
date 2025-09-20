import joblib
from catboost import CatBoostClassifier


class IntentPredictor:
    def __init__(self, model_path: str = "catboost_model.cbm", vectorizer_path: str = "tfidf_vectorizer.pkl"):
        self.model = CatBoostClassifier()
        self.model.load_model(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    def predict(self, text: str):
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]
