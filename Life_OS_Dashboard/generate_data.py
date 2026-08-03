import pandas as pd
import random
from datetime import datetime, timedelta

def generate_data():
    apps = [
        ("TikTok", "Social Media"),
        ("Instagram", "Social Media"),
        ("Twitter", "Social Media"),
        ("YouTube", "Entertainment"),
        ("Netflix", "Entertainment"),
        ("VS Code", "Coding"),
        ("Stack Overflow", "Coding"),
        ("Duolingo", "Education"),
        ("Coursera", "Education")
    ]
    
    start_date = datetime.now().date() - timedelta(days=14)
    data = []
    
    for i in range(14):
        current_date = start_date + timedelta(days=i)
        
        # Simulate weekend vs weekday
        is_weekend = current_date.weekday() >= 5
        
        for app, category in apps:
            # Generate realistic usage times
            if category == "Coding" and not is_weekend:
                minutes = random.randint(60, 240) # Work days
            elif category == "Coding" and is_weekend:
                minutes = random.randint(0, 60)
            elif category == "Social Media":
                minutes = random.randint(20, 180) # Doomscrolling
            elif category == "Entertainment":
                minutes = random.randint(30, 150)
            elif category == "Education":
                minutes = random.randint(0, 60)
            else:
                minutes = random.randint(0, 30)
                
            data.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "App_Name": app,
                "Category": category,
                "Minutes_Used": minutes
            })
            
    df = pd.DataFrame(data)
    df.to_csv("screentime.csv", index=False)
    print("Successfully generated screentime.csv")

if __name__ == "__main__":
    generate_data()
