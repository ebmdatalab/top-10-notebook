# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ## Analysis of Top 10 Medicines
#
# We are interested to see the "top 10" medicines use in NHS primary care in England in 2019. WE will produce the top 10 chemicals and BNF paragraphs by volume and cost.

import pandas as pd
import numpy as np
from ebmdatalab import bq, maps, charts

# +

pd.set_option('display.float_format', lambda x: '%.2f' % x)
# -

# ## Top 10 Chemicals in 2019 by Volume

# +
## code for top 10 items
sql = '''
WITH
  bnf_tab AS (
  SELECT
    DISTINCT chemical,
    chemical_code
  FROM
    ebmdatalab.hscic.bnf )
SELECT
 SUBSTR(presc.bnf_code, 0, 9) AS chemical_code, ##user requested chemical substance
 chemical,
 SUM(items) AS items,
 Sum(actual_cost) AS actualcost
FROM
ebmdatalab.hscic.normalised_prescribing_standard AS presc
LEFT JOIN
bnf_tab
ON
chemical_code=SUBSTR(presc.bnf_code,0,9)
WHERE
 month BETWEEN TIMESTAMP('2019-01-01')
 AND TIMESTAMP('2019-12-01') ##user requested 2019
GROUP BY
chemical_code,
chemical
ORDER BY
 items DESC
 LIMIT 20 ##limit to 20
  '''

df_chemical_items = bq.cached_read(sql, csv_path='chemical_items.csv')
df_chemical_items.head(11)
# -

# ## Top 10 Chemicals in 2019 by Cost

# +
sql = '''
WITH
  bnf_tab AS (
  SELECT
    DISTINCT chemical,
    chemical_code
  FROM
    ebmdatalab.hscic.bnf )
SELECT
 SUBSTR(presc.bnf_code, 0, 9) AS chemical_code, ##user requested chemical substance
 chemical,
 SUM(items) AS items,
 Sum(actual_cost) AS actualcost
FROM
ebmdatalab.hscic.normalised_prescribing_standard AS presc
LEFT JOIN
bnf_tab
ON
chemical_code=SUBSTR(presc.bnf_code,0,9)
WHERE
 month BETWEEN TIMESTAMP('2019-01-01')
 AND TIMESTAMP('2019-12-01') ##user requested 2018
GROUP BY
chemical_code,
chemical
ORDER BY
 actualcost DESC
 LIMIT 20 ##limit to 20
  '''

df_chemical_cost = bq.cached_read(sql, csv_path='chemical_cost.csv')
df_chemical_cost.head(11)
# -

# ## Top 10 Classes of Medicines in 2019 by Volume

# +
sql = '''
WITH
  bnf_tab AS (
  SELECT
    DISTINCT para,
    para_code
  FROM
    ebmdatalab.hscic.bnf )
SELECT
 SUBSTR(presc.bnf_code, 0, 6) AS para_code, ##user requested chemical substance
 para,
 SUM(items) AS items,
 Sum(actual_cost) AS actualcost
FROM
ebmdatalab.hscic.normalised_prescribing_standard AS presc
LEFT JOIN
bnf_tab
ON
para_code=SUBSTR(presc.bnf_code,0,6)
WHERE
 month BETWEEN TIMESTAMP('2019-01-01')
 AND TIMESTAMP('2019-12-01') ##user requested 2019
GROUP BY
para_code,
para
ORDER BY
 items DESC
 LIMIT 20 ##limit to 20
  '''

df_para_items = bq.cached_read(sql, csv_path='para_items.csv')
df_para_items.head(11)
# -

# ## Top 10 Classes of Medicines in 2019 by Cost

# +
sql = '''
WITH
  bnf_tab AS (
  SELECT
    DISTINCT para,
    para_code
  FROM
    ebmdatalab.hscic.bnf )
SELECT
 SUBSTR(presc.bnf_code, 0, 6) AS para_code, ##user requested chemical substance
 para,
 SUM(items) AS items,
 Sum(actual_cost) AS actualcost
FROM
ebmdatalab.hscic.normalised_prescribing_standard AS presc
LEFT JOIN
bnf_tab
ON
para_code=SUBSTR(presc.bnf_code,0,6)
WHERE
 month BETWEEN TIMESTAMP('2019-01-01')
 AND TIMESTAMP('2019-12-01') ##user requested 2019
GROUP BY
para_code,
para
ORDER BY
 actualcost DESC
 LIMIT 20 ##limit to 20
  '''

df_para_cost = bq.cached_read(sql, csv_path='para_cost.csv')
df_para_cost.head(11)
