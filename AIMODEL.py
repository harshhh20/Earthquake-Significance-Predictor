import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import pathlib


# Step 1: Load the dataset
# Replace 'path_to_dataset.csv' with the actual path to the downloaded dataset
file_path = pathlib.Path("C:/Users/prana/OneDrive/Desktop/project-bolt-sb1-wucddrqv/project/Earthquake_Dataset.csv")
df = pd.read_csv(file_path)



# Step 2: Preprocess the data
# Selecting features and target variable
features = ['magnitudo', 'state']
target = 'significance'

X = df[features]
y = df[target]

# Handling categorical variable 'state' using one-hot encoding
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['state'])
    ],
    remainder='passthrough'  # This leaves 'magnitudo' as is
)

# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train the model within a pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

model.fit(X_train, y_train)

# Step 5: Save the trained model
joblib.dump(model, 'random_forest_regressor.pkl')