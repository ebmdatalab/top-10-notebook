# -*- coding: utf-8 -*-
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

# Building on our work on [top 10 medicines](https://ebmdatalab.net/top10-medicines-2019/) a user copule of people have been in touch asking for longer lists at a chemical substance level. Reusing the code from the Top 10 we will produce the "top 500" as a data dump to support others analysis.
#
# Please cite as "The DataLab, University of Oxford, https://ebmdatalab.net/top10-medicines-2019/" or similar.

#import libraries
import pandas as pd
import numpy as np
import os
from ebmdatalab import bq, maps, charts

#this sets £ and pence properly
pd.set_option('display.float_format', lambda x: '%.2f' % x)

# ## Top 500 chemicals in 2019 by volume

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
 LIMIT 500 ##limit to 500
  '''

df_chemical_items_500 = bq.cached_read(sql, csv_path=os.path.join('..','data','chemical_items_500.csv'))
df_chemical_items_500.head(50)
# -

# ## Top 500 chemicals in 2019 by cost

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
 LIMIT 500 ##limit to 500
  '''

df_chemical_cost_500 = bq.cached_read(sql, csv_path=os.path.join('..','data','chemical_cost_500.csv'))
df_chemical_cost_500.head(51)
# -


