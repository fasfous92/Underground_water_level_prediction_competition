# Seed: The Model Class


> **Important:** The input `X_train` and `X_test` are **Pandas DataFrames**. Your model must handle or drop the non-numeric columns (`well_id_str`, `date_dt`) to avoid errors during training.
Basically apply all the necessary feature engineer you see fit.

```python
class Model:
    def __init__(self):
        """
        Initialize your model here.
        You can define hyperparameters or internal pipelines.
        """
        pass

    def fit(self, X_train, y_train):
        """
        This handles the training logic.
        :param X_train: Pandas DataFrame of training features (1M rows).
        :param y_train: Pandas Series/Array of groundwater levels.
        """
        # Example: Drop strings before fitting
        X_numeric = X_train.drop(columns=['well_id_str', 'date_dt'], errors='ignore')
        
        # Your training logic here
        pass

    def predict(self, X_test):
        """
        This handles making predictions.
        :param X_test: Pandas DataFrame of testing features.
        :return: np.array of predictions.
        """
        # Example: Drop strings before predicting
        X_numeric = X_test.drop(columns=['well_id_str', 'date_dt'], errors='ignore')
        
        # Your prediction logic here
        return predictions
