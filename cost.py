import pandas as pd
import numpy as np

# list of irish counties

counties = '''DUBLIN,	CORK,	GALWAY,	OFFALY,	WICKLOW,	TIPPERARY,	MONAGHAN,	SLIGO,	WEXFORD,	DUBLIN,	DUBLIN,	CLARE,	DONEGAL,	MEATH,	WESTMEATH,	MAYO,	LIMERICK,	KILDARE,	KERRY,	LOUTH,	LONGFORD,	DUBLIN,	GALWAY,	CARLOW,	CORK,	LEITRIM,	KILKENNY,	LAOIS,	ROSCOMMON,	CAVAN,	WATERFORD,'''

counties_list = [county.strip() for county in counties.split(',') if county.strip()]

# make service providers a global variable

service_providers = [
    "Provider A", "Provider B", "Provider C", "Provider D", "Provider E", 
    "Provider F", "Provider G", "Provider H", "Provider I", "Provider J", 
    "Provider K", "Provider L", "Provider M", "Provider N", "Provider O", 
    "Provider P", "Provider Q", "Provider R", "Provider S", "Provider T", 
    "Provider U", "Provider V", "Provider W", "Provider X", "Provider Y", 
    "Provider Z", "Provider AA", "Provider AB", "Provider AC", "Provider AD"
]



def template_cost():
    base_info = {
        "Service": "Residential Care",
        "Person_ID": "RES_001",
        "County": counties_list[0],
        "Disability_Complexity": "high",
        "Service_Provider": "Provider A"
    }
    costs = [
        ("direct", "Staffing Costs", 1300.00),
        ("direct", "Medical Supplies", 300.00),
        ("indirect", "Administrative Salaries", 500.00),
        ("indirect", "Facility Costs", 200.00),
        ("direct", "Resident-Specific Utilities", 100.00),
        ("direct", "Transportation", 150.00),
        ("direct", "Meals", 200.00),
        ("direct", "Equipment Maintenance", 80.00),
        ("direct", "Extra Activities", 60.00),
        ("indirect", "Insurance", 250.00),
        ("indirect", "Staff Training", 300.00),
        ("indirect", "Compliance and Licensing", 160.00),
        ("indirect", "Utilities", 100.00)
    ]
    rows = []
    for c_type, desc, val in costs:
        row = base_info.copy()
        row.update({
            "Cost_Type": c_type,
            "Cost_Description": desc,
            "Cost_Value": val
        })
        rows.append(row)
    return pd.DataFrame(rows)





## example collated templates



def simulate_service_costs(num_people=1000):
    counties = '''DUBLIN,	CORK,	GALWAY,	OFFALY,	WICKLOW,	TIPPERARY,	MONAGHAN,	SLIGO,	WEXFORD,	DUBLIN,	DUBLIN,	CLARE,	DONEGAL,	MEATH,	WESTMEATH,	MAYO,	LIMERICK,	KILDARE,	KERRY,	LOUTH,	LONGFORD,	DUBLIN,	GALWAY,	CARLOW,	CORK,	LEITRIM,	KILKENNY,	LAOIS,	ROSCOMMON,	CAVAN,	WATERFORD,'''

    counties_list = [county.strip() for county in counties.split(',') if county.strip()]
    # Set a seed for reproducibility
    np.random.seed(42)

    # Define disability Complexity levels
    severities = ['low', 'medium', 'high']

    # Define service types
    service_types = ["Residential Care", "Day Services", "Home and Personal Support", 
                    "Respite", "Multi-disciplinary Services"]

    # Define cost parameter ranges for each service type.
    service_cost_params = {
        "Residential Care": {
            "direct": {
                "low":    (1000, 1500, ["Staffing Costs", "Medical Supplies", "Resident-Specific Utilities", "Transportation"]),
                "medium": (1500, 2000, ["Staffing Costs", "Medical Supplies", "Resident-Specific Utilities", "Transportation"]),
                "high":   (2000, 2500, ["Staffing Costs", "Medical Supplies", "Resident-Specific Utilities", "Transportation"])
            },
            "indirect": (500, 800, ["Administrative Salaries", "Facility Costs", "Utilities", "General Supplies", "Insurance"])
        },
        "Day Services": {
            "direct": {
                "low":    (500, 800, ["Staffing Costs", "Activity Materials", "Transportation"]),
                "medium": (800, 1200, ["Staffing Costs", "Activity Materials", "Transportation"]),
                "high":   (1200, 1600, ["Staffing Costs", "Activity Materials", "Transportation"])
            },
            "indirect": (300, 500, ["Administrative Salaries", "Facility Costs", "Utilities", "General Supplies"])
        },
        "Home and Personal Support": {
            "direct": {
                "low":    (300, 500, ["Caregiver Wages", "Travel Costs"]),
                "medium": (500, 700, ["Caregiver Wages", "Travel Costs"]),
                "high":   (700, 900, ["Caregiver Wages", "Travel Costs"])
            },
            "indirect": (200, 400, ["Administrative Salaries", "Training Costs", "Supervision Costs"])
        },
        "Respite": {
            "direct": {
                "low":    (400, 600, ["Caregiver Wages", "Accommodation Costs"]),
                "medium": (600, 800, ["Caregiver Wages", "Accommodation Costs"]),
                "high":   (800, 1000, ["Caregiver Wages", "Accommodation Costs"])
            },
            "indirect": (200, 300, ["Administrative Salaries", "Facility Costs"])
        },
        "Multi-disciplinary Services": {
            "direct": {
                "low":    (600, 900, ["Therapist Fees", "Assessment Costs"]),
                "medium": (900, 1200, ["Therapist Fees", "Assessment Costs"]),
                "high":   (1200, 1500, ["Therapist Fees", "Assessment Costs"])
            },
            "indirect": (300, 500, ["Administrative Salaries", "Equipment Costs"])
        }
    }

    """Simulate detailed cost data for all services."""
    records = []

    for service_name in service_types:
        params = service_cost_params[service_name]
        
        for i in range(num_people):
            county = np.random.choice(counties_list)
            Complexity = np.random.choice(severities)
            service_provider = np.random.choice(service_providers)
        
            d_low, d_high, direct_cost_types = params["direct"][Complexity]
            direct_cost = np.random.uniform(d_low, d_high)
            
            i_low, i_high, indirect_cost_types = params["indirect"]
            indirect_cost = np.random.uniform(i_low, i_high)
            
            total_cost = direct_cost + indirect_cost

            for cost_type, cost_value in zip(direct_cost_types, np.random.dirichlet(np.ones(len(direct_cost_types)), size=1)[0]):
                records.append({
                    "Service": service_name,
                    "Person_ID": f"{service_name[:3].upper()}_{i+1:03d}",
                    "County": county,
                    "Disability_Complexity": Complexity,
                    "Cost_Type": "direct",
                    "Cost_Description": cost_type,
                    "Cost_Value": round(direct_cost * cost_value, 2),
                    "Service_Provider": service_provider
                })

            for cost_type, cost_value in zip(indirect_cost_types, np.random.dirichlet(np.ones(len(indirect_cost_types)), size=1)[0]):
                records.append({
                    "Service": service_name,
                    "Person_ID": f"{service_name[:3].upper()}_{i+1:03d}",
                    "County": county,
                    "Disability_Complexity": Complexity,
                    "Cost_Type": "indirect",
                    "Cost_Description": cost_type,
                    "Cost_Value": round(indirect_cost * cost_value, 2),
                    "Service_Provider": service_provider
                })
    
    # Create a pandas DataFrame
    return pd.DataFrame(records)

## aggregate data

df = pd.read_csv('test.csv')

df.columns = ['Service', 'Person_ID', 'County', 'Disability_Complexity', 'Cost_Type',
       'Cost_Description', 'Cost_Value', 'Service_Provider']


def aggregate_cost_data(df):
    """
    Aggregates cost data by service, county, and disability complexity,
    calculating sum, average, median, min, and max of cost value for each
    unique person ID within those groups.

    Args:
        df: Pandas DataFrame with columns 'Service', 'Person_ID', 'County',
           'Disability_Complexity', 'Cost_Value'.

    Returns:
        Pandas DataFrame with aggregated cost data.
    """

    # Group by service, county, disability complexity, and person ID
    grouped = df.groupby(['Service', 'County', 'Disability_Complexity', 'Person_ID'])['Cost_Value'].sum().reset_index()

    # Aggregate at the service, county, and disability complexity level
    aggregated = grouped.groupby(['Service', 'County', 'Disability_Complexity'])['Cost_Value'].agg(
        Total_Cost = 'sum',
        Average_Cost = 'mean',
        Median_Cost = 'median',
        Min_Cost = 'min',
        Max_Cost = 'max',
        Unique_Person_Count = 'count'  # Count of unique person IDs
    ).reset_index()

    return aggregated

