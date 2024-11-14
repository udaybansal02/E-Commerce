import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def calculate_optimal_price(cost, competitor_price, desired_profit_margin):
    try:
        cost = float(cost)
        competitor_price = float(competitor_price)
        desired_profit_margin = float(desired_profit_margin)
# formula for calculating the optimal price or selling price of a product
        optimal_price = max(cost + cost * (desired_profit_margin / 100), competitor_price)

        return optimal_price, (cost, competitor_price, optimal_price)
    except ValueError as error:
        messagebox.showerror("Error", str(error))
        return None, None

def handle_calculate_price():
    product_cost = entry_cost_var.get()
    competitor_price = entry_competitor_price_var.get()
    desired_profit_margin = entry_profit_margin_var.get()

    optimal_price, input_values = calculate_optimal_price(product_cost, competitor_price, desired_profit_margin)

    if optimal_price is not None:
        print(f"Calculated Optimal Price: {optimal_price}")
        label_optimal_price["text"] = f"Optimal Price: ₹{optimal_price:.2f}"

        data_points.append(input_values)
        update_table()
        plot_graph()
    else:
        label_optimal_price["text"] = ""

def add_data_point():
    product_cost = entry_cost_var.get()
    competitor_price = entry_competitor_price_var.get()
    desired_profit_margin = entry_profit_margin_var.get()

    optimal_price, input_values = calculate_optimal_price(product_cost, competitor_price, desired_profit_margin)

    if optimal_price is not None:
        print(f"Added Data Point: {input_values}")
        data_points.append(input_values)
        update_table()
        plot_graph()

        # Append the new entry to the dataset and save to CSV file
        new_entry = {'Product Cost': float(product_cost), 'Competitor Price': float(competitor_price),
                     'Desired Profit Margin': float(desired_profit_margin)}
        dataset = pd.DataFrame(data_points, columns=['Product Cost', 'Competitor Price', 'Optimal Price'])
        dataset = dataset.append(new_entry, ignore_index=True)
        dataset.to_csv('tshirt_data.csv', index=False)

def clear_fields():
    entry_cost_var.set("")
    entry_competitor_price_var.set("")
    entry_profit_margin_var.set("")
    label_optimal_price["text"] = ""

def update_table():
    for item in data_table.get_children():
        data_table.delete(item)

    for index, values in enumerate(data_points, start=1):
        data_table.insert("", "end", values=(index, *values))

def plot_graph():
    if not data_points:
        messagebox.showinfo("Info", "No data points to plot the graph!!")
        return

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    costs, competitor_prices, optimal_prices = zip(*data_points)

    unique_colors = plt.cm.viridis(np.linspace(0, 1, len(data_points)))
    for i in range(len(data_points)):
        plt.scatter(costs[i], competitor_prices[i], c=[unique_colors[i]], label=f'Data Point {i + 1}', marker='o')

    for i in range(1, len(data_points)):
        plt.plot([costs[i - 1], costs[i]], [competitor_prices[i - 1], competitor_prices[i]], color=unique_colors[i],
                 linestyle='--')

    plt.xlabel("Product Cost")
    plt.ylabel("Competitor Price")
    plt.title("Optimal Price Data Points")
    plt.legend()

    plt.subplot(1, 2, 2)
    indices = np.arange(len(data_points))
    bar_width = 0.2
    opacity = 0.7

    plt.bar(indices, costs, bar_width, alpha=opacity, color='b', label='Product Cost')
    plt.bar(indices + bar_width, competitor_prices, bar_width, alpha=opacity, color='g', label='Competitor Price')
    plt.bar(indices + 2 * bar_width, optimal_prices, bar_width, alpha=opacity, color='r', label='Optimal Price')

    plt.xlabel('Data Points')
    plt.ylabel('Price')
    plt.title('Product Cost, Competitor Price, and Optimal Price')
    plt.xticks(indices + bar_width, [str(i + 1) for i in range(len(data_points))])
    plt.legend()

    plt.show()

def load_dataset():
    file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            dataset = pd.read_csv(file_path)
            for index, row in dataset.iterrows():
                optimal_price, input_values = calculate_optimal_price(row['Product Cost'], row['Competitor Price'], row['Desired Profit Margin'])
                if optimal_price is not None:
                    print(f"Calculated Optimal Price for Entry {index + 1}: {optimal_price}")
                    data_points.append(input_values)
            update_table()
            plot_graph()
        except pd.errors.EmptyDataError:
            messagebox.showwarning("Warning", "The selected file is empty.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the dataset: {str(e)}")

data_points = []

root = tk.Tk()
root.title("E-commerce Price Optimization Tool")
root.geometry("800x400")

entry_cost_var = tk.StringVar()
entry_competitor_price_var = tk.StringVar()
entry_profit_margin_var = tk.StringVar()
# product cost

label_cost = tk.Label(root, text="Product Cost:")
label_cost.grid(row=0, column=0, pady=10)
entry_cost = tk.Entry(root, width=10, textvariable=entry_cost_var)
entry_cost.grid(row=0, column=1, pady=10)

# competittor price

label_competitor_price = tk.Label(root, text="Competitor Price:")
label_competitor_price.grid(row=1, column=0, pady=10)
entry_competitor_price = tk.Entry(root, width=10, textvariable=entry_competitor_price_var)
entry_competitor_price.grid(row=1, column=1, pady=10)

#profit margin

label_profit_margin = tk.Label(root, text="Desired Profit Margin (%):")
label_profit_margin.grid(row=2, column=0, pady=10)
entry_profit_margin = tk.Entry(root, width=10, textvariable=entry_profit_margin_var)
entry_profit_margin.grid(row=2, column=1, pady=10)

# Calculate price button

button_calculate_price = tk.Button(root, text="Calculate Price", command=handle_calculate_price)
button_calculate_price.grid(row=3, column=0, columnspan=2, pady=10)

# Add data point botton

button_add_data_point = tk.Button(root, text="Add Data Point", command=add_data_point)
button_add_data_point.grid(row=4, column=0, columnspan=2, pady=10)

# Clear button

button_clear = tk.Button(root, text="Clear", command=clear_fields)
button_clear.grid(row=5, column=0, columnspan=2, pady=10)

# load data set button

button_load_dataset = tk.Button(root, text="Load Dataset", command=load_dataset)
button_load_dataset.grid(row=6, column=0, columnspan=2, pady=10)

label_optimal_price = ttk.Label(root)
label_optimal_price.grid(row=7, column=0, columnspan=2, pady=10)

data_table_frame = ttk.Frame(root)
data_table_frame.grid(row=8, column=0, columnspan=2, pady=10)

# using treeview module in tkinter for adding a table in tkinter window

data_table = ttk.Treeview(data_table_frame, columns=('Index', 'Product Cost', 'Competitor Price', 'Optimal Price'),
                          show='headings')
data_table.heading('Index', text='Index')
data_table.heading('Product Cost', text='Product Cost')
data_table.heading('Competitor Price', text='Competitor Price')
data_table.heading('Optimal Price', text='Optimal Price')
data_table.pack(side=tk.LEFT, fill=tk.Y)

# adding scrollbar in tkinter window

data_table_scrollbar = ttk.Scrollbar(data_table_frame, orient="vertical", command=data_table.yview)
data_table_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
data_table.configure(yscrollcommand=data_table_scrollbar.set)

root.mainloop()
