import pandas as pd
import numpy as np
import os

def analyze_market_and_inventory():
    # Load data
    sales_df = pd.read_csv('data/processed_sales_data.csv')
    comp_df = pd.read_csv('data/competitor_data.csv')
    
    # 1. Phase 5: Competitor Pricing Analysis
    # Get average price per SKU from our sales data
    our_prices = sales_df.groupby('sku_id')['price'].mean().reset_index().rename(columns={'price': 'our_avg_price'})
    
    # Join with competitor data
    market_df = comp_df.merge(our_prices, on='sku_id')
    market_df['price_gap'] = market_df['our_avg_price'] - market_df['competitor_price']
    market_df['price_gap_pct'] = (market_df['price_gap'] / market_df['competitor_price']) * 100
    
    # Identify price position
    def identify_pos(gap_pct):
        if gap_pct > 5: return 'Premium'
        elif gap_pct < -5: return 'Discount'
        else: return 'Market Parity'
        
    market_df['price_position'] = market_df['price_gap_pct'].apply(identify_pos)
    
    # 2. Phase 6: Inventory Sufficiency Check
    # Calculate average daily sales (last 30 days or overall)
    avg_sales = sales_df.groupby('sku_id')['units_sold'].mean().reset_index().rename(columns={'units_sold': 'avg_daily_sales'})
    
    # Get latest inventory
    latest_inventory = sales_df.sort_values('date').groupby('sku_id').tail(1)[['sku_id', 'inventory_on_hand']]
    
    inventory_check = latest_inventory.merge(avg_sales, on='sku_id')
    
    # Inventory Cover = Inventory / Avg Daily Sales (Days of Stock)
    inventory_check['inventory_cover_days'] = inventory_check['inventory_on_hand'] / inventory_check['avg_daily_sales'].replace(0, np.nan)
    
    # Risk Flags
    def get_risk(days):
        if days < 7: return 'High Stockout Risk'
        elif days < 14: return 'Medium Stockout Risk'
        elif days > 60: return 'Overstock Risk'
        else: return 'Healthy Stock'
        
    inventory_check['inventory_risk'] = inventory_check['inventory_cover_days'].apply(get_risk)
    
    # Save results
    market_df.to_csv('data/competitor_analysis.csv', index=False)
    inventory_check.to_csv('data/inventory_sufficiency.csv', index=False)
    
    print("Market and Inventory analysis complete.")
    print("\nSample Inventory Risk:")
    print(inventory_check['inventory_risk'].value_counts())

if __name__ == "__main__":
    analyze_market_and_inventory()
