import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_data():
    # Set seed for reproducibility
    np.random.seed(42)
    
    # 1. Product Definitions
    categories = ['Electronics', 'Home & Kitchen', 'Sports', 'Books', 'Toys']
    skus_per_category = 20
    skus = []
    
    sku_counter = 1001
    for cat in categories:
        for i in range(skus_per_category):
            skus.append({
                'sku_id': f'SKU_{sku_counter}',
                'product_name': f'{cat} Product {i+1}',
                'category': cat,
                'base_price': np.random.uniform(10, 500),
                'cost_multiplier': np.random.uniform(0.5, 0.7)
            })
            sku_counter += 1
            
    df_products = pd.DataFrame(skus)
    df_products['cost'] = df_products['base_price'] * df_products['cost_multiplier']
    
    # 2. Daily Sales Data (365 days)
    start_date = datetime(2025, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(365)]
    
    sales_data = []
    competitor_data = []
    competitors = ['MarketLeader', 'DiscouterPlace', 'PremiumHub']
    
    for _, product in df_products.iterrows():
        sku_id = product['sku_id']
        base_price = product['base_price']
        cost = product['cost']
        
        # Price elasticity coefficient (randomly assigned to make it interesting)
        # Some are elastic (-2.5), some are inelastic (-0.5)
        elasticity = np.random.uniform(-3.0, -0.2)
        
        # Initial inventory
        inventory = np.random.randint(500, 2000)
        
        for date in dates:
            # Randomly fluctuate price (+/- 10%) occasionally
            price_fluctuation = 1.0
            if np.random.random() < 0.1: # 10% chance of price change
                price_fluctuation = np.random.uniform(0.9, 1.1)
            
            current_price = base_price * price_fluctuation
            
            # Demand logic: Base demand * (Price Ratio)^Elasticity + Seasonality/Noise
            # Base demand is roughly 10-50 units
            base_demand = np.random.uniform(10, 50)
            price_ratio = current_price / base_price
            demand = base_demand * (price_ratio ** elasticity)
            
            # Add noise and seasonality (weekend boost)
            noise = np.random.normal(0, 2)
            weekend_boost = 1.3 if date.weekday() >= 5 else 1.0
            units_sold = int(max(0, (demand * weekend_boost) + noise))
            
            # Inventory management
            inventory -= units_sold
            if inventory < 200: # Restock
                inventory += np.random.randint(500, 1000)
                
            revenue = units_sold * current_price
            
            sales_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'sku_id': sku_id,
                'product_name': product['product_name'],
                'category': product['category'],
                'price': round(current_price, 2),
                'units_sold': units_sold,
                'revenue': round(revenue, 2),
                'cost': round(cost, 2),
                'inventory_on_hand': inventory
            })
            
            # 3. Competitor Data (Weekly samples)
            if date.weekday() == 0: # Every Monday
                for comp in competitors:
                    # Competitors track our base price but with noise
                    comp_fluctuation = np.random.uniform(0.85, 1.15)
                    competitor_data.append({
                        'sku_id': sku_id,
                        'competitor_name': comp,
                        'competitor_price': round(base_price * comp_fluctuation, 2),
                        'date': date.strftime('%Y-%m-%d')
                    })
                    
    # Save to CSV
    if not os.path.exists('data'):
        os.makedirs('data')
        
    pd.DataFrame(sales_data).to_csv('data/sales_data.csv', index=False)
    pd.DataFrame(competitor_data).to_csv('data/competitor_data.csv', index=False)
    print("Data generated successfully in data/ directory.")

if __name__ == "__main__":
    generate_data()
