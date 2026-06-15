# optimizer.py
import numpy as np

def simulate_demand(base_demand, predicted_price, simulated_price, elasticity=1.4, market_mode="Balanced Market"):
    """
    Simulates consumer market demand volume using Price Elasticity of Demand (PED).
    """
    if predicted_price <= 0 or simulated_price <= 0:
        return 0
    
    # Apply dynamic multiplier shifts based on selected market climate
    if market_mode == "High Demand (Sellers' Market)":
        effective_base_demand = base_demand * 1.6   # 60% expansion in transaction volumes
        effective_elasticity = elasticity * 0.8     # Consumers are less price sensitive due to scarcity
    elif market_mode == "High Competition (Buyers' Market)":
        effective_base_demand = base_demand * 0.65  # Competitors capture market share, lowering traffic
        effective_elasticity = elasticity * 1.4     # High sensitivity; buyers jump to rival alternatives quickly
    else:
        effective_base_demand = base_demand
        effective_elasticity = elasticity

    # Core Microeconomic Constant Elasticity Equation
    price_ratio = simulated_price / predicted_price
    simulated_demand = effective_base_demand * (price_ratio ** (-effective_elasticity))
    
    return int(max(0, np.round(simulated_demand)))


def simulate_supply(unit_cost, predicted_price, simulated_price, base_supply=400, market_mode="Balanced Market"):
    """
    Simulates market-wide supply allocation using inventory production margins.
    """
    if simulated_price <= unit_cost:
        return 0
    
    # Adjust baseline competitive inventory density based on competition layout
    if market_mode == "High Competition (Buyers' Market)":
        effective_base_supply = base_supply * 1.9   # Market is flooded with stock from rivals
    elif market_mode == "High Demand (Sellers' Market)":
        effective_base_supply = base_supply * 0.55  # Inventory scarcity across the platform
    else:
        effective_base_supply = base_supply

    # Linear-root supply scaling function based on target profitability thresholds
    margin_ratio = (simulated_price - unit_cost) / (predicted_price - unit_cost + 1e-5)
    simulated_supply = effective_base_supply * (margin_ratio ** 0.5)
    
    return int(max(0, np.round(simulated_supply)))


def calculate_financials(simulated_price, simulated_demand, unit_cost):
    """
    Calculates operational transaction metrics for the active simulation slice.
    """
    revenue = simulated_price * simulated_demand
    total_cost = unit_cost * simulated_demand
    profit = revenue - total_cost
    return revenue, profit