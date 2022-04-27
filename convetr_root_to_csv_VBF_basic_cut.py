#find /cms/mc/MG5_aMC_v3_1_1/pp_2_hjj_and_h_2_4mu_0_10/Events/ -name "*.root"

import os
import uproot
import root_to_df as lib_root
import pandas as pd
import numpy as np

s1=os.popen('find /cms/mc/MG5_aMC_v3_1_1/pp_2_hjj_and_h_2_4mu_0_10/Events/ -name "*.root"').read()
s2=os.popen('find /cms/mc/MG5_aMC_v3_1_1/pp_2_hjj_and_h_2_4mu_11_20/Events/ -name "*.root"').read()
list_archivos=s1.split()+s2.split()


branch=["MissingET.MET","MissingET.Phi",
"Jet.PT","Jet.Eta","Jet.Phi","Jet.Mass",
"Muon.PT","Muon.Eta","Muon.Phi","Muon.Charge"]

def count_na(row):
  var = row.loc["jet_pt0":"jet_pt3"].notnull().sum()
  return var

df = pd.DataFrame()

for i in range(len(list_archivos)):
    print(i)
    rtf=lib_root.RootToPdf(path=list_archivos[i],tree_name="Delphes")
    df_root=rtf.extract_df_branch(branch,4)

    df_root.loc[df_root.jet_pt0<30,'jet_pt0']=np.nan
    df_root.loc[df_root.jet_pt1<30,'jet_pt1']=np.nan
    df_root.loc[df_root.jet_pt2<30,'jet_pt2']=np.nan
    df_root.loc[df_root.jet_pt3<30,'jet_pt3']=np.nan

    df_root["sum_jet"]=df_root.apply(count_na, axis = 1)

    df_root2=df_root[df_root["sum_jet"]>=2].drop(['sum_jet'], axis=1)


    df=df.append(df_root2, ignore_index=True)

print(len(df))

df.to_csv("./out_df/VBF_MC_filter.csv",sep="|",index=False)

