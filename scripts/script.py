## A function to convert dates to a given format after adding one day to the input date.
def convert_date(input_date):
    from datetime import datetime, timedelta
    
    # Parse the input date string to a datetime object
    date_object = datetime.strptime(input_date, "%Y-%m-%d")
    
    # Add one day to the date
    new_date_object = date_object + timedelta(days=1)
    
    # Convert the new date back to a string in the desired format
    new_date_string = new_date_object.strftime("%Y-%m-%d")
    
    return new_date_string