"""PillPal: a digital medication tracker built with Streamlit.

Pages: Daily Schedule, Add Medication, Interaction Check, Inventory.
Data is kept in st.session_state and can be uploaded or downloaded as a CSV.

"""


#1: IMPORTS 

import streamlit as st
import pandas as pd
import datetime
import myutils #my logic file


#2: PAGE SETTINGS 

st.set_page_config(  #comes from the streamlit docs
    page_title="PillPal: Medication Tracker",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)


#includes a title and a caption at the top of every page
st.title("💊 PillPal")
st.caption("For demonstration purposes only. Please consult a doctor or pharmacist for professional guidance.")



#3: SIDEBAR MENU:
#user picks a page, its saved in page_chosen

with st.sidebar:
    page_chosen = st.radio(
        "MENU",
        ("Daily Schedule", "Add Medication", "Interaction Check", "Inventory")
    )


#4: SETTING UP OUR DATA: 
#these are the columns that will be added to our medication table

MED_COLUMNS = [
    "med_id", "med_name", "active_ingredients", "dosage",
    "scheduled_times", "instructions", "urgency_level",
    "category", "pills_remaining", "refill_threshold", "expiry_date",
]



#this step creates an empty table when the app opens
#st.session_state keeps data while app is running to avoid data getting erased 

if "meds" not in st.session_state:
    st.session_state.meds = pd.DataFrame(columns=MED_COLUMNS)


#5: DAILY SCHEDULE PAGE 

if page_chosen == "Daily Schedule":
    st.header("Daily Schedule", divider="orange")

    
    meds = st.session_state.meds #to get the saved meds
    

    if len(meds) == 0:
        st.info("No medications yet. Add one from the menu!") #shows a message if there are no medications yet 
    else: 
        rows = [] #an empty list that will hold one row per med

        for i in range(len(meds)): #a loop to go through each med
            times = meds.loc[i, "scheduled_times"].split(",") #splitting times into a list
           
            for t in times:
                if t.strip() != "" : #to skip empty times
                    #adds a row for each time- strip() to remove extra spaces
                    rows.append([t.strip(), meds.loc[i, "med_name"],
                                 meds.loc[i, "dosage"], meds.loc[i, "instructions"]])


        #turns the list into a table and sorts it with earliest first
        schedule = pd.DataFrame(rows, columns=["Time", "Medication", "Pills", "Instructions"])
        schedule = schedule.sort_values("Time")


        #shows the table. hide_index to hide the row numbers
        st.dataframe(schedule, hide_index=True)




#6 : ADD MEDICATION PAGE       

elif page_chosen == "Add Medication":
    st.header("Add Medication", divider="orange")

    
    #st.columns splits the page to 2 side by side columns
    col1, col2 = st.columns(2)


    #left column - st.text_input, st.number_input, st.selectbox are all input boxes- from streamlit docs
    with col1:
        med_name = st.text_input("Medication Name")
        dosage = st.number_input("Pills per dose", min_value = 1, step = 1 )
        category = st.selectbox ("Category", ("Prescription" , "OTC" , "Supplement"))
        pills_remaining = st.number_input("Pills in the bottle" , min_value = 0, step = 1)


    #right column (again, with their input boxes)
    with col2:
        active_ingredients = st.text_input("Active ingredients")
        scheduled_times = st.text_input("Scheduled times")
        urgency_level = st.selectbox("Urgency level", ("High", "Medium", "Low"))
        refill_threshold = st.number_input("Warn me when pills drop to (for refill)", min_value=0, step=1)
        instructions = st.text_input ("Instructions")

        #my phase 3 feature. st.date_input allows user to pick the expiry date from calendar
        expiry_date = st.date_input("Expiry date") 
        

        if st.button("Add medication"): #when button is clicked
            if med_name == "": #name can't be empty
                st.warning("Please type a medication name.")
            else:
                #adds one row to table with the values - has to be in same order as MED_COLUMNS
                new_row = pd.DataFrame(
                [[len(st.session_state.meds) + 1, med_name, active_ingredients, dosage, scheduled_times, instructions, urgency_level, category, pills_remaining, refill_threshold, expiry_date]], columns=MED_COLUMNS
                )

                #adds new row to bottom of saved table (for each entry)
                st.session_state.meds = pd.concat(
               [st.session_state.meds, new_row], ignore_index=True)
                st.success(f"{med_name} was added!") #st.success = green success message



#7 : INTERACTION CHECK PAGE  

elif page_chosen == "Interaction Check":
    st.header("Interaction Check", divider="orange")

    
    ingredient = st.text_input("Type an active ingredient")
    ingredient = ingredient.lower()  #.lower() to ignore capital letters

    meds = st.session_state.meds  


    matches = myutils.find_meds_with_ingredient(meds, ingredient) #function from myutils

    #shows results once something has been typed
    if ingredient != "":
        if len(matches) > 1:
            #2 or more medications share same ingredient: a warning message will be shown  + meds will be listed
            st.warning("Warning: more than one of your medications contains " + ingredient)
            for name in matches:
                st.write(name) 
        elif len(matches) == 1:
            st.success("Only one of your medications contains " + ingredient)
        else:
            st.write("None of your medications contain " + ingredient)

    


#8: INVENTORY PAGE  

elif page_chosen == "Inventory":
    st.header("Inventory", divider="orange")
    

    #st.file_uploader to upload a csv file
    uploaded = st.file_uploader("Upload a medication CSV", type="csv")
    if uploaded is not None: #to stop file from reloading and erasing new medications
        if st.button("Load file"):
            try:
                data = pd.read_csv(uploaded) #reads csv into a table
                data = data.fillna("") #replaces empty cells with empty text
                st.session_state.meds = data #saves it in session_state
                st.success ("File loaded!")

            except Exception:
                st.error("Oops! Please upload a valid medication file.")

    #to filter by category using (st.selectbox)
    chosen = st.selectbox("Filter by category", ("All", "Prescription", "OTC", "Supplement"))
    meds = st.session_state.meds
    if chosen != "All":
        meds = meds[meds["category"] == chosen] #keeps oly rows where category matches the choice
    st.dataframe(meds, hide_index = True) #shows table without row numbers


    #refill warning: when pills is at or below the refill capacity
    all_meds = st.session_state.meds
    for name in myutils.get_low_stock_names(all_meds):
        st.warning(name + " is running low! Time to request a refill 💊")


    #expiry alert (my phase 3 feature)
    #date calculation in myutils.py
    
    if "expiry_date" in all_meds.columns: #only runs if table has expiry_date column
        for i in range(len(all_meds)):
            name = all_meds.loc[i, "med_name"]
            days_left = myutils.days_until_expiry(all_meds.loc[i, "expiry_date"])

            if days_left is not None: #skips meds with invalid dates
                if days_left < 0: #negative days = means it already expired
                    st.error(name + " has EXPIRED ❌ . Please do not take it.")
                
                elif days_left <= 30: #30 days or less left = yellow warning
                    st.warning("⌛" + name + " expires in " + str(days_left) + " days.") 


    #downloads table as a CSV
    csv = all_meds.to_csv(index=False)
    st.download_button("Download CSV", csv, "medications.csv", "text/csv")
    






