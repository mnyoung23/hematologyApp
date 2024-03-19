import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import string

### Dicts

ratFemaleChemPartnerRef = {"WBC (×103/uL)":[5.44, 16.44], "Neut (%)":[4.4, 23.8], "Neut (×103/uL)":[0.34, 3.23], 
    "Lymph (%)":[67.1, 90.8], "Lymph (×103/uL)":[4.17, 13.65], "Mono (%)":[ 3.4, 9], "Mono (×103/uL)":[0.24, 1.06],
    "Eos (%)":[0.4, 2.1], "Eos (×103/uL)":[0.03,0.21], "Baso (%)":[0.0, 0.6], "Baso (×103/uL)":[0.0, 0.07],
    "Luc (%)":[0, 0, 0, 0], "Luc (×103/uL)":[0, 0, 0, 0], "Retic (%)":[2.36, 4.97], "Retic (×109/L)":[0.1803*1000, 0.3695*1000], 
    "HGB (g/dL)":[123/10, 173/10], "HCT (%)":[35.2, 48.7], "MCV (fL)":[52.8, 62], "MCH (Pg)":[18.9, 21.8], 
    "MCHC (g/dL)":[329/10, 366/10], "PLT (×103/uL)":[193, 1427], "RDW (%)":[10.2, 12.9], "RBC (×106/uL)":[5.96, 8.62]}

ratMaleChemPartnerRef = {"WBC (×103/uL)":[5.13, 15.65], "Neut (%)":[7.0, 26.6], "Neut (×103/uL)":[0.56,3.13], 
    "Lymph (%)":[61.3, 85.9], "Lymph (×103/uL)":[3.6,12.22], "Mono (%)":[5.0, 15.7], "Mono (×103/uL)":[0.36, 1.8],
    "Eos (%)":[0.2, 1.5], "Eos (×103/uL)":[0.02, 0.21], "Baso (%)":[0.1, 0.8], "Baso (×103/uL)":[0.01, 0.10],
    "Luc (%)":[0, 0, 0, 0], "Luc (×103/uL)":[0, 0, 0, 0], "Retic (%)":[2.81, 12.0], "Retic (×109/L)":[0.2177*1000, 0.7148*1000], 
    "HGB (g/dL)":[111/10, 161/10], "HCT (%)":[34.2, 48.4], "MCV (fL)":[54.7, 68.2], "MCH (Pg)":[19.0, 22.8], 
    "MCHC (g/dL)":[318/10, 356/10], "PLT (×103/uL)":[15, 1514], "RDW (%)":[10.7, 14.1], "RBC (×106/uL)":[5.20, 8.30]}

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

refDict = {
    "chempartner male":ratMaleChemPartnerRef, 
    "chempartner female":ratFemaleChemPartnerRef, 
    "clinbridge":ratClinBridgeRef,
    "taconic female":ratTaconicFemaleRef
    }

#### Functions ####
@st.cache_data
def preprocessData(file):
    wb = pd.read_excel(file, sheet_name=0)
     
    ## Clean up data table
    data = wb.iloc[3:, :]
    for i,val in enumerate(wb.iloc[1,:]):
        if isinstance(wb.iloc[1,i], float):
            wb.iloc[1,i] = wb.iloc[1,i-1]
        
    names = [str(wb.iloc[1,i]) + " (" + str(wb.iloc[2,i]) + ")" for i in range(len((wb.iloc[1,:])))]
    names[1] = "Group"
    df = pd.DataFrame(data)
    df.columns=names
    df.loc[:, "Group"] = [i.split("-")[0] for i in df.iloc[:,0]]
    return df

@st.cache_data
def generatePlots(df, cmap=[], xpos=[], dims=[10,15], ref=[], refxs=[]):
    df_melted = pd.melt(df.iloc[:,1:], id_vars=["Group"])
    gdf = df_melted.groupby('variable')
    dfkeys = list(np.unique(df_melted.variable))
    grpNames = np.unique(df_melted.Group)
    
    f, axes = plt.subplots(6, 4, figsize = (dims[0], dims[1]))

    if len(xpos) == len(grpNames):
        xdict = {grpNames[i]:int(xorder[i]) for i in range(len(grpNames))}
    else:
        xdict = {grpNames[i]:i for i in range(len(grpNames))}

    for name, g in gdf:
        agg = g.groupby('Group').agg(mean = ('value','mean'),
                  sem = ('value', 'sem'),
                  group = ('Group', 'first')
                  )

        ind = np.where(name == np.asarray(dfkeys))[0][0]
        ax = axes[gridLocs[ind]]

        xs = [xdict[i] for i in df.Group]
        xaggs = [xdict[i] for i in agg.group]
        xlocs = sorted(xaggs)
        
        
        refxs = [i for i in refxs if i]
        reflocs = [i.translate({ord(c): None for c in string.whitespace}).split(",") for i in refxs]
                 
        if (len(ref) > 0) & (len(reflocs) == len(ref)):
            for i, r in enumerate(ref):
                tempxlocs = [float(j) for j in reflocs[i]]
                ax.fill_between([tempxlocs[0],tempxlocs[1]], [refDict[r][name][0], refDict[r][name][0]], [refDict[r][name][1], refDict[r][name][1]], color="gray", alpha=0.2, linewidth=0)

        if len(cmap) == len(np.unique(df.Group)):
            ax.bar(x=xaggs, height="mean", yerr="sem", color=[cmap[xlocs.index(i)] for i in xaggs], capsize=2, linewidth=1, edgecolor="black", data=agg)
            ax.scatter(x=xs, y=g.value, color=[cmap[xlocs.index(i)] for i in xs], alpha=0.6, linewidth=1, edgecolor="black")
        else:
            ax.bar(x=xaggs, height="mean", yerr="sem", color="lightgray", capsize=2, linewidth=1, edgecolor="black", data=agg)
            ax.scatter(x=xs, y=g.value, color="black", alpha=0.6, linewidth=1, edgecolor="black")
        ax.set(ylabel=dfkeys[ind], xlabel="")
        if len(xpos) == len(grpNames):
            ax.set_xticks([int(i) for i in xpos])
            ax.set_xticklabels(agg.group, rotation=90)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.xaxis.set_tick_params(left='off', direction='out', width=1)
        ax.yaxis.set_tick_params(bottom='off', direction='out', width=1)
        ax.set_xlim(np.min(xaggs)-1, np.max(xaggs)+1)
        #ax.get_legend().remove()
    
    for i in range((len(gridLocs) - len(gdf))):
        axes[gridLocs[len(gridLocs)-(i+1)]].axis('off')

    plt.style.use('fast')
    return f, axes

st.title('Hematology Analysis')

with st.sidebar:
    uploaded_file = st.file_uploader("Choose a file")

    st.markdown("## Figure Dimensions")
    dims=st.text_input("Input your figure dimensions as length,height in inches.","")

    st.markdown("## X label")
    xlb = st.text_input("Input an xlabel if you would like one.","")

    st.markdown("## X Order")
    xorder = st.text_area("Type the positions that you would like your groups to appear in (e.g. 1,2,4 would position G1 at 1, G2 at 2, and G3 at 4). The number of assignments must equal the total number of unique groups.","", key=1)

    st.markdown("## Group Names")
    grps = st.text_area("Type group names as a comma separated list in the order of appearance on the x-axis (e.g. Group 1, Group 2, etc...)","", key=2)

    st.markdown("## Colors")
    cmap = st.text_area("Type colors in the order data appear on the x-axis (e.g. blue, blue, red, red, etc...)","", key=3)

    st.markdown("## Add Reference Ranges")
    refs = st.multiselect("## Select which reference ranges you want plotted.", ["chempartner male", "chempartner female", "clinbridge", "taconic female"])

    refxs = []
    for i, r in enumerate(refs):
        temp = st.text_input(f'Input x-start and x-stop positions as comma separated integers for {r}.', key=i*100)
        refxs.append(temp)

if uploaded_file:
    col1, col2 = st.columns(2)

    # To read file as bytes:
    df = preprocessData(uploaded_file)
    st.write(df)

    grpNames = np.unique(df.Group)
    xorder = xorder.translate({ord(c): None for c in string.whitespace}).split(",")
    dims = dims.translate({ord(c): None for c in string.whitespace}).split(",")
    xticks = grps.translate({ord(c): None for c in string.whitespace}).split(",")
    cmap = cmap.translate({ord(c): None for c in string.whitespace}).split(",")
    gridLocs = [(i,j) for i in [0,1,2,3,4,5] for j in [0,1,2,3]]

    if len(dims) == 2:
        dims = [int(i) for i in dims]
        f, axes = generatePlots(df, cmap, xorder, dims, ref=refs, refxs=refxs)
    else:
        f, axes = generatePlots(df, cmap, xorder, ref=refs, refxs=refxs)

    if len(xticks) == len(grpNames):
        xorder = [int(i) for i in xorder]
        for i in gridLocs:
            axes[i].set_xticks(sorted(xorder))
            axes[i].set_xticklabels(xticks, rotation=90)
            axes[i].set_xlim(np.min(xorder)-1, np.max(xorder)+1)

    if xlb != "":
        for i in gridLocs:
            axes[i].set_xlabel(xlb)

    plt.tight_layout()

    st.pyplot(f)

