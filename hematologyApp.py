import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import string

### Dicts

ratFemaleChemPartnerRef = {"WBC (×103/uL)":[5.44, 16.44], "Neut (%)":[4.4, 23.8], "Neut (×103/uL)":[0.34, 3.23], 
    "Lymph (%)":[67.1, 90.8], "Lymph (×103/uL)":[4.17, 13.65], "Mono (%)":[ 3.4, 9], "Mono (×103/uL)":[0.24, 1.06],
    "Eos (%)":[0.4, 2.1], "Eos (×103/uL)":[0.03,0.21], "Baso (%)":[0.0, 0.6], "Baso (×103/uL)":[0.0, 0.07],
    "Luc (%)":[0, 0, 0, 0], "Luc (×103/uL)":[0, 0, 0, 0], "Retic (%)":[2.36, 4.97], "Retic (×109/L)":[0.1803*1000, 0.3695*1000], 
    "HGB (g/dL)":[123/10, 173/10], "HCT (%)":[35.2, 48.7], "MCV (fL)":[52.8, 62], "MCH (Pg)":[18.9, 21.8], 
    "MCHC (g/dL)":[329/10, 366/10], "PLT (×103/uL)":[193, 1427], "RDW (%)":[10.2, 12.9], "RBC (×106/uL)":[5.96, 8.62]}

ratClinBridgeRef = {"WBC (×103/uL)":[3.3, 8.7], "Neut (%)":[3.3, 26.6], "Neut (×103/uL)":[0.3,1.7], 
    "Lymph (%)":[68.6, 94.5], "Lymph (×103/uL)":[2.6, 7.1], "Mono (%)":[0, 4.1], "Mono (×103/uL)":[0, 0.2],
    "Eos (%)":[0, 5.0], "Eos (×103/uL)":[0, 0.1], "Baso (%)":[0, 1.0], "Baso (×103/uL)":[0, 0.02],
    "Luc (%)":[0, 1.0], "Luc (×103/uL)":[0, 0.02], "Retic (%)":[1.0, 5.0], "Retic (×109/L)":[60, 300], 
    "HGB (g/dL)":[10.6, 15.6], "HCT (%)":[32.7, 44.8], "MCV (fL)":[43.5, 62.7], "MCH (Pg)":[15.8, 19.9], 
    "MCHC (g/dL)":[31.4, 36.0], "PLT (×103/uL)":[493,1124], "RDW (%)":[11.9, 16.1], "RBC (×106/uL)":[5.5,9.3]}

ratTaconicFemaleRef = {"WBC (×103/uL)":[4.5, 7.5], "Neut (%)":[], "Neut (×103/uL)":[0.1, 0.7], 
    "Lymph (%)":[], "Lymph (×103/uL)":[4.1,6.9], "Mono (%)":[], "Mono (×103/uL)":[0, 0.2],
    "Eos (%)":[], "Eos (×103/uL)":[], "Baso (%)":[], "Baso (×103/uL)":[],
    "Luc (%)":[], "Luc (×103/uL)":[], "Retic (%)":[], "Retic (×109/L)":[], 
    "HGB (g/dL)":[15.5, 16.7], "HCT (%)":[51.2-2.6, 51.2+2.6], "MCV (fL)":[66, 67.8], "MCH (Pg)":[19.9, 22.1], 
    "MCHC (g/dL)":[], "PLT (×103/uL)":[1262.2-278.4, 1262.2+278.4], "RDW (%)":[], "RBC (×106/uL)":[7.4, 8.0]}

st.title('Hematology Analysis')

with st.sidebar:
    uploaded_file = st.file_uploader("Choose a file")

    st.markdown("## Group Names")
    st.write("Type group names as a comma separated list in the order of appearance on the x-axis (e.g. Group 1, Group 2, etc...)")
    grps = st.text_area("", key=123)

    st.markdown("## Colors")
    st.write("Type colors in the order data appear on the x-axis (e.g. blue, blue, red, red, etc...)")

    cmap = st.text_area("", key=234)    

if uploaded_file:
    col1, col2 = st.columns(2)

    # To read file as bytes:
    wb = pd.read_excel(uploaded_file, sheet_name=0)
    
    ## Clean up data table
    data = wb.iloc[3:, :]
    headerRows = wb.iloc[1:3, :]
    for i,val in enumerate(wb.iloc[1,:]):
            if isinstance(wb.iloc[1,i], float):
                 wb.iloc[1,i] = wb.iloc[1,i-1]

    names = [str(wb.iloc[1,i]) + " (" + str(wb.iloc[2,i]) + ")" for i in range(len((wb.iloc[1,:])))]
    names[1] = "Group"
    df = pd.DataFrame(data)
    df.columns=names
    df.loc[:, "Group"] = [i.split("-")[0] for i in df.iloc[:,0]]
    st.write(df)

    df_melted = pd.melt(df.iloc[:,1:], id_vars=["Group"])
    cols = df.columns[2:].to_list()

    gridLocs = [(i,j) for i in [0,1,2,3,4,5] for j in [0,1,2,3]]
    gdf = df_melted.groupby('variable')
    dfkeys = list(np.unique(df_melted.variable))

    f, axes = plt.subplots(6, 4, figsize = (10, 15))

    xticks = grps.translate({ord(c): None for c in string.whitespace}).split(",")
    cmap = cmap.translate({ord(c): None for c in string.whitespace}).split(",")

    print()
    for name, g in gdf:
        ind = np.where(name == np.asarray(dfkeys))[0][0]
        ax = axes[gridLocs[ind]]
        if len(cmap) == len(np.unique(df.Group)):
            sns.barplot(x=g.Group, y=g.value, hue=[cmap[np.where(i == np.unique(df.Group))[0][0]] for i in g.Group], alpha=0.6, ax=ax, capsize=0.2,
                linewidth=1, edgecolor="0")
            sns.scatterplot(x=g.Group, y=g.value, hue=[cmap[np.where(i == np.unique(df.Group))[0][0]] for i in g.Group], alpha=0.6, ax=ax, linewidth=1, edgecolor="0")
        else:
            sns.barplot(x=g.Group, y=g.value, hue=g.Group, alpha=0.6, ax=ax, capsize=0.2,
                linewidth=1, edgecolor="0")
            sns.scatterplot(x=g.Group, y=g.value, hue=g.Group, alpha=0.6, ax=ax, linewidth=1, edgecolor="0")
        ax.set(ylabel=dfkeys[ind], xlabel="")
        ax.get_legend().remove()

        grpNames = np.unique(df.Group)
        if len(xticks) == len(grpNames):
            ax.set_xticks(range(len(grpNames)))
            ax.set_xticklabels(xticks, rotation=90)

    sns.despine(bottom = False, left = False)

    for i in range((len(gridLocs) - len(gdf))):
        axes[gridLocs[len(gridLocs)-(i+1)]].axis('off')

    plt.tight_layout()



    
 #   with col2:
   #     st.markdown("## Add References")
  #      refs = st.multiselect(
    #        'Select reference ranges to view',
   #         ['SD Female ChemParter', 'SD ClinBridge', 'SD Female Taconic']
    #        )
   #     st.write("SD Female Chemparter - purple dash")
   #     st.write("SD ClinBridge - red dash")
   #     st.write("SD Female Taconic - green dash")
   # with col1:
    #    st.markdown("## Summary Table")
    #    st.dataframe(agg)    
    st.pyplot(f)
