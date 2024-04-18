# TODO: Importing necessary libraries and modules
import pandas as pd
import csv
from sklearn.preprocessing import LabelEncoder
data = []
file_path = 'C:/Users/Fernando/PycharmProjects/week07-tutorial19-FernandoNGR/helpers/data.csv'

column_names = ['AccelX', 'AccelY', 'AccelZ', 'GyroX', 'GyroY', 'GyroZ', 'Label', 'Sep']

with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # Only append rows with exactly 7 entries to match the specified columns
        if len(row) == 8:
            processed_row = []
            for entry in row[:-1]:  # Exclude the last entry (Label) from this processing
                # Split on colon, strip whitespace, and take the numeric part
                numeric_value = entry.split(':')[1].strip()
                processed_row.append(float(numeric_value))
            processed_row.append(row[-1])  # Add the Label back as is
            data.append(processed_row)
# Create the DataFrame using the specified column names
df = pd.DataFrame(data, columns=column_names)# Assuming the first row is headers
# Display the first few rows to check the DataFrame
print(df)

le = LabelEncoder()
df['Label'] = le.fit_transform(df['Label'])

print(df)
df['Sep'] = df['Sep'].apply(lambda x: 1 if 'True' in x else 0)
# Scaling features

# Output for demonstration
# if 'Sep' in df.columns:
#     df.loc[0, 'Sep'] = 1

df.to_csv('Andres.csv')