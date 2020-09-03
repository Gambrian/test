import sys, os
import pandas as pd
import plotly.graph_objects as go


def make_windows():
    bedfile_dir = "/home/zhluo/Project/CRC/data_nazhang/step42_chromatine_state_expression/every_week_state"

    for one_file in os.listdir(bedfile_dir):
        if "sorted" not in one_file:
            continue
        else:
            input_bed = os.path.join(bedfile_dir, one_file)

            out_bed = os.path.join("/home/zhluo/Project/CRC/data_nazhang/step43_sankey/segment_200_bin", one_file + ".200bin")
            cmd= "bedtools makewindows -b %s -w 200 -i src >%s" % (input_bed, out_bed)
            os.system(cmd)

def statistic_number():
    bin_file = "/home/zhluo/Project/CRC/data_nazhang/step43_sankey/segment_200_bin/combined.state.binfile.txt"
    df = pd.read_csv(bin_file, sep="\t", names=["chr", "start", "end", "ctrl_state", "week2_state", "week4_state", "week7_state", "week10_state"])
    print(df)
    change_state_list = []
    trace_dir = "/home/zhluo/Project/CRC/data_nazhang/step43_sankey/trace/"

    ctrl_week2 = df.groupby(["ctrl_state", "week2_state"]).size().reset_index(name="count")
    ctrl_week2.to_csv(os.path.join(trace_dir, "ctrl_week2.txt"), sep="\t")
    change_state_list.append(ctrl_week2)

    week2_week4 = df.groupby(["week2_state", "week4_state"]).size().reset_index(name="count")
    week2_week4.to_csv(os.path.join(trace_dir, "week2_week4.txt"), sep="\t")
    change_state_list.append(week2_week4)

    week4_week7 = df.groupby(["week4_state", "week7_state"]).size().reset_index(name="count")
    week4_week7.to_csv(os.path.join(trace_dir, "week4_week7.txt"), sep="\t")
    change_state_list.append(week4_week7)

    week7_week10 = df.groupby(["week7_state", "week10_state"]).size().reset_index(name="count")
    week7_week10.to_csv(os.path.join(trace_dir, "week7_week10.txt"), sep="\t")
    change_state_list.append(week7_week10)
    return change_state_list
    


def node_trace():
    #total nodes = 65, 13*5
    lable = ["ctrl_" + "E_" + str(i) for i in range(1,14)] + ["week2_" + "E_" + str(i) for i in range(1,14)] + ["week4_" + "E_" + str(i) for i in range(1,14)] + ["week7_" + "E_" + str(i) for i in range(1,14)]    + ["week10_" + "E_" + str(i) for i in range(1,14)]
    lable_s = ["E" + str(i) for i in range(1,14)] + ["E" + str(i) for i in range(1,14)] + ["E" + str(i) for i in range(1,14)] + ["E" + str(i) for i in range(1,14)]    + ["E" + str(i) for i in range(1,14)]

    #print(lable[0:13])
    source,target,value = [], [], []
    value0_2,value2_4,value4_7,value7_10 =[],[],[],[]
    sr,tr,vr =[],[],[]
    rowvalue = 0
    
    sortlist ={'state1':["E1","E3"],
                'state2':["E2"],
                'state3':["E4","E5"],
                'state4':["E6","E10","E11","E12","E13"],
                'state5':["E7","E8","E9"],
    }
    print(sortlist)

    ctrl_week2 = pd.read_csv("/home/zhluo/Project/CRC/data_nazhang/step43_sankey/trace/ctrl_week2.txt", sep="\t", index_col=0)
    #print(ctrl_week2)

    for i in range(1,6):
        for j in range(1,6):                                #6*6 node
            sr.append(i)
            tr.append(j+5)
            rowvalue = 0
            for sstate in sortlist["state"+str(i)]:
                for estate in sortlist["state"+str(j)]:
                    row = ctrl_week2[(ctrl_week2["ctrl_state"]==sstate) & (ctrl_week2["week2_state"]==estate)]
                    #print(int(row["count"]))
                    if row.empty:
                        continue
                    rowvalue =rowvalue + int(row["count"])                        #every node's value
            vr.append(rowvalue)

           
     
    week2_week4 = pd.read_csv("/home/zhluo/Project/CRC/data_nazhang/step43_sankey/trace/week2_week4.txt", sep="\t", index_col=0)
    for i in range(1,6):
        for j in range(1,6):
            sr.append(i+5)
            tr.append(j+5+5)
            rowvalue = 0
            for sstate in sortlist["state"+str(i)]:
                for estate in sortlist["state"+str(j)]:
                    row = week2_week4[(week2_week4["week2_state"]==sstate) & (week2_week4["week4_state"]==estate)]
                    if row.empty:
                        continue
                    rowvalue += int(row["count"])
            vr.append(rowvalue)


    week4_week7 = pd.read_csv("/home/zhluo/Project/CRC/data_nazhang/step43_sankey/trace/week4_week7.txt", sep="\t", index_col=0)
    for i in range(1,6):
        for j in range(1,6):
            sr.append(i+5+5)
            tr.append(j+5+5+5)
            rowvalue = 0
            for sstate in sortlist["state"+str(i)]:
                for estate in sortlist["state"+str(j)]:
                    row = week4_week7[(week4_week7["week4_state"]==sstate) & (week4_week7["week7_state"]==estate)]
                    if row.empty:
                        continue
                    rowvalue += int(row["count"])
            vr.append(rowvalue)
           

    week7_week10 = pd.read_csv("/home/zhluo/Project/CRC/data_nazhang/step43_sankey/trace/week7_week10.txt", sep="\t", index_col=0)
    for i in range(1,6):
        for j in range(1,6):
            sr.append(i+5+5+5)
            tr.append(j+5+5+5+5)
            rowvalue = 0
            for sstate in sortlist["state"+str(i)]:
                for estate in sortlist["state"+str(j)]:
                    row = week7_week10[(week7_week10["week7_state"]==sstate) & (week7_week10["week10_state"]==estate)]
                    if row.empty:
                        continue
                    rowvalue += int(row["count"])
            vr.append(rowvalue)
           
           
    result = []
    result.append(sr)
    result.append(tr)
    result.append(vr) 
    
    m1,m2,m3,m4,m5=[],[],[],[],[]
    for i in range(1,5):
        m1.append(result[2][(i*25-25)])
        m2.append(result[2][(i*25-19)])
        m3.append(result[2][(i*25-13)])
        m4.append(result[2][(i*25-7)])
        m5.append(result[2][(i*25-1)])
    m1m=min(m1)
    m2m=min(m2)
    m3m = min(m3)
    m4m = min(m4)
    m5m = min(m5)
    print(m1m,"/t",m2m,"/t",m3m,"/t",m4m,"/t",m5m)
    for i in range(1,5):
        #result[2][(i*25-25)]=result[2][(i*25-25)]-m1m
        result[2][(i*25-19)]=result[2][(i*25-19)]-m2m
        result[2][(i*25-13)]=result[2][(i*25-13)]-m3m
        result[2][(i*25-7)]=result[2][(i*25-7)]-m4m
        result[2][(i*25-1)]=result[2][(i*25-1)]-m5m
        
        
	#print(result[0])
    #print(result[1])
    #print(result[2])
    return result



def sankey():

    result = node_trace()
    
    linkcolor = [   
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(82,12,172,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(190,190,190,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(6,130,196,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(30,122,51,0.5)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
            "rgba(156,9,13,0.8)",
        ]
               
    for i in range(1,6):
        for j in range(1,21):
            if i != 1 and j%5 !=1 :
                linkcolor[(j*5+i-1-5)]="rgba(190,190,190,0.5)"
                
    fig = go.Figure(data=[go.Sankey(
    valueformat = ".0f",
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = ["0","state1", "state2", "state3", "state4","state5","state1", "state2", "state3", "state4", "state5","state1", "state2", "state3", "state4", "state5","state1", "state2", "state3", "state4", "state5","state1", "state2", "state3", "state4", "state5"],
      color = [ "rgba(0,0,0,0.8)",        #the first parmeter in "label" and "color" no means
            "rgba(82,12,172,0.8)",
            "rgba(231,227,251,0.6)",
            "rgba(231,227,251,0.6)",
            "rgba(231,227,251,0.6)",
            "rgba(231,227,251,0.6)",
            "rgba(82,12,172,0.8)",
            "rgba(231,227,251,0.6)",
            "rgba(231,227,251,0.6)",
            "rgba(231,227,251,0.6)",
            "rgba(231,227,251,0.6)",
            "rgba(82,12,172,0.8)",
            "rgba(231,227,251,0.6)",
            "rgba(231,227,251,0.6)",
            "rgba(231,227,251,0.6)",
            "rgba(231,227,251,0.6)",
            "rgba(82,12,172,0.8)",
            "rgba(231,227,251,0.6)",
            "rgba(231,227,251,0.6)",
            "rgba(231,227,251,0.6)",
            "rgba(231,227,251,0.6)",
            "rgba(82,12,172,0.8)",
            "rgba(231,227,251,0.6)",
            "rgba(231,227,251,0.6)",
            "rgba(231,227,251,0.6)",
            "rgba(231,227,251,0.6)",
        ]
    ),
    link = dict(
      source = result[0], # indices correspond to labels, eg A1, A2, A2, B1, ...
      target = result[1],
      value = result[2],
      color=linkcolor

      ),

    textfont= dict(size=1)
      )])

    fig.update_layout(title_text="State1 Sankey Diagram", font_size=10)
    #fig.write_image("./fig1.png", width=600, height=600)
    fig.show()

    







if __name__ == "__main__":
    #make 200 bp windows, the row in each file should be the same
    #make_windows()

    #step43, cd /home/zhluo/Project/CRC/data_nazhang/step43_sankey/segment_200_bin
    #paste -d "\t" /home/zhluo/Project/CRC/data_nazhang/step43_sankey/segment_200_bin/ctrl_13_segments.bed.sorted.200bin /home/zhluo/Project/CRC/data_nazhang/step43_sankey/segment_200_bin/2weeks_13_segments.bed.sorted.200bin /home/zhluo/Project/CRC/data_nazhang/step43_sankey/segment_200_bin/4weeks_13_segments.bed.sorted.200bin /home/zhluo/Project/CRC/data_nazhang/step43_sankey/segment_200_bin/7weeks_13_segments.bed.sorted.200bin /home/zhluo/Project/CRC/data_nazhang/step43_sankey/segment_200_bin/10weeks_13_segments.bed.sorted.200bin | cut -f 1,2,3,4,8,12,16,20 > /home/zhluo/Project/CRC/data_nazhang/step43_sankey/segment_200_bin/combined.state.binfile.txt
    #statistic_number()
    #node_trace()
    sankey()
