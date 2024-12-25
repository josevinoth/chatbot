import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

@csrf_exempt  # This allows POST requests without CSRF token (useful for testing)
def text_command(request):
    if request.method == "POST":
        # Get the text command from the form
        command = request.POST.get("command", "")
        if not command:
            return HttpResponse("No text command provided.")

        # Check for "Total Energy Consumption" command
        if command.lower() == "total energy consumption":
            try:
                # Read the Excel file
                df = pd.read_excel(r'C:\Users\BVM\Documents\Jose_Personal\R2S\Phygitalz\Chatbot\database.xlsx')

                # Calculate the total energy consumed by summing the 'EnergyConsumed' column
                total_energy_consumed = df['EnergyConsumed'].sum()

                # Prepare the response message
                response = f"Total Energy Consumption: {total_energy_consumed} Units"

            except Exception as e:
                response = f"Error processing the Excel file: {str(e)}"

        # Check for "Poorly performing machines" command
        elif "poorly performing machines" in command.lower():
            try:
                # Read the Excel file
                df = pd.read_excel(r'C:\Users\BVM\Documents\Jose_Personal\R2S\Phygitalz\Chatbot\database.xlsx',sheet_name='Machines')

                # Filter poorly performing machines (e.g., PerformanceScore < 60)
                poorly_performing_machines = df[df['PerformanceScore'] < 60]

                # Prepare the response message with HTML table
                if not poorly_performing_machines.empty:
                    response = """
                        <h3>Poorly Performing Machines</h3>
                        <table class="table table-striped" style="text-align: center; width: 80%; margin: 0 auto; border-collapse: collapse;">
                            <thead style="background-color: #007BFF; color: white;">
                                <tr>
                                    <th>MachineID</th>
                                    <th>MachineName</th>
                                    <th>PerformanceScore</th>
                                </tr>
                            </thead>
                            <tbody>
                    """
                    # Loop through the rows and add them to the table
                    for index, row in poorly_performing_machines.iterrows():
                        response += f"""
                            <tr>
                                <td>{row['MachineID']}</td>
                                <td>{row['MachineName']}</td>
                                <td>{row['PerformanceScore']}</td>
                            </tr>
                        """
                    response += """
                            </tbody>
                        </table>
                    """
                else:
                    response = "No poorly performing machines found."

            except Exception as e:
                response = f"Error processing the Excel file: {str(e)}"

        # Check for "Machines with high cycle time" command
        elif "high cycle time" in command.lower():
            try:
                # Read the Excel file
                df = pd.read_excel(r'C:\Users\BVM\Documents\Jose_Personal\R2S\Phygitalz\Chatbot\database.xlsx', sheet_name='Machines')

                # Filter machines with cycle time greater than 40 minutes
                high_cycle_time_machines = df[df['CycleTime'] > 40]

                # Prepare the response message with HTML table
                if not high_cycle_time_machines.empty:
                    response = """
                        <h3>Machines with High Cycle Time</h3>
                        <table class="table table-striped" style="text-align: center; width: 80%; margin: 0 auto; border-collapse: collapse;">
                            <thead style="background-color: #007BFF; color: white;">
                                <tr>
                                    <th>MachineID</th>
                                    <th>MachineName</th>
                                    <th>CycleTime</th>
                                </tr>
                            </thead>
                            <tbody>
                    """
                    # Loop through the rows and add them to the table
                    for index, row in high_cycle_time_machines.iterrows():
                        response += f"""
                            <tr>
                                <td>{row['MachineID']}</td>
                                <td>{row['MachineName']}</td>
                                <td>{row['CycleTime']}</td>
                            </tr>
                        """
                    response += """
                            </tbody>
                        </table>
                    """
                else:
                    response = "No machines with high cycle time found."

            except Exception as e:
                response = f"Error processing the Excel file: {str(e)}"

        # Check for "Machines with Downtime > 10 mins after 10 AM" command
        elif "higher downtime after 10 am" in command.lower():
            try:
                # Read the Excel file
                df = pd.read_excel(r'C:\Users\BVM\Documents\Jose_Personal\R2S\Phygitalz\Chatbot\database.xlsx')

                # Parse the 'DowntimeStart' column as datetime
                df['DowntimeStart'] = pd.to_datetime(df['DowntimeStart'], errors='coerce')

                # Ensure that 'DowntimeStart' is after 10:00 AM and downtime is greater than 10 minutes
                threshold_time = datetime.combine(datetime.today(), datetime.min.time()) + pd.Timedelta(hours=10)

                # Filter machines with downtime greater than 10 minutes and DowntimeStart after 10 AM
                machines_with_downtime_after_10am = df[(df['DowntimeStart'] >= threshold_time) & (df['Downtime (mins)'] > 10)]

                # Prepare the response message with HTML table
                if not machines_with_downtime_after_10am.empty:
                    response = """
                        <h3>Machines with Downtime > 10 Minutes After 10 AM</h3>
                        <table class="table table-striped" style="text-align: center; width: 80%; margin: 0 auto; border-collapse: collapse;">
                            <thead style="background-color: #007BFF; color: white;">
                                <tr>
                                    <th>MachineID</th>
                                    <th>MachineName</th>
                                    <th>DowntimeStart</th>
                                    <th>Downtime (mins)</th>
                                </tr>
                            </thead>
                            <tbody>
                    """
                    # Loop through the rows and add them to the table
                    for index, row in machines_with_downtime_after_10am.iterrows():
                        response += f"""
                            <tr>
                                <td>{row['MachineID']}</td>
                                <td>{row['MachineName']}</td>
                                <td>{row['DowntimeStart']}</td>
                                <td>{row['Downtime (mins)']}</td>
                            </tr>
                        """
                    response += """
                            </tbody>
                        </table>
                    """
                else:
                    response = "No machines with downtime greater than 10 minutes after 10 AM found."

            except Exception as e:
                response = f"Error processing the Excel file: {str(e)}"

        # Check for "Parts with High Rejection" command
        elif "parts with high rejection" in command.lower():
            try:
                print('Inside Try Command')
                # Read the Excel file
                df = pd.read_excel(r'C:\Users\BVM\Documents\Jose_Personal\R2S\Phygitalz\Chatbot\database.xlsx', sheet_name='Parts')

                print("Columns in Excel:", df.columns)

                # Ensure 'RejectionRate' is numeric
                df['RejectionRate'] = pd.to_numeric(df['RejectionRate'], errors='coerce')

                # Filter parts with rejection rate greater than 10%
                high_rejection_parts = df[df['RejectionRate'] > 2]
                print('high_rejection_parts',high_rejection_parts)
                # Prepare the response message with HTML table
                if not high_rejection_parts.empty:
                    response = """
                        <h3>Parts with High Rejection</h3>
                        <table class="table table-striped" style="text-align: center; width: 80%; margin: 0 auto; border-collapse: collapse;">
                            <thead style="background-color: #007BFF; color: white;">
                                <tr>
                                    <th>PartID</th>
                                    <th>PartName</th>
                                    <th>RejectionRate</th>
                                    <th>MachineID</th>
                                </tr>
                            </thead>
                            <tbody>
                    """
                    # Loop through the rows and add them to the table
                    for index, row in high_rejection_parts.iterrows():
                        response += f"""
                            <tr>
                                <td>{row['PartID']}</td>
                                <td>{row['PartName']}</td>
                                <td>{row['RejectionRate']}</td>
                                <td>{row['MachineID']}</td>
                            </tr>
                        """
                    response += """
                            </tbody>
                        </table>
                    """
                else:
                    response = "No parts with high rejection found."

            except Exception as e:
                response = f"Error processing the Excel file: {str(e)}"

        else:
            # If the command doesn't match, return the command back
            response = f"Received and processed text command: {command}"

        return HttpResponse(response)

    # If GET request, render the form to input text
    return render(request, "aip_app/text_command.html")
