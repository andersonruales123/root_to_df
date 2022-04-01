# import library
import pandas as pd
import root_to_df as lib_root

# load the class RootToPdf
url_root="tag_1_delphes_events_example.root" # url to root file
rtf=lib_root.RootToPdf(path=url_root,tree_name="Delphes")

# conver sheets

df=rtf.extract_sheets("Jet.PT",2) #2 is the number of Jet.PT to extract
#if the number is not entered, extract all possible columns
# save df in csv

df.to_csv("./out_df/extract_sheets2.csv",sep="|",index=False)

# Other example

df2=rtf.extract_sheets("Jet.PT")
df2.to_csv("./out_df/extract_sheets3.csv",sep="|",index=False)