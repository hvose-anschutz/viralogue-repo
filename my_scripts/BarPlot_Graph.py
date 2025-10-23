import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys
import re

FileCSV = "Data.csv"
print(FileCSV)
mySVGOut = re.sub(".csv$","_Image.svg",FileCSV,1)

DataSet = pd.read_csv(FileCSV,index_col = 0)
#TissueOrder = ["Colon"]	#Must edit for new dataset
TissueOrder = ["mLN","PeyersPatch","Proximal Colon","Epithelial cells"]	#Must edit for new dataset
#TreatmentOrder = ["ControlDiet","HiFiDiet"]
#TreatmentOrder = ["Control","Amp","Vanc"]		#Must edit for new dataset
#TreatmentOrder = ["Control_Starch", "Control_AcStarch", "Amp_Starch", "Amp_AcStarch"]
#TreatmentOrder = ["MHV-Y", "MHV-Y_dHE"]
#TreatmentOrder = ["SPF", "GF"]
#TreatmentOrder = ["WT", "CD64-creSTING-flox"]
#TreatmentOrder = ["Control","Amp","AmpHydroxybutyrate","AmpTributyrin"]
TreatType = DataSet.copy()
TreatType = TreatType.pop("Tissue")
WhiteWheel = dict()
for Treat in TreatType:
	WhiteWheel.setdefault(Treat, '#FFFFFF')

#ColorWheel = ("#88BFB2","#E37D57","#4273B2") #,"#98AD8B","#E3CBCA","#DA788E","#A36E37","#BABC4E","#C1AFCD","#675852","#F3DD96")#,"#BCDBE8","#BA412E","#879FB7","#29636C","#7C4480","#B24C87","#3A714D","#483530")
#lut = dict(zip(TreatType.unique(), ColorWheel))
ColorWheel = dict([
('Control', '#a0c3d9'),
('SPF', '#f1c4c8'),
('PeyersPatch', '#4b81bf'),
('Proximal Colon', '#F6C163'),
('Epithelial cells', '#29636C'),
('ControlDiet', '#BCDBE8'),
('HiFiDiet', '#7C4480'),
('Amp', '#BA412E'),
('Vanc', '#A36E37'),
('Control_Starch', '#BCDBE8'),
('Control_AcStarch', '#215996'),
('Amp_Starch', '#BA412E'),
('Amp_AcStarch', '#C1AFCD'),
('mLN', '#BCDBE8'),
('MHV-Y_dHE', '#B54062'),
('MHV-Y','#BCDBE8'),
('CD64-creSTING-flox','#f1c4c8'),
('Amp','#cc4273'),
('AmpHydroxybutyrate','#3ca858'),
('AmpTributyrin','#c1db3c'),
])


g = sns.catplot(data=DataSet,
    kind="bar",
	x="Tissue",
    y="Log_Copies", 
    hue="Tissue",	#defines how the bars will be split
    order = TissueOrder,	#defines the order of the tissues on the x axis
    #hue_order = TissueOrder, #defines the order of the treatment on the X axis
    errorbar="sd", #specifies whether using an error bar or a confidence interval
    err_kws={'linewidth':0.75},	#line width of the error bar
    capsize = .1,	#This controls the cap of the stdev whisker
    palette= ColorWheel, #This controls the colors on the graph, must be a hash Treatment value to Hex code
 	saturation = 1,
    height=6,		#This controls the height of the graph
    aspect = 1.2, #4 Categories
#    aspect = 1, #3 Categories
#    aspect = .7, #2 Categories
	linewidth = 1, #defines the line thickness around the bar
	edgecolor = "black",	#defines the line color around the bar
	legend=False
)
#g.despine(left=True)
g.set_xlabels("")
g.set_ylabels("")
#g.legend.set_title("")
# g.savefig(mySVGOut)


# Draw a categorical scatterplot to show each observation
ax = sns.swarmplot(data=DataSet, 
					hue="Tissue", 
					x="Tissue",
					y="Log_Copies", 
					dodge = "true",	#Makes ure the dots are not plotted in the same column
				    order = TissueOrder,
			        #hue_order = TreatmentOrder, #defines the order of the treatment on the X axis
					palette = WhiteWheel, #defines color palette to make sure every dot is white
					edgecolor = "black",
					size = 12,	#defines size of dot
					linewidth = .75, #defines the line thickness around the white dot
					legend=False
)
#ax.set(ylim=(0, 6))
g.set_xlabels("")
g.set_ylabels("")
g.savefig(mySVGOut)