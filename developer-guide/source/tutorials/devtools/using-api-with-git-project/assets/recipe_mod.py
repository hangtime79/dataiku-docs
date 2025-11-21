# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np

import io
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
ecommerce_transactions_with_ip_prepared = dataiku.Dataset("ecommerce_transactions_with_ip_prepared")
df = ecommerce_transactions_with_ip_prepared.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
country_name = dataiku.get_variables()["country_name"]
df_filtered = df[df['MerchantIP_country'] == country_name]

df_avg_purchase = df_filtered[['PurchaseHour', 'CustomerAge', 'OrderTotal']].groupby(by = ['PurchaseHour',
                                                                                 'CustomerAge'],as_index=False).mean()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xs = df_avg_purchase['PurchaseHour']
ys = df_avg_purchase['CustomerAge']
zs = df_avg_purchase['OrderTotal']

ax.set_xlabel('PurchaseHour')
ax.set_ylabel('CustomerAge')
ax.set_zlabel('OrderTotal')

ax.scatter(xs, ys, zs)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
folder_for_plot = dataiku.Folder("dy9hOjP1")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Compute recipe outputs from inputs

bs = io.BytesIO()
plt.savefig(bs, format="png")
folder_for_plot.upload_stream("scatter_plot.png", bs.getvalue())
