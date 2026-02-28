import pandas as pd
import numpy as np
import statsmodels.api as sm
import os

def analyze_elasticity_and_simulation():
    # Load processed sales data
    df = pd.read_csv('data/processed_sales_data.csv')
    
    sku_elasticities = []
    
    unique_skus = df['sku_id'].unique()
    
    for sku in unique_skus:
        sku_data = df[df['sku_id'] == sku].copy()
        
        # log-log regression: log(Units) = a + b * log(Price)
        # Add 1 to avoid log(0)
        sku_data['log_units'] = np.log(sku_data['units_sold'] + 1)
        sku_data['log_price'] = np.log(sku_data['price'])
        
        X = sm.add_constant(sku_data['log_price'])
        model = sm.OLS(sku_data['log_units'], X).fit()
        
        elasticity = model.params.get('log_price', 0)
        p_value = model.pvalues.get('log_price', 1.0)
        
        sku_elasticities.append({
            'sku_id': sku,
            'elasticity': round(elasticity, 4),
            'p_value': round(p_value, 4),
            'is_elastic': 'Elastic' if elasticity < -1 else 'Inelastic'
        })
        
    elasticity_df = pd.DataFrame(sku_elasticities)
    
    # 2. Phase 4: Revenue Impact Simulation
    # Simulations: +5%, +10%, -5%, -10%
    price_changes = [0.05, 0.10, -0.05, -0.10]
    simulation_results = []
    
    # Aggregate current metrics
    sku_summary = df.groupby('sku_id').agg({
        'revenue': 'sum',
        'units_sold': 'sum',
        'price': 'mean'
    }).rename(columns={'revenue': 'current_revenue', 'units_sold': 'current_units', 'price': 'avg_price'})
    
    sku_summary = sku_summary.merge(elasticity_df, on='sku_id')
    
    for _, row in sku_summary.iterrows():
        e = row['elasticity']
        curr_units = row['current_units']
        curr_rev = row['current_revenue']
        curr_price = row['avg_price']
        
        for change in price_changes:
            # New Units = Current Units * (1 + Price Change)^Elasticity
            # (Note: Using the simplified power law assumption for elasticity)
            new_units = curr_units * ((1 + change) ** e)
            new_price = curr_price * (1 + change)
            new_rev = new_units * new_price
            
            simulation_results.append({
                'sku_id': row['sku_id'],
                'price_change_pct': f"{int(change*100)}%",
                'predicted_units': round(new_units, 0),
                'predicted_revenue': round(new_rev, 2),
                'revenue_diff': round(new_rev - curr_rev, 2)
            })
            
    sim_df = pd.DataFrame(simulation_results)
    
    # Save results
    elasticity_df.to_csv('data/sku_elasticity.csv', index=False)
    sim_df.to_csv('data/revenue_simulation.csv', index=False)
    
    print("Elasticity and Simulation analysis complete.")
    print(f"Average elasticity: {elasticity_df['elasticity'].mean():.2f}")
    print(f"Number of Elastic SKUs: {(elasticity_df['is_elastic'] == 'Elastic').sum()}")

if __name__ == "__main__":
    analyze_elasticity_and_simulation()
