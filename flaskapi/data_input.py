"""
Feature input mapping and validation for Salary Prediction API

This module helps validate and structure input features for the model.
The model expects 19 features (one-hot encoded from original data).
"""

# Feature names in order (for reference)
FEATURE_NAMES = [
    'Rating',
    'Size_M',
    'Size_S',
    'Size_XL',
    'Type of ownership_Company - Private',
    'Type of ownership_Company - Public',
    'Industry_Aerospace & Defense',
    'Industry_Agriculture',
    'Sector_Accounting',
    'Revenue_$1 to $2 billion',
    'num_comp',
    'hourly',
    'employer_provided',
    'job_state_CA',
    'job_state_NY',
    'same_state',
    'age',
    'python_yn',
    'spark',
    'aws',
    'excel',
    'job_simp_analyst',
    'job_simp_data engineer',
    'job_simp_data scientist',
    'seniority_senior'
]

# Note: The actual features may differ based on your model
# Verify the exact features by checking the training data feature names

def validate_input(feature_list):
    """
    Validate input feature list
    
    Args:
        feature_list: List of 19 feature values
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(feature_list, (list, tuple)):
        raise ValueError("Input must be a list or tuple")
    
    if len(feature_list) != 19:
        raise ValueError(f"Expected 19 features, got {len(feature_list)}")
    
    try:
        # Try converting to floats
        _ = [float(x) for x in feature_list]
    except (ValueError, TypeError):
        raise ValueError("All features must be numeric values")
    
    return True

def create_prediction_input(features_dict):
    """
    Create prediction input from dictionary format
    
    Args:
        features_dict: Dictionary with feature names and values
        
    Returns:
        list: Feature array ready for model prediction
    """
    # This is a template - adjust based on your actual features
    # Example structure - modify according to your model
    pass
