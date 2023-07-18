import random
import pandas as pd
import datetime
import holidays


MIN_UNITS_PROCESSED = 100
MAX_UNITS_PROCESSED = 300

PERCENTAGE_OF_ALLOWED_DEFECTS = 0.1

EFFICIENCY_FACTOR_MIN = 0.8
EFFICIENCY_FACTOR_MAX = 1.0

def get_business_days(leave_days=None):
    if leave_days is None:
        leave_days = []
    now = datetime.datetime.now()
    pt_holidays = holidays.country_holidays('PT')
    business_days = 0
    for i in range(1, 32):
        try:
            this_date = datetime.date(now.year, now.month, i)
        except ValueError:
            break
        # Monday == 0, Sunday == 6
        if this_date.weekday() < 5 and this_date not in pt_holidays and this_date.day not in leave_days:
            business_days += 1

    return business_days


# units per hour
def get_productivity(units_processed, number_of_defects, total_labor_hours, efficiency_factor):
    return (units_processed - number_of_defects) / (total_labor_hours * efficiency_factor)

# time per unit (hours)
def get_unit_processing_time(units_processed, number_of_defects, total_labor_hours, efficiency_factor):
    return (total_labor_hours * efficiency_factor) / (units_processed - number_of_defects)

def generate_dataset(number_of_employees):

    data = {'units_processed': [],
            'number_of_defects': [],
            'total_labor_hours': [],
            'efficiency_factor': [],
            # 'quality_factor': [],    # for debug purposes
            'unit_processing_time': [],
            # 'productivity': []      # for debug purposes
            }
    
    index = []

    for i in range(number_of_employees):
        # Variables
        index.append(i)

        units_processed = random.randint(MIN_UNITS_PROCESSED, MAX_UNITS_PROCESSED)

        max_number_of_defects = int(units_processed * PERCENTAGE_OF_ALLOWED_DEFECTS)    # Round down number
        number_of_defects = random.randint(0, max_number_of_defects)
        
        leave_days = random.sample(range(1, 32), random.randint(0, 5))
        total_labor_hours = get_business_days(leave_days) * 8

        efficiency_factor = random.uniform(EFFICIENCY_FACTOR_MIN, EFFICIENCY_FACTOR_MAX)

        # quality_factor = (units_processed - number_of_defects) / units_processed


        unit_processing_time = get_unit_processing_time(units_processed, number_of_defects, total_labor_hours, efficiency_factor)

        # productivity = get_productivity(units_processed, number_of_defects, total_labor_hours, efficiency_factor)
        
        # Add to dataframe
        data['units_processed'].append(units_processed)
        data['number_of_defects'].append(number_of_defects)
        data['total_labor_hours'].append(total_labor_hours)
        data['efficiency_factor'].append(efficiency_factor)
        # data['quality_factor'].append(quality_factor)
        data['unit_processing_time'].append(unit_processing_time)
        # data['productivity'].append(productivity)

    # pd.DataFrame(data).to_csv(csv_name, index=False)
    print("Dataset generated successfully!")

    df = pd.DataFrame(data, index=index)
    df.index.name = "employee_id"

    return df
