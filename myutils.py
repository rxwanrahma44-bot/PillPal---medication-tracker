"""Requirement: helper functions for PillPal. 
this is the logic containing functions and streamlit screen lives in pillpal.py"""

#importing libraries
import datetime 
import pandas as pd 


#used on interaction check page.
#it looks through every medication and returns a list of names of the ones that contain the ingredient the user typed 
def find_meds_with_ingredient (meds,ingredient):
    matches = [] #returns a list of medications that include the given active ingredients
    ingredient = ingredient.lower()
    for i in range (len(meds)): 
        if ingredient in str(meds.loc[i,"active_ingredients"]).lower():  #str to not cause a crash when theres an empty cell
            matches.append(meds.loc[i, "med_name"])

    return matches



#used on inventory page for my phase 3 of the project requirement.
#returns how many days are left until a medication expires
#if date is blank, try/except make it return None instead of crashing
def days_until_expiry(expiry_value):
    try:
        expiry = pd.to_datetime(expiry_value).date()  #will return no. of days until expiry date, or none if date is invalid
        return (expiry - datetime.date.today()).days

    except Exception:
        return None #for blank or invalid date



#used on inventory page for refill warning
#returns names of medications whose pills are at or below their refill threshold
#rows with blank numbers are skipped 
def get_low_stock_names(meds):

    low = []
    for i in range (len(meds)):
        pills = meds.loc[i, "pills_remaining"]
        threshold = meds.loc[i, "refill_threshold"] #skips blank cells - only compares real numbers
        if pills != "" and threshold != "" :
            if pills <= threshold :
                low.append(meds.loc[i, "med_name"])
    return low