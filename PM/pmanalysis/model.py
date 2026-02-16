"""
End-to-End Mining Predictive Maintenance ML Pipeline
Input: Raw sensor time-series data
Output: Dashboard-ready CSV matching exact schema
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

# =====================================================
# STEP 1: DEFINE RAW INPUT DATA REQUIREMENTS
# =====================================================
PLANT_HIERARCHY = {
    "Crushing Plant": {
        "Jaw Crusher": ["Bearing", "Motor"],
        "Cone Crusher": ["Bearing", "Gearbox"]
    },
    "Grinding Plant": {
        "Ball Mill": ["Bearing", "Gearbox", "Motor"],
        "SAG Mill": ["Bearing", "Motor"]
    },
    "Separation / Beneficiation Plant": {
        "Flotation Pump": ["Pump", "Motor"],
        "Magnetic Separator": ["Coil", "Bearing"]
    },
    "Dewatering Plant": {
        "Thickener": ["Hydraulic", "Motor"],
        "Filter Press": ["Hydraulic", "Pump"]
    },
    "Conveyor & Material Handling": {
        "Conveyor Belt": ["Belt", "Roller"],
        "Drive Pulley": ["Bearing", "Motor"]
    },
    "Utilities (Power Water Compressors)": {
        "Air Compressor": ["Motor", "Valve"],
        "Power Transformer": ["Coil", "Cooling"]
    }
}

SENSOR_MAPPING = {
    "Bearing": ["Vibration", "Temperature"],
    "Motor": ["Temperature", "Power"],
    "Gearbox": ["Vibration", "Temperature"],
    "Pump": ["Pressure", "Vibration"],
    "Hydraulic": ["Pressure", "Temperature"],
    "Belt": ["Speed", "Wear"],
    "Roller": ["Vibration"],
    "Valve": ["Pressure"],
    "Coil": ["Temperature"],
    "Cooling": ["Temperature"]
}

SENSOR_OPERATIONAL_RANGES = {
    "Vibration": {"healthy": (1.5, 3.5), "warning": (3.5, 4.5), "critical": (4.5, 6.0)},
    "Temperature": {"healthy": (50, 75), "warning": (75, 85), "critical": (85, 100)},
    "Pressure": {"healthy": (6.0, 9.0), "warning": (9.0, 10.0), "critical": (10.0, 12.0)},
    "Power": {"healthy": (40, 160), "warning": (160, 200), "critical": (200, 250)},
    "Speed": {"healthy": (2.0, 3.5), "warning": (3.5, 4.5), "critical": (4.5, 5.5)},
    "Wear": {"healthy": (0, 25), "warning": (25, 35), "critical": (35, 50)}
}

COMPONENT_STRESS_FACTORS = {
    "Bearing": 1.3, "Motor": 1.2, "Gearbox": 1.4, "Pump": 1.5,
    "Hydraulic": 1.2, "Belt": 1.6, "Roller": 1.1, "Valve": 1.0,
    "Coil": 1.3, "Cooling": 1.0
}

# =====================================================
# STEP 2: GENERATE RAW SENSOR TIME-SERIES DATA
# =====================================================
def generate_raw_timeseries_data(plants=5, timesteps=1000):
    """
    Generate raw sensor time-series data simulating real operational conditions
    Returns: DataFrame with columns [plant_id, sub_plant, equipment, component, 
             sensor_type, timestamp, readings (array)]
    """
    plant_ids = [f"Plant-{i}" for i in range(1, plants + 1)]
    base_timestamp = datetime(2024, 2, 8, 0, 0, 0)
    
    raw_data = []
    
    for plant_id in plant_ids:
        for sub_plant, equipments in PLANT_HIERARCHY.items():
            for equipment, components in equipments.items():
                for component in components:
                    sensors = SENSOR_MAPPING.get(component, ["General"])
                    
                    component_health_trajectory = np.linspace(
                        np.random.uniform(85, 95),
                        np.random.uniform(45, 75),
                        timesteps
                    )
                    
                    for sensor_type in sensors:
                        ranges = SENSOR_OPERATIONAL_RANGES[sensor_type]
                        stress = COMPONENT_STRESS_FACTORS[component]
                        
                        readings = []
                        for step in range(timesteps):
                            health = component_health_trajectory[step]
                            health_degradation = (100 - health) / 100
                            
                            if sensor_type == "Wear":
                                base_value = ranges["healthy"][0] + health_degradation * (
                                    ranges["critical"][1] - ranges["healthy"][0]
                                )
                            else:
                                base_value = (ranges["healthy"][0] + ranges["healthy"][1]) / 2
                                base_value += health_degradation * stress * (
                                    ranges["critical"][1] - base_value
                                )
                            
                            noise = np.random.normal(0, base_value * 0.08)
                            reading = max(base_value + noise, 0)
                            readings.append(reading)
                        
                        raw_data.append({
                            'plant_id': plant_id,
                            'sub_plant': sub_plant,
                            'equipment': equipment,
                            'component': component,
                            'sensor_type': sensor_type,
                            'timestamp': base_timestamp,
                            'readings': readings,
                            'health_trajectory': component_health_trajectory
                        })
    
    return pd.DataFrame(raw_data)

# =====================================================
# STEP 3: FEATURE ENGINEERING FROM TIME-SERIES
# =====================================================
def extract_features_from_timeseries(readings):
    """Extract statistical and temporal features from sensor readings"""
    recent = readings[-100:]
    
    features = {
        'mean': np.mean(recent),
        'std': np.std(recent),
        'max': np.max(recent),
        'min': np.min(recent),
        'median': np.median(recent),
        'rms': np.sqrt(np.mean(np.square(recent))),
        'peak_to_peak': np.max(recent) - np.min(recent),
        'trend': np.polyfit(range(len(recent)), recent, 1)[0],
        'acceleration': np.polyfit(range(len(recent)), recent, 2)[0],
        'cv': np.std(recent) / (np.mean(recent) + 1e-10),
        'skew': pd.Series(recent).skew(),
        'kurtosis': pd.Series(recent).kurtosis(),
        'latest': recent[-1]
    }
    
    if len(recent) >= 20:
        features['rolling_std'] = pd.Series(recent).rolling(20).std().iloc[-1]
        features['rolling_max'] = pd.Series(recent).rolling(20).max().iloc[-1]
    else:
        features['rolling_std'] = features['std']
        features['rolling_max'] = features['max']
    
    return features

def engineer_features(raw_df):
    """Apply feature engineering to raw time-series data"""
    engineered = []
    
    for idx, row in raw_df.iterrows():
        features = extract_features_from_timeseries(row['readings'])
        sensor_type = row['sensor_type']
        ranges = SENSOR_OPERATIONAL_RANGES[sensor_type]
        
        features['sensor_normalized'] = (features['latest'] - ranges["healthy"][0]) / (
            ranges["critical"][1] - ranges["healthy"][0]
        )
        features['threshold_exceedance'] = int(features['latest'] > ranges["warning"][1])
        features['stress_factor'] = COMPONENT_STRESS_FACTORS[row['component']]
        
        anomaly_score = 0
        if features['latest'] > ranges["warning"][1]:
            anomaly_score += 1
        if abs(features['trend']) > features['std']:
            anomaly_score += 1
        if features['cv'] > 0.3:
            anomaly_score += 1
        
        features['anomaly_detected'] = bool(anomaly_score >= 2)
        
        engineered.append({
            **row.to_dict(),
            **features
        })
    
    return pd.DataFrame(engineered)

# =====================================================
# STEP 4: ML MODEL - HEALTH SCORE PREDICTOR
# =====================================================
class HealthScoreModel:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=150, max_depth=12, min_samples_split=4,
            random_state=42, n_jobs=-1
        )
        self.scaler = StandardScaler()
    
    def train(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
    
    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        return np.clip(predictions, 40, 95).astype(int)

# =====================================================
# STEP 5: ML MODEL - RISK CLASSIFIER
# =====================================================
class RiskClassificationModel:
    def __init__(self):
        self.model = GradientBoostingClassifier(
            n_estimators=120, max_depth=6, learning_rate=0.12,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.risk_labels = {
            0: "Low Failure Risk",
            1: "Medium Failure Risk",
            2: "High Failure Risk"
        }
    
    def train(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
    
    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        risk_codes = self.model.predict(X_scaled)
        return [self.risk_labels[code] for code in risk_codes]

# =====================================================
# STEP 6: BUSINESS LOGIC FUNCTIONS
# =====================================================
def compute_status(health_score):
    if health_score >= 85: return "Healthy"
    elif health_score >= 70: return "Warning"
    else: return "Critical"

def compute_maintenance_type(health_score):
    if health_score >= 85: return "Proactive"
    elif health_score >= 70: return "Preventive"
    else: return "Predictive"

def compute_action_required(health_score):
    if health_score >= 85: return "Continue monitoring"
    elif health_score >= 70: return "Plan inspection"
    else: return "Immediate inspection & shutdown planning"

def compute_severity(health_score):
    if health_score >= 85: return "Normal"
    elif health_score >= 70: return "Warning"
    else: return "Critical"

def compute_priority(health_score):
    if health_score >= 85: return "Low"
    elif health_score >= 70: return "Medium"
    else: return "High"

def compute_failure_days(health_score, anomaly, stress_factor):
    base_rate = 0.018
    
    if health_score < 65:
        days = (health_score - 40) / (base_rate * 12 * stress_factor)
    elif health_score < 80:
        days = (health_score - 50) / (base_rate * 6 * stress_factor)
    else:
        days = (health_score - 70) / (base_rate * 3 * stress_factor)
    
    if anomaly:
        days *= 0.55
    
    return max(int(days), 1)

def compute_due_date(timestamp, health_score):
    if health_score < 70: return timestamp + timedelta(days=1)
    elif health_score < 85: return timestamp + timedelta(days=7)
    else: return timestamp + timedelta(days=14)

def assign_owner(completed):
    if completed:
        return np.random.choice(["Operations Team", "Maintenance Team"], p=[0.65, 0.35])
    return "Unassigned"

# =====================================================
# STEP 7: MAIN PIPELINE
# =====================================================
def main_pipeline():
    print("="*80)
    print("MINING PREDICTIVE MAINTENANCE ML PIPELINE")
    print("="*80)
    
    print("\n[1/8] Generating raw sensor time-series data...")
    raw_df = generate_raw_timeseries_data(plants=5, timesteps=1000)
    print(f"      Generated {len(raw_df)} sensor streams")

    output_file = 'data.csv'
    raw_df.to_csv(output_file, index=False)
    
    print("\n[2/8] Engineering features from time-series...")
    feature_df = engineer_features(raw_df)
    print(f"      Extracted {len([c for c in feature_df.columns if c not in raw_df.columns])} features per sensor")
    
    print("\n[3/8] Training Health Score prediction model...")
    feature_cols = ['mean', 'std', 'max', 'min', 'rms', 'trend', 'cv', 'sensor_normalized',
                    'threshold_exceedance', 'stress_factor', 'rolling_std', 'acceleration']
    
    X_health = feature_df[feature_cols].fillna(0)
    y_health = feature_df['health_trajectory'].apply(lambda x: x[-1])
    
    health_model = HealthScoreModel()
    health_model.train(X_health, y_health)
    
    feature_df['health_score'] = health_model.predict(X_health)
    print(f"      RMSE: {np.sqrt(np.mean((feature_df['health_score'] - y_health)**2)):.2f}")
    
    print("\n[4/8] Training Risk Classification model...")
    risk_feature_cols = ['health_score', 'anomaly_detected', 'sensor_normalized', 
                         'trend', 'threshold_exceedance']
    
    X_risk = feature_df[risk_feature_cols].copy()
    X_risk['anomaly_detected'] = X_risk['anomaly_detected'].astype(int)
    
    y_risk = feature_df['health_score'].apply(
        lambda h: 2 if h < 65 else (1 if h < 80 else 0)
    )
    
    risk_model = RiskClassificationModel()
    risk_model.train(X_risk, y_risk)
    
    feature_df['ml_failure_risk'] = risk_model.predict(X_risk)
    print(f"      Accuracy: {np.mean(y_risk == [0 if 'Low' in r else 1 if 'Med' in r else 2 for r in feature_df['ml_failure_risk']]):.2%}")
    
    print("\n[5/8] Computing derived business metrics...")
    feature_df['status'] = feature_df['health_score'].apply(compute_status)
    feature_df['maintenance_type'] = feature_df['health_score'].apply(compute_maintenance_type)
    feature_df['action_required'] = feature_df['health_score'].apply(compute_action_required)
    feature_df['severity'] = feature_df['health_score'].apply(compute_severity)
    feature_df['priority'] = feature_df['health_score'].apply(compute_priority)
    
    feature_df['predicted_failure_days'] = feature_df.apply(
        lambda r: compute_failure_days(r['health_score'], r['anomaly_detected'], r['stress_factor']),
        axis=1
    )
    
    feature_df['due_date'] = feature_df.apply(
        lambda r: compute_due_date(r['timestamp'], r['health_score']),
        axis=1
    )
    
    feature_df['completed'] = feature_df['health_score'] >= 85
    feature_df['owner'] = feature_df['completed'].apply(assign_owner)
    
    print("\n[6/8] Computing sensor-specific columns...")
    feature_df['sensor_value'] = feature_df['latest'].round(1)
    feature_df['vibration_rms'] = feature_df.apply(
        lambda r: round(r['rms'], 1) if r['sensor_type'] == 'Vibration' else 0.0,
        axis=1
    )
    feature_df['temperature_celsius'] = feature_df.apply(
        lambda r: round(r['latest'], 0) if r['sensor_type'] == 'Temperature' else 0.0,
        axis=1
    )
    feature_df['pressure_bar'] = feature_df.apply(
        lambda r: round(r['latest'], 1) if r['sensor_type'] == 'Pressure' else 0.0,
        axis=1
    )
    feature_df['power_kw'] = feature_df.apply(
        lambda r: round(r['latest'], 0) if r['sensor_type'] == 'Power' else 0.0,
        axis=1
    )
    feature_df['speed_rpm'] = feature_df.apply(
        lambda r: int(np.random.randint(800, 1800)) if r['component'] in ['Bearing', 'Motor', 'Gearbox'] else 0,
        axis=1
    )
    feature_df['wear_percentage'] = feature_df.apply(
        lambda r: round(r['latest'], 0) if r['sensor_type'] in ['Wear', 'Speed'] else 0.0,
        axis=1
    )
    
    print("\n[7/8] Formatting output to match schema...")
    output_cols = [
        'plant_id', 'sub_plant', 'equipment', 'component', 'sensor_type', 'timestamp',
        'sensor_value', 'health_score', 'status', 'maintenance_type', 'action_required',
        'severity', 'due_date', 'priority', 'ml_failure_risk', 'predicted_failure_days',
        'anomaly_detected', 'vibration_rms', 'temperature_celsius', 'pressure_bar',
        'power_kw', 'speed_rpm', 'wear_percentage', 'owner', 'completed'
    ]
    
    output_df = feature_df[output_cols].copy()
    output_df['timestamp'] = output_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    output_df['due_date'] = output_df['due_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    print("\n[8/8] Exporting to CSV...")
    output_file = 'mining_data.csv'
    output_df.to_csv(output_file, index=False)
    print(f"      ✓ Exported to: {output_file}")
    
    print("\n" + "="*80)
    print("PIPELINE SUMMARY")
    print("="*80)
    print(f"Total Records:              {len(output_df)}")
    print(f"Plants:                     {output_df['plant_id'].nunique()}")
    print(f"Sub-Plants:                 {output_df['sub_plant'].nunique()}")
    print(f"Equipment:                  {output_df['equipment'].nunique()}")
    print(f"Components:                 {output_df['component'].nunique()}")
    print(f"Sensor Types:               {output_df['sensor_type'].nunique()}")
    print(f"\nHealth Score Range:         {output_df['health_score'].min()} - {output_df['health_score'].max()}")
    print(f"Average Health Score:       {output_df['health_score'].mean():.1f}")
    print(f"\nStatus Distribution:")
    for status, count in output_df['status'].value_counts().items():
        print(f"  {status:15s}: {count:4d}")
    print(f"\nMaintenance Type:")
    for mtype, count in output_df['maintenance_type'].value_counts().items():
        print(f"  {mtype:15s}: {count:4d}")
    print(f"\nRisk Levels:")
    for risk, count in output_df['ml_failure_risk'].value_counts().items():
        print(f"  {risk:20s}: {count:4d}")
    print(f"\nAnomalies Detected:         {output_df['anomaly_detected'].sum()}")
    print(f"Completed Tasks:            {output_df['completed'].sum()}")
    print(f"Open Tasks:                 {(~output_df['completed']).sum()}")
    print("\n" + "="*80)
    print("✓ ML PIPELINE COMPLETE")
    print("✓ Output CSV ready for dashboard integration")
    print("="*80)
    
    return output_df

if __name__ == "__main__":
    df_final = main_pipeline()