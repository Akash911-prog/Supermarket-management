from db import DB
import matplotlib.pyplot as plt

def sales_report_main():
    db = DB()
    sales = db.get_daily_sales()
    db.close()
    
    dates = [row[0] for row in sales]
    totals = [float(row[1]) for row in sales]

    plt.figure()
    plt.plot(dates, totals)   # No colors specified (safe default)
    plt.xlabel("Date")
    plt.ylabel("Total Sales")
    plt.title("Daily Sales Over Time")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()
    return sales


if __name__ == "__main__":
    sales = sales_report_main()
    print(sales)




