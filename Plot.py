from Nepse_Scrapper import connect_table
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def get_data(script):
    db = connect_table("nepse")
    if db is None:
        return None
    
    cursor = db.cursor()
    # Step 1: Check if ticker exists
    check_query = "SELECT COUNT(*) FROM company WHERE ticker = %s"
    cursor.execute(check_query, (script,))
    count = cursor.fetchone()[0]

    if count == 0:
        print(f"Stock '{script}' not found in the database.")
        cursor.close()
        db.close()
        return None
    
    seven_days_ago = (datetime.now() - timedelta(days=7)).date()
    query = "SELECT ltp, updated_on FROM company WHERE ticker = %s AND updated_on >= %s ORDER BY updated_on ASC"
    cursor.execute(query, (script,seven_days_ago))
    result = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    # Convert to DataFrame for further use or plotting
    df = pd.DataFrame(result, columns=["ltp","updated_on"])
    df['updated_on'] = pd.to_datetime(df['updated_on'], format='%Y-%m-%d')
    df=df.sort_values("updated_on")
    return df

script=input("Enter the script name: ").upper()
if not script:
    print("No script name provided.")
    exit()
data = get_data(script)
if data is not None:
    plt.figure(figsize=(10, 5))
    plt.plot(data["updated_on"], data["ltp"], marker='o', linestyle='-')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.title("LTP vs Updated On for " + script)
    plt.xlabel("Updated On")
    plt.ylabel("LTP")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
