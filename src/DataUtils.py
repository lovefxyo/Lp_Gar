import pandas as pd
class DataUtils:
    def __init__(self,graph_e_file,graph_v_file,graph_route):
        self.graph_e_file=graph_e_file
        self.graph_v_file=graph_v_file
        self.graph_route=graph_route
        self.e_data=None
        self.v_data=None
        self.route=None
    def init(self):
        self.e_data=pd.read_csv(self.graph_e_file,delimiter=",")
        self.v_data=pd.read_csv(self.graph_v_file,delimiter=",")
        self.route=pd.read_csv(self.graph_route,delimiter=",")
    #此方法只适合最后一列存在分隔符，除去此分隔符以便于读取
    def split_seq(self,del_num,input_file,output_file):
        fw=open(output_file,"w")
        with open(input_file,"r") as f:
            lines=f.readlines()
            for line in lines:
                while(line.count(",")>del_num):
                    line_list=list(line)
                    line_list.pop(line.rfind(","))
                    line=''.join(line_list)
                fw.writelines(line)
    #获得路径的小图，percentage是获得的百分比，为int
    def get_smallgraph(self,percentage,output_file):
        df=pd.read_csv(self.graph_route)
        df_new=df.iloc[0:int(df.size*percentage/1000),:]
        df_new.columns=["id:int"]
        df_new.to_csv(output_file,index=None,sep="\t",) 
    #获得在路径route中出现的边
    def get_e_inroute(self,output_file):
        new_e=pd.merge(pd.merge(self.e_data,self.route,left_on="source_id:int",right_on="id:int"),self.route,left_on="target_id:int",right_on="id:int")
        new_e.reindex(columns=["edge_id:int","source_id:int","target_id:int","label_id:int"]).to_csv(output_file,index=None)
    #获得在路径route中出现的点
    def get_v_inroute(self,output_file):
        new_v=pd.merge(self.v_data,self.route,left_on="vertex_id:int",right_on="id:int")
        new_v.reindex(columns=["vertex_id:int","label_id:int","attr:string"]).to_csv(output_file,index=None)