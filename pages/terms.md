# Terms and Conditions

By participating in the GEMS-GER Groundwater Level Prediction Challenge, you agree to the following terms:

## 1. Data Usage & Intellectual Property
* **Academic Use:** The dataset provided (GEMS-GER) is for educational and competition purposes only. Commercial redistribution of the raw data is prohibited.
* **Winning Submissions:** Winners of the challenge agree to make their winning code (submission.zip) available under an open-source license (e.g., MIT or Apache 2.0) to allow for scientific verification.

## 2. Competition Integrity
* **No Manual Labeling:** Participants are strictly forbidden from manually labeling the test data or searching for the original Zenodo dataset to extract the hidden ground truth labels.
* **No External Data:** You may only use the provided dataset and static site features. The use of external meteorological data (e.g., from DWD or other sources) is not permitted unless specifically authorized by the organizers.
* **One Account per Person:** Multiple accounts per participant are not allowed. Collaborating in teams is encouraged, but a team must submit under a single account.

## 3. Submission Limits & Phases
* **Daily Limit:** You are limited to **5 submissions per day** during the Development Phase to prevent "leaderboard probing."
* **Final Selection:** At the end of the Development Phase, you must select **one** submission for the Final Phase. This submission will be re-evaluated against the private test set.

## 4. Resource Usage
* **Memory Constraints:** Submissions must run within the memory limits of the Codabench server (typically 4GB-8GB RAM). Models that require excessive resources or crash the ingestion program will be disqualified.
* **Training Time:** Your model's `fit` and `predict` logic must complete within the allotted time limit (e.g., 30 minutes for the 1M row dataset).

## 5. Disqualification
The organizers reserve the right to disqualify any participant found to be in violation of these rules or behaving in a way that undermines the fairness of the competition.
