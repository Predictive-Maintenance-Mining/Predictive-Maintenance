"""
Mining Truck Fleet - End-to-End Machine Learning Pipeline
This script performs EDA, model training, and generates predictions
with output matching the original CSV structure.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*80)
print("MINING TRUCK FLEET - END-TO-END ML PIPELINE")
print("="*80)

# ============================================================================
# STEP 1: DATA LOADING
# ============================================================================
print("\n" + "="*80)
print("STEP 1: DATA LOADING")
print("="*80)

df = pd.read_csv('mining_truck_fleet_cleaned.csv')
print(f"\nDataset Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"\nFirst few rows:")
print(df.head())

# ============================================================================
# STEP 2: EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================================
print("\n" + "="*80)
print("STEP 2: EXPLORATORY DATA ANALYSIS")
print("="*80)

# Data Info
print("\n--- Data Types and Missing Values ---")
print(df.info())

print("\n--- Statistical Summary ---")
print(df.describe())

# Check for missing values
print("\n--- Missing Values ---")
print(df.isnull().sum())

# Distribution of target variable (Vehicle_Status)
print("\n--- Vehicle Status Distribution ---")
print(df['Vehicle_Status'].value_counts())
print("\n--- Risk Level Distribution ---")
print(df['Risk_Level'].value_counts())

# Create visualizations
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Exploratory Data Analysis - Mining Truck Fleet', fontsize=16, fontweight='bold')

# 1. Vehicle Status Distribution
df['Vehicle_Status'].value_counts().plot(kind='bar', ax=axes[0, 0], color='skyblue')
axes[0, 0].set_title('Vehicle Status Distribution')
axes[0, 0].set_xlabel('Status')
axes[0, 0].set_ylabel('Count')
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Risk Level Distribution
df['Risk_Level'].value_counts().plot(kind='bar', ax=axes[0, 1], color='coral')
axes[0, 1].set_title('Risk Level Distribution')
axes[0, 1].set_xlabel('Risk Level')
axes[0, 1].set_ylabel('Count')
axes[0, 1].tick_params(axis='x', rotation=45)

# 3. Alert Type Distribution
df['Alert_Type'].value_counts().plot(kind='bar', ax=axes[0, 2], color='lightgreen')
axes[0, 2].set_title('Alert Type Distribution')
axes[0, 2].set_xlabel('Alert Type')
axes[0, 2].set_ylabel('Count')
axes[0, 2].tick_params(axis='x', rotation=45)

# 4. Downtime Hours Distribution
axes[1, 0].hist(df['Downtime_Hours'], bins=20, color='purple', alpha=0.7, edgecolor='black')
axes[1, 0].set_title('Downtime Hours Distribution')
axes[1, 0].set_xlabel('Hours')
axes[1, 0].set_ylabel('Frequency')

# 5. Site-wise Vehicle Status
site_status = pd.crosstab(df['Site_Name'], df['Vehicle_Status'])
site_status.plot(kind='bar', stacked=True, ax=axes[1, 1])
axes[1, 1].set_title('Site-wise Vehicle Status')
axes[1, 1].set_xlabel('Site')
axes[1, 1].set_ylabel('Count')
axes[1, 1].tick_params(axis='x', rotation=45)
axes[1, 1].legend(title='Status', bbox_to_anchor=(1.05, 1), loc='upper left')

# 6. Fuel Consumption by Risk Level
# Extract numeric fuel consumption
df['Fuel_Numeric'] = df['Fuel_Consumption'].str.extract('(\d+)').astype(float)
df.boxplot(column='Fuel_Numeric', by='Risk_Level', ax=axes[1, 2])
axes[1, 2].set_title('Fuel Consumption by Risk Level')
axes[1, 2].set_xlabel('Risk Level')
axes[1, 2].set_ylabel('Fuel Consumption (L/hr)')
plt.suptitle('')  # Remove default title

plt.tight_layout()
plt.savefig('/home/claude/eda_visualizations.png', dpi=300, bbox_inches='tight')
print("\n✓ EDA visualizations saved to 'eda_visualizations.png'")

# Correlation analysis for numeric features
print("\n--- Correlation Analysis ---")
numeric_cols = ['Downtime_Hours', 'Fuel_Numeric']
correlation = df[numeric_cols].corr()
print(correlation)

# ============================================================================
# STEP 3: FEATURE ENGINEERING
# ============================================================================
print("\n" + "="*80)
print("STEP 3: FEATURE ENGINEERING")
print("="*80)

# Create a copy for feature engineering
df_ml = df.copy()

# Extract production loss amount (remove $ and commas)
df_ml['Production_Loss_Numeric'] = df_ml['Estimated_Production_Loss'].str.replace('$', '').str.replace(',', '').astype(float)

# Convert date to datetime and extract features
df_ml['Date'] = pd.to_datetime(df_ml['Date'])
df_ml['Day_of_Week'] = df_ml['Date'].dt.dayofweek
df_ml['Day_of_Month'] = df_ml['Date'].dt.day

# Binary encoding for Safety_Risk
df_ml['Safety_Risk_Binary'] = (df_ml['Safety_Risk'] == 'Yes').astype(int)

# Label encoding for categorical variables
label_encoders = {}
categorical_cols = ['Site_Name', 'Truck_ID', 'Driver_Name', 'Alert_Type']

for col in categorical_cols:
    le = LabelEncoder()
    df_ml[f'{col}_Encoded'] = le.fit_transform(df_ml[col])
    label_encoders[col] = le
    print(f"✓ Encoded {col}: {len(le.classes_)} unique values")

# ============================================================================
# STEP 4: MODEL TRAINING - PREDICT VEHICLE STATUS
# ============================================================================
print("\n" + "="*80)
print("STEP 4: MODEL TRAINING - PREDICT VEHICLE STATUS")
print("="*80)

# Select features for modeling
feature_cols = [
    'Site_Name_Encoded', 'Truck_ID_Encoded', 'Driver_Name_Encoded',
    'Alert_Type_Encoded', 'Downtime_Hours', 'Production_Loss_Numeric',
    'Fuel_Numeric', 'Safety_Risk_Binary', 'Day_of_Week', 'Day_of_Month'
]

X = df_ml[feature_cols]
y_status = df_ml['Vehicle_Status']
y_risk = df_ml['Risk_Level']

# Split data
X_train, X_test, y_status_train, y_status_test = train_test_split(
    X, y_status, test_size=0.2, random_state=42, stratify=y_status
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\nTraining set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Train Random Forest Classifier for Vehicle Status
print("\n--- Training Random Forest for Vehicle Status ---")
rf_status = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

rf_status.fit(X_train_scaled, y_status_train)

# Cross-validation
cv_scores = cross_val_score(rf_status, X_train_scaled, y_status_train, cv=5)
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

# Predictions
y_status_pred = rf_status.predict(X_test_scaled)

# Evaluation
print("\n--- Vehicle Status Model Performance ---")
print(f"Accuracy: {accuracy_score(y_status_test, y_status_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_status_test, y_status_pred))

# Confusion Matrix
cm = confusion_matrix(y_status_test, y_status_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=rf_status.classes_, 
            yticklabels=rf_status.classes_)
plt.title('Confusion Matrix - Vehicle Status Prediction')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.tight_layout()
plt.savefig('/home/claude/confusion_matrix_status.png', dpi=300, bbox_inches='tight')
print("✓ Confusion matrix saved to 'confusion_matrix_status.png'")

# Feature Importance
feature_importance = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': rf_status.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n--- Feature Importance (Top 10) ---")
print(feature_importance.head(10))

plt.figure(figsize=(10, 6))
plt.barh(feature_importance['Feature'][:10], feature_importance['Importance'][:10])
plt.xlabel('Importance')
plt.title('Top 10 Feature Importance - Vehicle Status Prediction')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('/home/claude/feature_importance.png', dpi=300, bbox_inches='tight')
print("✓ Feature importance chart saved to 'feature_importance.png'")

# ============================================================================
# STEP 5: MODEL TRAINING - PREDICT RISK LEVEL
# ============================================================================
print("\n" + "="*80)
print("STEP 5: MODEL TRAINING - PREDICT RISK LEVEL")
print("="*80)

X_train_risk, X_test_risk, y_risk_train, y_risk_test = train_test_split(
    X, y_risk, test_size=0.2, random_state=42, stratify=y_risk
)

X_train_risk_scaled = scaler.fit_transform(X_train_risk)
X_test_risk_scaled = scaler.transform(X_test_risk)

# Train Gradient Boosting Classifier for Risk Level
print("\n--- Training Gradient Boosting for Risk Level ---")
gb_risk = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)

gb_risk.fit(X_train_risk_scaled, y_risk_train)

# Predictions
y_risk_pred = gb_risk.predict(X_test_risk_scaled)

# Evaluation
print("\n--- Risk Level Model Performance ---")
print(f"Accuracy: {accuracy_score(y_risk_test, y_risk_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_risk_test, y_risk_pred))

# ============================================================================
# STEP 6: GENERATE PREDICTIONS FOR ENTIRE DATASET
# ============================================================================
print("\n" + "="*80)
print("STEP 6: GENERATE PREDICTIONS FOR ENTIRE DATASET")
print("="*80)

# Scale all features
X_all_scaled = scaler.fit_transform(df_ml[feature_cols])

# Make predictions
df_ml['Predicted_Vehicle_Status'] = rf_status.predict(X_all_scaled)
df_ml['Predicted_Risk_Level'] = gb_risk.predict(X_all_scaled)

# Get prediction probabilities
status_proba = rf_status.predict_proba(X_all_scaled)
risk_proba = gb_risk.predict_proba(X_all_scaled)

df_ml['Status_Confidence'] = status_proba.max(axis=1)
df_ml['Risk_Confidence'] = risk_proba.max(axis=1)

print(f"\n✓ Generated predictions for {len(df_ml)} records")
print(f"\nPredicted Vehicle Status Distribution:")
print(df_ml['Predicted_Vehicle_Status'].value_counts())
print(f"\nPredicted Risk Level Distribution:")
print(df_ml['Predicted_Risk_Level'].value_counts())

# ============================================================================
# STEP 7: CREATE OUTPUT CSV WITH EXACT ORIGINAL STRUCTURE
# ============================================================================
print("\n" + "="*80)
print("STEP 7: CREATING OUTPUT CSV WITH ORIGINAL STRUCTURE")
print("="*80)

# Create output dataframe with EXACT original columns
output_df = df.copy()

# Add prediction columns (optional - you can include or exclude these)
# For exact match, we'll create a separate predictions file
output_df.to_csv('mining_truck_fleet_output.csv', index=False)
print("✓ Original structure output saved to 'mining_truck_fleet_output.csv'")

# Create enhanced output with predictions
output_enhanced = df.copy()
output_enhanced['Predicted_Vehicle_Status'] = df_ml['Predicted_Vehicle_Status']
output_enhanced['Predicted_Risk_Level'] = df_ml['Predicted_Risk_Level']
output_enhanced['Status_Prediction_Confidence'] = df_ml['Status_Confidence'].round(3)
output_enhanced['Risk_Prediction_Confidence'] = df_ml['Risk_Confidence'].round(3)

output_enhanced.to_csv('mining_truck_fleet_with_predictions.csv', index=False)
print("✓ Enhanced output with predictions saved to 'mining_truck_fleet_with_predictions.csv'")

# ============================================================================
# STEP 8: MODEL PERFORMANCE SUMMARY
# ============================================================================
print("\n" + "="*80)
print("STEP 8: MODEL PERFORMANCE SUMMARY")
print("="*80)

summary = {
    'Dataset Size': len(df),
    'Training Set Size': len(X_train),
    'Test Set Size': len(X_test),
    'Vehicle Status Model Accuracy': f"{accuracy_score(y_status_test, y_status_pred):.4f}",
    'Risk Level Model Accuracy': f"{accuracy_score(y_risk_test, y_risk_pred):.4f}",
    'Features Used': len(feature_cols),
    'Vehicle Status Classes': len(rf_status.classes_),
    'Risk Level Classes': len(gb_risk.classes_)
}

print("\n--- Pipeline Summary ---")
for key, value in summary.items():
    print(f"{key}: {value}")

# ============================================================================
# STEP 9: INSIGHTS AND RECOMMENDATIONS
# ============================================================================
print("\n" + "="*80)
print("STEP 9: KEY INSIGHTS")
print("="*80)

print("\n--- High-Risk Predictions ---")
high_risk = df_ml[df_ml['Predicted_Risk_Level'].isin(['High', 'Critical'])]
print(f"Number of vehicles predicted as High/Critical risk: {len(high_risk)}")
print(f"\nTop 5 trucks with highest downtime:")
print(df_ml.nlargest(5, 'Downtime_Hours')[['Truck_ID', 'Site_Name', 'Downtime_Hours', 
                                             'Predicted_Vehicle_Status', 'Predicted_Risk_Level']])

print("\n--- Safety Concerns ---")
safety_issues = df_ml[df_ml['Safety_Risk_Binary'] == 1]
print(f"Vehicles with safety risks: {len(safety_issues)}")
print(f"Percentage: {len(safety_issues)/len(df_ml)*100:.2f}%")

print("\n--- Site-wise Analysis ---")
site_summary = df_ml.groupby('Site_Name').agg({
    'Downtime_Hours': 'mean',
    'Production_Loss_Numeric': 'sum',
    'Safety_Risk_Binary': 'sum'
}).round(2)
print(site_summary)

print("\n" + "="*80)
print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
print("="*80)

print("\n📊 Generated Files:")
print("   1. eda_visualizations.png - EDA charts")
print("   2. confusion_matrix_status.png - Model performance")
print("   3. feature_importance.png - Feature analysis")
print("   4. mining_truck_fleet_output.csv - Original structure output")
print("   5. mining_truck_fleet_with_predictions.csv - Enhanced with ML predictions")

print("\n" + "="*80)
