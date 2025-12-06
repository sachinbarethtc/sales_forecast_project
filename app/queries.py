DAY_AGG_SQL = """
SELECT
    sh.bill_date::date AS day,
    sh.site_code,
    sh.icode,
    COALESCE(af.assortment_name, 'UNKNOWN') AS assortment_name,
    SUM(sh.qty) AS total_qty
FROM {schema}.{sales_table} sh
LEFT JOIN {schema}.{assort_table} af
       ON sh.icode = af.icode
WHERE sh.bill_date IS NOT NULL
  AND sh.bill_date BETWEEN :start_date AND :end_date
GROUP BY
    sh.bill_date::date,
    sh.site_code,
    sh.icode,
    af.assortment_name
ORDER BY 1, 2, 3;
"""
