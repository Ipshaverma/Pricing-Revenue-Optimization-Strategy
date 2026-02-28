import pandas as pd
import numpy as np
import os

def analyze_pricing_and_segmentation():
    # Load data
    sales_df = pd.read_csv('data/sales_data.csv')
    
    # 1. Price Distribution Analysis
    # Create price buckets (Low, Medium, High) based on quantiles
    sales_df['price_bucket'] = pd.qcut(sales_df['price'], 3, labels=['Low', 'Medium', 'High'])
    
    # Aggregate by bucket
    bucket_analysis = sales_df.groupby('price_bucket').agg({
        'sku_id': 'nunique',
        'revenue': 'sum',
        'units_sold': 'sum'
    }).rename(columns={'sku_id': 'num_skus'})
    
    print("Price Bucket Analysis:")
    print(bucket_analysis)
    
    # 2. SKU Segmentation (Pareto Analysis)
    sku_revenue = sales_df.groupby(['sku_id', 'product_name', 'category']).agg({
        'revenue': 'sum',
        'units_sold': 'sum',
        'price': 'mean'
    }).reset_index().rename(columns={'price': 'avg_price'})
    
    # Rank SKUs by revenue descending
    sku_revenue = sku_revenue.sort_values(by='revenue', ascending=False)
    
    # Calculate cumulative revenue percentage
    sku_revenue['cum_revenue'] = sku_revenue['revenue'].cumsum()
    total_rev = sku_revenue['revenue'].sum()
    sku_revenue['cum_revenue_pct'] = sku_revenue['cum_revenue'] / total_rev
    
    # Assign segments based on Pareto logic (Top 20%, Next 60%, Bottom 20%)
    def assign_segment(pct):
        if pct <= 0.20:
            return 'Top'
        elif pct <= 0.80:
            return 'Core'
        else:
            return 'Tail'
            
    sku_revenue['sku_segment'] = sku_revenue['cum_revenue_pct'].apply(assign_segment)
    
    print("\nSKU Segmentation Analysis:")
    print(sku_revenue.groupby('sku_segment').agg({
        'sku_id': 'count',
        'revenue': 'sum'
    }))
    
    # Save processed data for Power BI
    # Join segment back to daily sales for granular analysis
    segment_map = sku_revenue[['sku_id', 'sku_segment']]
    sales_df = sales_df.merge(segment_map, on='sku_id')
    
    sales_df.to_csv('data/processed_sales_data.csv', index=False)
    sku_revenue.to_csv('data/sku_segmentation.csv', index=False)
    
    print("\nProcessed data saved to data/ directory.")

if __name__ == "__main__":
    analyze_pricing_and_segmentation()
