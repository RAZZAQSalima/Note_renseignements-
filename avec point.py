from arcpy import *
from fpdf import FPDF

env.overwriteOutput=True

Date_NRU =arcpy.GetParameterAsText(0)
Nom_du_demandeur=arcpy.GetParameterAsText(1)
Numero_du_demandeur=arcpy.GetParameterAsText(2)
txtfilepath=arcpy.GetParameterAsText(3)
couche_out=arcpy.GetParameterAsText(4)
titre=arcpy.GetParameterAsText(5)
path_bd=arcpy.GetParameterAsText(6)
nru=arcpy.GetParameterAsText(7)

env.workspace=os.path.join(path_bd,"office.gdb")

MakeXYEventLayer_management(txtfilepath,"X","Y","point") 
k= CopyFeatures_management("point","pnt")
with da.SearchCursor("pnt",["Shape@"]) as cursor:
    for row in cursor:
        surface_total=row[0].area
Intersect_analysis (["pnt","PERIMETRES_IRRIGUES"], "intersectpt")
surface_intersection=0

with da.SearchCursor("intersectpt",["shape@"]) as cursor:
    for row in cursor:
        surface_intersection+=row[0].area 
N=[]        
with da.SearchCursor("intersectpt",["Nom_Perime"]) as cursor:
    for row in cursor :  
         N.append (row[0])

Kx,ky=[],[]
with da.SearchCursor("pnt",["shape@XY"]) as cursor:
    for row in cursor :  
      Kx.append(row[0][0])
      ky.append(row[0][1])
      
Near_analysis("pnt","PERIMETRES_IRRIGUES")    
L =[] 
with da.SearchCursor("pnt",["NEAR_DIST"]) as cursor :
    for row in cursor:
        L.append(row[0]) 

  

mxd=mapping.MapDocument(os.path.join(path_bd,"workplace.mxd"))
df = arcpy.mapping.ListDataFrames(mxd)
refLayer = arcpy.mapping.ListLayers(mxd)
c=[]
liste_couhe=ListFeatureClasses()

for i in range(len(liste_couhe)):
    c.append(os.path.join(env.workspace,liste_couhe[i]))

for i in range(len(c)):
    insertLayer = arcpy.mapping.Layer(c[i])
    arcpy.mapping.InsertLayer(df[0], refLayer[0],insertLayer , "AFTER")
    
for lyr in mapping.ListLayers(mxd):    
        lyr.visible=True
    
mapping.ExportToJPEG(mxd,os.path.join(path_bd,"ORMVAH.jpg"))

if  surface_intersection ==0 and L[0] != 0 :
    
           
    pdf=FPDF('P','mm','A4')
    pdf.add_page()
    pdf.image(os.path.join(path_bd,"logo.jpg"),x=2.4,w=197.9,h=26.5)
    pdf.set_font('arial','', 11)
    pdf.set_text_color(0,0,0)
    pdf.ln(5)
    var= " N "+str (Numero_du_demandeur)+"/ORH/SEHA/BTR                                                                                         Marrakech, le "+str (Date_NRU)        
    pdf.cell(0,5, var )
    pdf.set_text_color(170,0,0)
    pdf.ln(40)
    pdf.set_font('arial','BI',18)
    pdf.cell(0,5, "                                            Attestation                                    " )
    pdf.set_text_color(0,0,0)
    pdf.ln(40)
    pdf.set_font('arial','', 13)
    pdf.cell(0,5,"                 Le Directeur de l Office Regional de Mise en Valeur Agricole du Haouz") 
    pdf.ln(7)
    pdf.cell(0,5,"         atteste par la presente que, suite a la demande formulee par"+" "+ str (Nom_du_demandeur))
    pdf.ln(7)
    pdf.cell(0,5,"         et apres examen du plan delivre par le service du cadastre , Le titre foncier ")
    pdf.ln(7)       
    pdf.cell(0,5,"         n "+str(titre)+" , d une coordonne centroide ( X ; Y ) = (" + str(Kx[0])+";"+str(ky[0]) +") se trouve ")
    pdf.ln(7)
    pdf.cell(0,5,"         dehors des perimetres d irrigations.La distance minimale c est "+ str (L[0]) + " miles.")
    pdf.ln(15)    
    pdf.cell(0,5,"         De meme, vous trouverez ci-joint un extrait montrant la position du plan .")
    pdf.ln(30)
    pdf.cell(0,5,"         La presente Attestation est delivree a l interessee pour servir et valoir ce que de ") 
    pdf.ln(7)
    pdf.cell(0,5,"         droit.")
    pdf.ln(60)
    pdf.image(os.path.join(path_bd,"logo1.jpg"),w=182.8,h=13.9)
    pdf.image(os.path.join(path_bd,"ORMVAH.jpg"),w=160, h=120)
    pdf.output(nru)   
    
else :
    pdf=FPDF('P','mm','A4')
    pdf.add_page()
    pdf.image(os.path.join(path_bd,"logo.jpg"),x=2.4,w=197.9,h=26.5)
    pdf.set_font('arial','', 11)
    pdf.set_text_color(0,0,0)
    pdf.ln(5)
    var= " N "+str (Numero_du_demandeur)+"/ORH/SEHA/BTR                                                                                         Marrakech, le "+str (Date_NRU)        
    pdf.cell(0,5, var )
    pdf.set_text_color(170,0,0)
    pdf.ln(40)
    pdf.set_font('arial','BI',18)
    pdf.cell(0,5, "                                            Attestation                                    " )
    pdf.set_text_color(0,0,0)
    pdf.ln(40)
    pdf.set_font('arial','', 13)
    pdf.cell(0,5,"                 Le Directeur de l Office Regional de Mise en Valeur Agricole du Haouz") 
    pdf.ln(7)
    pdf.cell(0,5,"         atteste par la presente que, suite a la demande formulee par"+" "+ str (Nom_du_demandeur))
    pdf.ln(7)
    pdf.cell(0,5,"         et apres examen du plan delivre par le service du cadastre , Le titre foncier ")
    pdf.ln(7)       
    pdf.cell(0,5,"         n "+str(titre)+" , d une coordonne centroide (X ; Y ) = (" + str(Kx[0])+";"+str(ky[0]) +") se trouve a ")
    pdf.ln(7)
    pdf.cell(0,5,"         l interieur du perimetre d irrigation  "+ str (N[0]) + ".")
    pdf.ln(15)    
    pdf.cell(0,5,"         De meme, vous trouverez ci-joint un extrait montrant la position du plan .")
    pdf.ln(30)
    pdf.cell(0,5,"         La presente Attestation est delivree a l interessee pour servir et valoir ce que de ") 
    pdf.ln(7)
    pdf.cell(0,5,"         droit.")
    pdf.ln(60)
    pdf.image(os.path.join(path_bd,"logo1.jpg"),w=182.8,h=13.9)
    pdf.image(os.path.join(path_bd,"ORMVAH.jpg"),w=160, h=120)
    pdf.output(nru)

