import pandas as pd
import random
from datetime import datetime, timedelta
from supabase import create_client, Client
import json

# Replace these with your actual credentials
SUPABASE_URL = 'https://eygedvepmuwllwcefimq.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV5Z2VkdmVwbXV3bGx3Y2VmaW1xIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI3MTk5NjIsImV4cCI6MjA1ODI5NTk2Mn0.RZ2-hipNcemzQALtTzyJ8oVujza9Ua5s1-0Q8yaoKpc'

# Initialize Supabase client
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Connected to Supabase successfully")
    
    # Fetch data from the existing table
    response = supabase.table('user_interactions').select('*').execute()
    data = response.data
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    
    # Ensure the DataFrame has the necessary columns
    required_columns = ["id", "user_id", "product_id", "page_url", "interaction_type", "visit_count", "last_visited", "created_at"]
    if not all(column in df.columns for column in required_columns):
        raise ValueError("The fetched data does not contain all required columns.")
    
    # Calculate interaction score
    max_time_spent = 10  # Assume max possible time spent
    max_pages_viewed = 10  # Assume max possible pages viewed
    alpha, beta, gamma = 0.4, 0.4, 0.2  # Weight factors

    def calculate_interaction_score(visit_count, last_visited):
        # Parse the timestamp with the correct format
        try:
            dt = datetime.strptime(last_visited, "%Y-%m-%dT%H:%M:%S.%f%z")
        except ValueError:
            # Fallback to handle timestamps without milliseconds or timezone
            dt = datetime.strptime(last_visited, "%Y-%m-%dT%H:%M:%S%z")
        
        # Calculate days since last visited
        days_since_last = (datetime.now(dt.tzinfo) - dt).days
        
        # Calculate interaction score
        return round(alpha * (visit_count / max_time_spent) + beta * (visit_count / max_pages_viewed) + gamma * (1 / (1 + days_since_last)), 2)


    df["interaction_score"] = df.apply(lambda row: calculate_interaction_score(row["visit_count"], row["last_visited"]), axis=1)

    # Generate notifications
    notification_types = ["Email", "SMS", "Push"]

    def generate_notification(row):
        # Parse the timestamp with the correct format using the same approach as calculate_interaction_score
        try:
            dt = datetime.strptime(row["last_visited"], "%Y-%m-%dT%H:%M:%S.%f%z")
        except ValueError:
            # Fallback to handle timestamps without milliseconds or timezone
            try:
                dt = datetime.strptime(row["last_visited"], "%Y-%m-%dT%H:%M:%S%z")
            except ValueError:
                # Additional fallback if needed
                dt = datetime.fromisoformat(row["last_visited"].replace('Z', '+00:00'))
        
        # Calculate days since last visited
        days_since_last = (datetime.now(dt.tzinfo) - dt).days
        
        if row["interaction_score"] < 0.5 and days_since_last > 3:
            notif_type = random.choice(notification_types)
            message = f"Hey User {row['user_id']}! We noticed you haven't visited in a while. Check out our latest offers!"
            return pd.Series([notif_type, message])
        return pd.Series([None, None])

    df[["notification_type", "message"]] = df.apply(generate_notification, axis=1)

    # Check if the new table exists, if not, create it
    
        # Try to query the new table
    response = supabase.table('new_table1').select('*').limit(1).execute()
    print("New table exists, proceeding with insert operation")
        
    
    # Insert the processed data into the new table
    try:
        # First, get the table structure to check available columns
        response = supabase.rpc('get_columns', {'table_name': 'new_table1'}).execute()
        print("Checking table structure...")
        
        # If the above RPC fails, we'll use a different approach
        existing_columns = [col['column_name'] for col in response.data]
        print(f"Available columns in table: {existing_columns}")
        
    except Exception as e:
        print(f"Couldn't verify columns: {e}")
        print("Will attempt to insert data with fallback approach")
        
        # We'll try inserting data with a more defensive approach
        # First get a single row to examine its structure
        response = supabase.table('new_table1').select('*').limit(1).execute()
        if response.data:
            existing_columns = response.data[0].keys()
            print(f"Available columns from query: {existing_columns}")
        else:
            print("Table exists but no sample data to determine columns, will try inserting without created_at")
            existing_columns = ['id', 'user_id', 'product_id', 'page_url', 'interaction_type', 
                               'visit_count', 'last_visited', 'interaction_score', 
                               'notification_type', 'message']

    # Insert the processed data into the new table
    for index, row in df.iterrows():
        # Create a filtered data dictionary with only columns that exist
        data = {}
        for column in existing_columns:
            if column in row:
                data[column] = row[column]
        
        try:
            response = supabase.table('new_table1').insert(data).execute()
            print(f"Inserted row {index + 1} of {len(df)}")
        except Exception as insert_error:
            print(f"Error inserting row {index + 1}: {insert_error}")
            # Try without problematic fields
            if 'created_at' in data:
                del data['created_at']
                try:
                    response = supabase.table('new_table1').insert(data).execute()
                    print(f"Inserted row {index + 1} without created_at field")
                except Exception as retry_error:
                    print(f"Failed to insert even without created_at: {retry_error}")
    
    print("Data inserted successfully into the new table")
    
except Exception as e:
    print(f"Error: {e}")