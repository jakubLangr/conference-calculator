import streamlit as st
import pandas as pd
import numpy as np
import base64
import io

# Function to export dataframe to excel
def export_excel(df):
    towrite = io.BytesIO()
    downloaded_file = df.to_excel(towrite, encoding='utf-8', index=False, header=True)
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="financials.xlsx">Download Excel File</a>'
    return href

# Streamlit app
st.title("Tech Conference Financial Calculator")

# Inputs
ticket_price = st.number_input("Ticket Price", value=100)
num_attendees = st.number_input("# of Attendees", value=100)
marketing_spend_per_ticket = st.number_input("Marketing Spend per Ticket", value=10)
num_speakers = st.number_input("# of Speakers", value=5)
num_business_class_speakers = st.number_input("# of Business Class Speakers", value=2)
num_local_speakers = st.number_input("# of Local Speakers", value=1)
flight_ticket_economy = st.number_input("Flight Ticket Price (Economy)", value=500)
flight_ticket_business = st.number_input("Flight Ticket Price (Business)", value=2000)
fb_spend = st.number_input("F&B Spend", value=50)
swag_spend = st.number_input("Swag Spend", value=20)
yacht_party_cost = st.number_input("Yacht After Party Cost", value=5000)
num_key_speakers = st.number_input("# of Key Speakers", value=3)
hotel_cost_per_key_speaker = st.number_input("Hotel Cost per Key Speaker", value=200)

# Calculations
total_ticket_revenue = ticket_price * num_attendees
total_marketing_spend = marketing_spend_per_ticket * num_attendees
total_flight_tickets_cost = ((num_speakers - num_business_class_speakers - num_local_speakers) * flight_ticket_economy
                             + num_business_class_speakers * flight_ticket_business)
total_fb_spend = fb_spend * num_attendees
total_swag_spend = swag_spend * num_attendees
total_yacht_party_cost = yacht_party_cost
total_hotel_costs = num_key_speakers * hotel_cost_per_key_speaker
total_costs = (total_marketing_spend + total_flight_tickets_cost + total_fb_spend
               + total_swag_spend + total_yacht_party_cost + total_hotel_costs)
profit = total_ticket_revenue - total_costs

# Dataframe
data = {'Category': ['Ticket Revenue', 'Marketing Spend', 'Flight Tickets Cost', 'F&B Spend', 'Swag Spend', 'Yacht After Party Cost', 'Hotel Costs', 'Total Costs', 'Profit'],
        'Amount': [total_ticket_revenue, total_marketing_spend, total_flight_tickets_cost, total_fb_spend, total_swag_spend, total_yacht_party_cost, total_hotel_costs, total_costs, profit]}
df = pd.DataFrame(data)

# Display dataframe
st.write(df)

# Export to excel
if st.button('Export to Excel'):
    st.markdown(export_excel(df), unsafe_allow_html=True)

# Breakeven point
breakeven_attendees = total_costs / ticket_price
st.write(f"Breakeven Point: {np.ceil(breakeven_attendees)} attendees")

# Upfront personal spend
upfront_personal_spend = total_costs - total_marketing_spend
st.write(f"Upfront Personal Spend: ${upfront_personal_spend}")