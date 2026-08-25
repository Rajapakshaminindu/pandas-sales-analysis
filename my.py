"""Lesson 1: Python values and variables."""

# A variable gives a meaningful name to a value.
customer_name = "Amina"
orders = 4
average_order_value = 25.50
is_member = True

total_spent = 70 #orders * average_order_value

print("Customer:", customer_name)
print("Total spent:", total_spent)
print("Member:", is_member)

# A list stores multiple values in order.
weekly_sales = [120, 95, 140, 110]
average_daily_sales = sum(weekly_sales) / len(weekly_sales)

# A dictionary stores related information using named keys.
customer = {
	"name": "Amina",
	"orders": 4,
	"member": True,
}

print("Average daily sales:", average_daily_sales)
print("Customer name from dictionary:", customer["name"])

# Conditional statements let a program make decisions.
if total_spent >= 100:
	print("Customer qualifies for a discount.")
elif total_spent >= 50:
	print("Customer is close to a discount.")
else:
	print("Customer does not qualify for a discount yet.")

# A for loop repeats code for every value in a list.
total_weekly_sales = 0
for daily_sales in weekly_sales:
	print("Daily sales:", daily_sales)
	total_weekly_sales = total_weekly_sales + daily_sales

print("Total weekly sales:", total_weekly_sales)

for daily_sales in weekly_sales:
    if daily_sales >= 120:
        print("Strong sales day:", daily_sales)

# A function is a reusable block of code.
# It can take inputs (parameters) and return a result.
def calculate_average(values):
    return sum(values) / len(values)

# Use the function with a list.
avg_sales = calculate_average(weekly_sales)
print("Average sales using function:", avg_sales)

# Another function to classify sales.
def sales_status(sales_value):
    if sales_value >= 120:
        return "High"
    elif sales_value >= 100:
        return "Medium"
    else:
        return "Low"

print("Status for 120:", sales_status(120))
print("Status for 95:", sales_status(95))