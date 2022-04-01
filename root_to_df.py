import awkward
import numpy as np
import pandas as pd
import uproot


class RootToPdf:
    def __init__(self,path:str,tree_name:str="Delphes"):
        self.tree=uproot.open(path)[tree_name]
        
    def detect_type_branch(self,i):
        arr_ret=[0,0]
        if ("/" in i or "." in i):
            indice = i.find("/")
            bran=i[indice+1:]
            arr_ret[0]=0
            arr_ret[1]=bran
        elif("_" in i):
            arr_ret[0]=1
            arr_ret[1]=i
        else:
            arr_ret[0]=2
            arr_ret[1]=i
        return arr_ret

    def extract_sheets(self,branch,max_elements=None):
        df2=pd.DataFrame()
        arr_branch=self.detect_type_branch(branch)
        indicador=0
        if arr_branch[0]==0:
            indicador=arr_branch[0]
            ja = self.tree[arr_branch[1]].array(library="pd")
            df_al=ja.to_frame()
            df2=df_al.unstack(level=-1)
            if ("missinget" in arr_branch[1].lower()):
                columna=[arr_branch[1].lower().replace(".","_")]
            else:
                columna=[arr_branch[1].lower().replace(".","_")+str(i) for i in range(len(df2.columns))]
            df2.columns=columna
            df2.index.name = None

        elif arr_branch[0]==1:
            indicador=arr_branch[0]
            ja = self.tree[arr_branch[1]].array(library="pd")
            df2=ja.to_frame()
            df2.columns=[arr_branch[1].lower()]
        else:
            indicador=arr_branch[0] 
            try:
                ja = self.tree[arr_branch[1]].array(library="pd")
                df2=ja.to_frame()
                df2.columns=[arr_branch[1].lower()]
            except:
                pass

        
        if max_elements!=None:
            colum_new_pro=self.colum_new(max_elements,[branch])
            dfr=pd.DataFrame()
            for j in colum_new_pro:
                try:
                    dfra=df2[[j]]
                    dfr = pd.concat([dfr, dfra], axis=1,)
                except:
                    dfr[j] = np.nan
            df2=dfr           

        return df2

    def colum_new(self,max_elemnt,colum_branch):
        colum_new=[]
        for j in colum_branch:
            arr_branch=self.detect_type_branch(j)

            if arr_branch[0]==0:
                if ("missinget" in arr_branch[1].lower()):
                    colum_new.append(arr_branch[1].lower().replace(".","_"))
                else:
                    for i in range(max_elemnt):
                        colum_new.append(arr_branch[1].lower().replace(".","_")+str(i))
            elif (arr_branch[0]==1):
                colum_new.append(arr_branch[1].lower())
            else:
                colum_new.append(arr_branch[1].lower())
                #pass
                
        return colum_new
    
    def extract_df_branch(self,colum_branch=[],max_elements=None):
        df=pd.DataFrame()
        for i in colum_branch:
            df1=self.extract_sheets(i)
            df = pd.concat([df, df1], axis=1,)
        if max_elements!=None:
            colum_new_pro=self.colum_new(max_elements,colum_branch)
            dfr=pd.DataFrame()
            for j in colum_new_pro:
                try:
                    dfra=df[[j]]
                    dfr = pd.concat([dfr, dfra], axis=1,)
                except:
                    dfr[j] = np.nan
                
            df=dfr
        return df
    
