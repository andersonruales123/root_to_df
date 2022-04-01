# import library
import pandas as pd
import root_to_df as lib_root

# load the class RootToPdf
url_root="tag_1_delphes_events_example.root" # url to root file
rtf=lib_root.RootToPdf(path=url_root,tree_name="Delphes")

#define branch

branch=["MissingET.MET","MissingET.Eta","MissingET.Phi","Jet.PT","Jet.Eta","Jet.Phi",
"Jet.Mass","Jet.TauTag","Jet.BTag","Jet_size"]


# conver branch
df_root=rtf.extract_df_branch(branch,2)

# save df in csv

df_root.to_csv("./out_df/extract_branch.csv",sep="|",index=False)