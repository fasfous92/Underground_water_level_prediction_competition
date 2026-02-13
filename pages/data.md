# Data Description

This page provides details about the GEMS-GER dataset and the submission format.

## Dataset Overview
- **Total Samples:** 1,000,000 historical records.
- **Goal:** Predict groundwater depth (**GWL**) based on environmental factors.

## File Structure
The competition data is organized as follows:

- **Training Data:** `dev_phase/input_data/train/train.csv`
  - Contains features and the target variable `GWL`.
- **Test Features:** `dev_phase/input_data/test/test_features.csv`
  - Contains features for which you must provide predictions.
- **Sample Submission:** `dev_phase/input_data/test/sample_submission.csv`
  - A template file showing the exact format required for your results.

## Features and Target Variable
### Input Features (X)
Includes daily precipitation, temperature, soil moisture, and static well characteristics.

### Target Variable (y)
- **GWL:** Depth to groundwater in meters.

## 📋 Submission Format
Your model must output a CSV file that matches the structure of the sample found in the `test` folder.
- **Columns:** `Id` (matching the test feature index) and `GWL` (your prediction).
- **Header:** The file must include the header row `Id,GWL`.
- **Example:**
  ```csv
  Id,GWL
  0,5.23
  1,5.45
