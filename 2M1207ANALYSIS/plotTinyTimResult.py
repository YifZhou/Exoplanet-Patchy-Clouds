#! /usr/bin/env python
from __future__ import print_function
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('ggplot')
fn = '2M1207B_flt_F125W_result.csv'
df = pd.read_csv(fn, parse_dates = {'datetime':['obs date', 'obs time']}, index_col = 'datetime')
plt.plot(df.index, df['fluxA'], 's', label = '2M1207 A')
plt.plot(df.index, df['fluxB'], 'o', label = '2M1207 B')
plt.gcf().autofmt_xdate()
plt.legend(loc = 'best')
plt.xlabel('UT')
plt.ylabel('Normalized flux')

plt.show()