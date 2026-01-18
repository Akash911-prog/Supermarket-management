from db import DB
from matplotlib.dates import AutoDateLocator, DateFormatter
import matplotlib.pyplot as plt

def sales_report_main():
    """
    Generates a sales report graph over time.

    Returns:
        List of tuples containing the date and total sales for each day.
    """
    db = DB()
    sales = db.get_daily_sales()
    db.close()
    
    dates = [row[0] for row in sales]  # Keep as datetime objects
    totals = [float(row[1]) for row in sales]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot the total sales over time
    ax.plot(dates, totals)
    
    # Set labels and title
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Sales")
    ax.set_title("Daily Sales Over Time")
    
    # Format the x-axis to display dates in a readable format
    ax.xaxis.set_major_locator(AutoDateLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%d-%m-%Y"))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Ensure the graph fits within the figure
    plt.tight_layout()
    
    # Display the graph
    plt.show()
    return sales

if __name__ == "__main__":
    sales = sales_report_main()
    print(sales)




