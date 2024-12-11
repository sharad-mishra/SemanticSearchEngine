import pandas as pd

# Load the dataset
questions = pd.read_csv('data/Questions.csv', encoding='latin1')
answers = pd.read_csv('data/Answers.csv', encoding='latin1')

# Clean data (e.g., remove null values, etc.)
questions.dropna(inplace=True)
answers.dropna(inplace=True)

# Save cleaned data
questions.to_csv('data/cleaned_Questions.csv', index=False)
answers.to_csv('data/cleaned_Answers.csv', index=False)
