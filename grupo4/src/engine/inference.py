import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import plot_tree

#view the dataset
crab_prediction = pd.read_csv('Datasources/categories.csv')
#copies data
data = crab_prediction.copy()
#initialize the encoder
encoder = LabelEncoder()

#template for the future crab categories
#this will encode categorical features with the target variables
data[''] = encoder.fit_transform(data[''])

