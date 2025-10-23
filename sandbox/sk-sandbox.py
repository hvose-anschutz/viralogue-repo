#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.sparse as sp
import re

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
import my_functions.files.graph_settings as gs

def set_value(row_number, assigned_value):
    return assigned_value[row_number]

my_tumor_data = {}

df = pd.read_table("just_log_values.txt",sep="\t",index_col=0,header=0)

mydf = df.T

x = mydf.drop('TumorType',axis=1)
y = pd.DataFrame(data=mydf['TumorType'])

y['TumorType'] = y['TumorType'].map({1.0:"Cut_nod",2.0:"Cut_SS",3.0:"Acral",4.0:"Subungual",5.0:"Muc_ano",6.0:"Muc_nasal",7.0:"Muc_vul",8.0:"Unknown",9.0:"Other", 10.0:"Unde"})

print(y.head())

#do the scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(x)

#do the PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print("Explained variance: ", pca.explained_variance_ratio_)
print("Cumulative: ", np.cumsum(pca.explained_variance_ratio_))

plot_df = pd.DataFrame(data=X_pca, columns=['PCA_1','PCA_2'])
print(plot_df.head())
final_df = pd.concat([plot_df.reset_index(drop=True), y.reset_index(drop=True)], axis=1)
final_df.columns = ['PCA_1','PCA_2','TumorType']
print(final_df.head())

my_range = np.linspace(start=-25,stop=25,num=2238)

color_range = gs.get_default_wheel()

# plt.figure(figsize=(8,6))
# plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, edgecolor='k')
# plt.xlabel("Principal Component 1")
# plt.ylabel("Principal Component 2")
# plt.title("PCA Transformed Data")
# plt.colorbar(label="Relative Gene Expression")
# plt.savefig("pca_kasey_test.jpg", dpi=300,format='jpg')

g = sns.scatterplot(data=final_df, x="PCA_1", y="PCA_2",hue='TumorType',palette=color_range)

fig = g.figure

fig.savefig('my_PCA.jpg', format='jpg')