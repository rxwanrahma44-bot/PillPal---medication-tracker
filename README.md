# 💊 PillPal: Digital Medication Tracker
**Project 1 | Data Science Course, DSB-4** , **Made By: Rawan Rahma**


PillPal is a simple web app built with **Streamlit** that helps a person keep track of their medications: what to take today, how many pills are left, and which ones are about to expire.

*It is for demonstration purposes only. Please consult a doctor or pharmacist for professional guidance.*


## Links 
- **Video Demo:** https://youtu.be/TH1vO8sZ-Ws?si=LKl1hdO9ytIheW1h
- **Live App:** https://pillpal---medication-tracker-uqebkkvosa7hjcrgzsve3k.streamlit.app/


## Problem Statement 
Managing multiple medications can quickly become confusing. Keeping track of how many pills to take, schedules, quantities and expiry dates is not always easy. 
PillPal makes medication management simpler by bringing together everything in one place to help users stay organized.


## Features

- **Daily Schedule:** a table of every dose to take today, sorted by time. 

- **Add Medication:** a form that saves the name, active ingredients, pills per dose, scheduled times, instructions, urgency level, category, pills in the bottle, refill threshold, and expiry date.

- **Interaction Check:** type an active ingredient and PillPal warns you if more than one of your medications contains it.

- **Inventory:** a table of all medications, with a filter by category (Prescription, OTC, Supplement).

- **Refill Request (Phase 2):** a warning appears when the pills left are at or below the refill threshold.

- **Expiry Alerts (Phase 3, my own feature):** PillPal checks every expiry date. A yellow warning shows when a medication expires within 30 days, and a red message shows when it has already expired.

- **CSV Upload / Edit / Download:** upload a starting CSV, add medications in the app, then download your updated list.


## How to use PillPal

1. Open **Inventory**, upload a CSV of your medications and click **load file**.
2. Add new medications in **Add Medication** . Type scheduled times like '08:00, 20:00'.
3. See today's doses in **Daily Schedule**
4. Use **Interaction Check** to look for ingredients that are shared between medications.
5. Check **Inventory** for refill and expiry warnings.
6. click **Download CSV** to save your list before you close the app.




## **How it works**

- 'pillpal.py ' is the Streamlit screen: pages, buttons, tables, and messages.

- 'myutils.py' holds the logic functions:
   - 'find_meds_with_ingredient' finds medications that contain an ingredient
   - 'get_low_stock_names' finds medications at are below their refill threshold.
   - 'days_until_expiry' counts the days until a medication expires 

- Data is kept in 'st.session\_state' while the app is running, and saved with 'st.download\_button'.

- Error handling: 'try/except' for bad or invalid CSV files, input validation for an empty medication name, and safe handling of blank cells and invalid dates.


## How to run it

- Install the libraries: pip install pandas, pip install streamlit

- Start the app: streamlit run pillpal.py ( keep file location in consideration )

- Go to Inventory and upload Medications.csv to try it with sample data.


## Files

1. pillpal.py: Main Streamlit app

2. myutils.py: Helper functions (logic file)

3. Medications.csv: medication data for testing



## **Streamlit features used**



\[ st.set\_page\_config, st.title, st.caption, st.sidebar, st.radio, st.columns, st.text\_input, st.number\_input, st.selectbox, st.date\_input, st.button, st.dataframe, st.file\_uploader, st.download\_button, st.session\_state, st.success, st.warning, st.error, st.info. ] 





## **Documentation:** 
https://docs.streamlit.io



