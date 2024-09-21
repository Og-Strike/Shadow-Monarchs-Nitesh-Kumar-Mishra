import pandas as pd
import matplotlib.pyplot as plt

# Create the dataset
data = {
    "Date": ["2024-09-18", "2024-09-19", "2024-09-20", "2024-09-21"],
    "Total Bill": [150, 75, 200, 300],
    "Store Name": ["GroceryMart", "CoffeeShop", "Electronics", "SuperStore"]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame as a CSV file
csv_file_path = r'C:\Users\redil\Downloads\BillWizard\BillWizard\daily_expenditure.csv'
df.to_csv(csv_file_path, index=False)

# Bar graph: Date vs. Total Bill
plt.figure(figsize=(8, 5))
plt.bar(df['Date'], df['Total Bill'], color='blue')
plt.title('Daily Expenditures')
plt.xlabel('Date')
plt.ylabel('Total Bill')
plt.xticks(rotation=45)
plt.tight_layout()
bar_graph_path = r'C:\Users\redil\Downloads\BillWizard\BillWizard\bar_graph.png'
plt.savefig(bar_graph_path)
plt.show()

# Pie chart: Distribution of spending by store
plt.figure(figsize=(7, 7))
plt.pie(df['Total Bill'], labels=df['Store Name'], autopct='%1.1f%%', startangle=140)
plt.title('Spending Distribution by Store')
pie_chart_path = r'C:\Users\redil\Downloads\BillWizard\BillWizard\pie_chart.png'
plt.savefig(pie_chart_path)
plt.show()

# Line plot: Date vs. Total Bill
plt.figure(figsize=(8, 5))
plt.plot(df['Date'], df['Total Bill'], marker='o', color='green', linestyle='-', markersize=8)
plt.title('Total Bill vs. Date')
plt.xlabel('Date')
plt.ylabel('Total Bill')
plt.xticks(rotation=45)
plt.tight_layout()
line_plot_path = r'C:\Users\redil\Downloads\BillWizard\BillWizard\plot_graph.png'
plt.savefig(line_plot_path)
plt.show()
