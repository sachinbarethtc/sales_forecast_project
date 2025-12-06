df = pd.read_sql("""
    SELECT * 
    FROM mbazaar_sandbox.forecast_results_assortment
    WHERE prediction_type = 'weekly'
    ORDER BY prediction_date;
""", engine)

df



df = pd.read_sql("""
    SELECT * 
    FROM mbazaar_sandbox.forecast_results_new
    WHERE prediction_type = 'monthly'
    ORDER BY prediction_date;
""", engine)

df
