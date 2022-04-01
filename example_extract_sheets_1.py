# import library
import pandas as pd
import root_to_df as lib_root

# load the class RootToPdf
url_root="tag_1_delphes_events_example.root" # url to root file
rtf=lib_root.RootToPdf(path=url_root,tree_name="Delphes")

# conver sheets

df=rtf.extract_sheets("MissingET.MET")

# save df in csv

df.to_csv("./out_df/extract_sheets1.csv",sep="|",index=False)
