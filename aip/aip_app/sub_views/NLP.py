from django.shortcuts import render
import spacy
import pandas as pd
from datetime import datetime

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    nlp = None  # Ensure the application doesn't crash if the model fails to load

# File path for the Excel data
file_location = r'C:\Users\BVM\Documents\Jose_Personal\R2S\Phygitalz\Chatbot\database.xlsx'

def load_data():
    """Load the Excel data from all sheets."""
    try:
        # Load data from individual sheets
        machines_df = pd.read_excel(file_location, sheet_name='Machines')
        parts_df = pd.read_excel(file_location, sheet_name='Parts')
        energy_df = pd.read_excel(file_location, sheet_name='Energy_Consumption')
        cells_df = pd.read_excel(file_location, sheet_name='Cells')
        maintenance_df = pd.read_excel(file_location, sheet_name='Maintenance')

        # Merge energy data with machines
        machines_df = pd.merge(machines_df, energy_df, on='MachineID', how='left')

        return machines_df, parts_df, cells_df, maintenance_df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None, None


def nlp_query_processor(command, machines_df, parts_df):
    """Process the user command and return the formatted HTML table."""
    if not nlp:
        return "NLP model not loaded. Please check the server setup."

    if machines_df is None or parts_df is None:
        return "Error loading data. Please ensure the files are accessible."

    # Define keywords for intents
    intents = {
        "poorly performing machines": ["poorly performing machines", "low performance", "bad machines",
                                       "inefficient machines"],
        "high cycle time": ["high cycle time", "long cycle", "slow machines"],
        "downtime after 10 am": ["downtime after 10 am", "issues after 10 am", "delays after 10 am"],
        "high rejection": ["high rejection", "faulty parts", "bad parts", "high scrap"],
        "high energy consumption": ["high energy", "energy consumption", "power usage high",
                                    "machines using too much energy"]
    }

    try:
        command_lower = command.lower()

        # Match intents using expanded keywords
        if any(keyword in command_lower for keyword in intents["poorly performing machines"]):
            result = machines_df[machines_df['PerformanceScore'] < 60]
            return format_table(result, ["MachineID", "MachineName", "PerformanceScore"])

        if any(keyword in command_lower for keyword in intents["high cycle time"]):
            result = machines_df[machines_df['CycleTime'] > 40]
            return format_table(result, ["MachineID", "MachineName", "CycleTime"])

        if any(keyword in command_lower for keyword in intents["downtime after 10 am"]):
            threshold_time = datetime.combine(datetime.today(), datetime.min.time()) + pd.Timedelta(hours=10)
            machines_df['DowntimeStart'] = pd.to_datetime(machines_df['DowntimeStart'], errors='coerce')
            result = machines_df[
                (machines_df['DowntimeStart'] >= threshold_time) & (machines_df['Downtime (mins)'] > 10)]
            return format_table(result, ["MachineID", "MachineName", "DowntimeStart", "Downtime (mins)"])

        if any(keyword in command_lower for keyword in intents["high rejection"]):
            result = parts_df[parts_df['RejectionRate'] > 10]
            return format_table(result, ["PartID", "PartName", "RejectionRate", "MachineID"])

        if any(keyword in command_lower for keyword in intents["high energy consumption"]):
            result = machines_df[machines_df['EnergyConsumption'] > 1000]  # Example threshold for high energy
            return format_table(result, ["MachineID", "MachineName", "EnergyConsumption"])

        # Fallback for unrecognized commands
        return "Command not recognized. Please try again with a relevant query."
    except Exception as e:
        return f"Error processing the query: {str(e)}"


def format_table(dataframe, columns):
    """Format the result as an HTML table."""
    if dataframe.empty:
        return "No data found for the query."

    html = '<table border="1" style="width:100%;text-align:center;">'
    html += "<thead><tr>"
    for col in columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"

    for _, row in dataframe.iterrows():
        html += "<tr>"
        for col in columns:
            html += f"<td>{row[col]}</td>"
        html += "</tr>"

    html += "</tbody></table>"
    return html


# Django view for NLP query
def nlp_view(request):
    """Render the NLP query page."""
    output = ""
    if request.method == "POST":
        command = request.POST.get("command")
        if command:
            machines_df, parts_df, cells_df, maintenance_df = load_data()
            output = nlp_query_processor(command, machines_df, parts_df)
        else:
            output = "Please enter a valid command."

    return render(request, "aip_app/nlp_view.html", {"output": output})
