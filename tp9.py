import numpy as np

# Sample data (replace with your own data)
returns = np.array([0.10, 0.12, 0.15, 0.08])
risks = np.array([0.05, 0.07, 0.1, 0.06])
prices = np.array([50, 40, 60, 30])
budget =100

min_num_stocks = 1  # Adjust the minimum number of stocks constraint
max_num_stocks = 5  # Adjust the maximum number of stocks constraint
max_risk = 10
max_quantity = 3
min_quantity = 1  # Set the minimum quantity constraint

n = len(returns)

# Function to calculate portfolio performance
def calculate_portfolio_performance(weights):
    total_return = np.dot(returns, weights)
    total_risk = np.sqrt(np.dot(weights.T, np.dot(np.diag(risks**2), weights)))
    total_price = np.dot(prices, weights)
    return total_return, total_risk, total_price

# Function to generate neighbor solutions
def generate_neighbor(weights, index):
    neighbor = np.copy(weights)
    neighbor[index] += 0.1  # Adjust the weight of the selected stock
    return neighbor / np.sum(neighbor)  # Normalize to ensure weights sum to 1

# Initial weights (equal allocation)
best_weights = np.ones(n) / n

# Optimization using hill climbing
for _ in range(100):
    for i in range(n):
        neighbor_weights = generate_neighbor(best_weights, i)
        neighbor_return, neighbor_risk, neighbor_price = calculate_portfolio_performance(neighbor_weights)

        if (
            neighbor_return > calculate_portfolio_performance(best_weights)[0] and
            neighbor_risk <= max_risk and
            neighbor_price <= budget
        ):
            best_weights = neighbor_weights

# Post-processing to meet constraints on the number of stocks, minimum and maximum quantity
selected_stocks = np.where(best_weights > 0)[0]

# If more stocks are selected than the maximum allowed, keep the ones with the highest weights
if len(selected_stocks) > max_num_stocks:
    sorted_indices = np.argsort(best_weights)[::-1]
    selected_stocks = sorted_indices[:max_num_stocks]

# If fewer stocks are selected than the minimum allowed, keep the ones with the highest weights
elif len(selected_stocks) < min_num_stocks:
    sorted_indices = np.argsort(best_weights)[::-1]
    additional_stocks = sorted_indices[:min_num_stocks - len(selected_stocks)]
    selected_stocks = np.concatenate((selected_stocks, additional_stocks))

# Calculate quantities and other metrics
selected_quantities = np.floor(best_weights[selected_stocks] * budget / prices[selected_stocks])

# Distribute remaining budget evenly among selected stocks
remaining_budget = budget - np.sum(selected_quantities * prices[selected_stocks])
average_budget_per_stock = remaining_budget / len(selected_stocks)

# Ensure minimum quantity for each stock
selected_quantities = np.maximum(min_quantity, np.floor(average_budget_per_stock / prices[selected_stocks]))

# Apply maximum quantity constraint
selected_quantities = np.minimum(selected_quantities, max_quantity)


# Distribute remaining budget evenly among selected stocks
remaining_budget = budget - np.sum(selected_quantities * prices[selected_stocks])
average_budget_per_stock = remaining_budget / len(selected_stocks)

# Add the remaining budget evenly to the quantities
selected_quantities += average_budget_per_stock / prices[selected_stocks]

total_budget_used = np.sum(selected_quantities * prices[selected_stocks])
total_return, total_risk, _ = calculate_portfolio_performance(best_weights)

# Output results
print("Selected stocks:")
for i, stock_index in enumerate(selected_stocks):
    print(f"Stock {stock_index + 1} - Return: {returns[stock_index]}, Risk: {risks[stock_index]}, Price: {prices[stock_index]}, Quantity: {selected_quantities[i]}")

print(f"Total Budget Used: {total_budget_used}")
print(f"Total Return: {total_return}")
print(f"Total Risk: {total_risk}")
print(f"Number of Selected Stocks: {len(selected_stocks)}")
print(f"Total Quantity of Selected Stocks: {np.sum(selected_quantities)}")