## How to Participate

To participate in this challenge, you will submit your **code**, not your predictions. This ensures that your model is reproducible and can be evaluated on hidden data.

### 1. The Submission File
Your model logic must be contained in a single Python file named `submission.py`. This file **must** contain a function named `get_model()` that returns an object with Scikit-Learn compatible `.fit()` and `.predict()` methods.

We recommend using a `Pipeline` to bundle your preprocessing (handling metadata) and your regressor together.



### 2. The Model Interface
The evaluation platform will import your code and execute it as follows:

```python
from submission import get_model

# The platform initializes your model
model = get_model()

# The platform trains your model on the 1M row dataset
model.fit(X_train, y_train)

# The platform generates predictions on the test set
y_pred = model.predict(X_test)

```

### 3. Packaging for Upload

Once you have modified `solution/submission.py`, use the provided helper script to create your submission archive.

1. Open a terminal in the starting kit folder.
2. Run `python zip_submission.py`.
3. Upload the resulting `submission.zip` to the **"My Submissions"** tab on the Codabench platform.

### 4. Phases

* **Development Phase:** Your model is trained on the historical training set and evaluated on the **Public Test Set**. You receive immediate feedback on the leaderboard.
* **Final Phase:** At the end of the competition, your best submission will be evaluated on the **Private Test Set** (the most recent data). This determines the final ranking.

> **Note:** Refer to the **Timeline** section for specific dates and submission limits for each phase.
