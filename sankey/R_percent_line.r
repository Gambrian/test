#trace.txt is from python script sankey.py output 
setwd("D:/Workplace/sankey")
sankey.trace <- read.table("trace.txt",sep = "\n")
sankey.trace <- matrix(sankey.trace$V1,nrow = 5,ncol = 20)

#compute node and percentage
node <- apply(sankey.trace,2,sum)
node.tail <- apply(sankey.trace[,16:20],1,sum)
node.tail
node <-c(node,node.tail)
node
save(sankey.trace, file = "tmp.RData")
state.average<-function(i,c1){
  c(c1[i]/sum(c1[1:5]),
    c1[i+5]/sum(c1[6:10]),
    c1[i+10]/sum(c1[11:15]),
    c1[i+15]/sum(c1[16:20]),
    c1[i+20]/sum(c1[21:25]))
}
state.average(1,node)
node_frame <- data.frame(state1=state.average(1,node),
                         state2=state.average(2,node),
                         state3=state.average(3,node),
                         state4=state.average(4,node),
                         state5=state.average(5,node),
                         stringsAsFactors = FALSE)
row.names(node_frame) <- c("ctrl","week2","week4","week7","week10")

library(ggplot2)
library(patchwork)

#build drawing function,the parameter i is state, str is color of line
p_state<-function(i,str){
  statei <- paste("state",as.character(i),sep = "")
  ggplot(data = node_frame,aes(x=c(1,2,3,4,5),y=node_frame[,i]))+
  geom_line(color=str,size=0.8)+
  scale_y_continuous(expand = c(0, 0),
                     breaks = c(0,0.05,0.1,0.15,0.2,0.25),
                     labels = c("0","5%","10%","15%","20%","25%"),limits = c(0,0.25)) +
  scale_x_continuous(labels = NULL)+
  labs(x="",y=colnames(node_frame)[i])+
    theme_bw()+
    theme(panel.grid=element_blank())
  
}

p1 <- p_state(1,"#520CAC")
p2 <- p_state(2,"#BEBEBE")
p3 <- p_state(3,"#0682C4")
p4 <- p_state(4,"#1E7A33")
p5 <- p_state(5,"#9C090D")
p<-(p1|p3)/
(p4|p5)


#print as pdf
pdf("result.pdf",width = 6,height = 4)
p
dev.off()

