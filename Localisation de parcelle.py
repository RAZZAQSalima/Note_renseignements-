from arcpy import *
from fpdf import FPDF

env.overwriteOutput=True

Date_NRU =arcpy.GetParameterAsText(0)
Nom_du_demandeur=arcpy.GetParameterAsText(1)
Numero_du_demandeur=arcpy.GetParameterAsText(2)
dxf = arcpy.GetParameterAsText(3)
couche_out=arcpy.GetParameterAsText(4)
titre =arcpy.GetParameterAsText(5)
path_bd=arcpy.GetParameterAsText(6)
nru=arcpy.GetParameterAsText(7)

env.workspace=os.path.join(path_bd,"office.gdb")

CADToGeodatabase_conversion(dxf,env.workspace,'test','50000','Nord Maroc')
  

with da.SearchCursor("Polygon",["Shape_area"]) as cursor:
    for row in cursor:
        surface_total =row[0]

Intersect_analysis(["PERIMETRES_IRRIGUES","Polygon"],"intersect_irrigues")
surface_intersection =0

with da.SearchCursor("intersect_irrigues",["area"]) as cursor:
    for row in cursor:
        surface_intersection +=row[0]

zones,communes=[],[]

with da.SearchCursor("intersect_irrigues",["Nom_Perime","area"]) as cursor:
    for row in cursor:
        zones.append([row[0],row[1]])
        
        
        
Intersect_analysis (["Polygon","zoneORMVAH2021_"], "intersect_zone")
  
with da.SearchCursor("intersect_zone","area") as cursor:
    for row in cursor:
        communes.append(row[0]) 

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


if  int (surface_intersection) ==0 :
       pdf=FPDF('P','mm','A4')
       pdf.add_page()
       pdf.image(os.path.join(path_bd,"logo.jpg"),x=2.4,w=197.9,h=26.5)
       pdf.set_font('arial','', 11)
       pdf.set_text_color(0,0,0)
       pdf.ln(5)
       var= " N "+str (Numero_du_demandeur)+"/ORH/SEHA/BTR                                                                                Marrakech, le "+str (Date_NRU)        
       pdf.cell(0,5, var )
       pdf.set_text_color(170,0,0)
       pdf.ln(40)
       pdf.set_font('arial','BI',18)
       pdf.cell(0,5, "                                           Attestation                                    " )
       pdf.ln(40)
       pdf.set_font('arial','', 13)
       pdf.cell(0,5,"                Le Directeur de l Office Regional de Mise en Valeur Agricole du Haouz") 
       pdf.ln(7)
       pdf.cell(0,5,"      atteste par la presente que, suite a la demande formulee par"+" "+ str (Nom_du_demandeur))
       pdf.ln(7)
       pdf.cell(0,5,"      et apres examen du plan delivre par le service du cadastre , Le titre foncier ")
       pdf.ln(7)       
       pdf.cell(0,5,"      n "+str(titre)+" , d une superficie totale de "+ str(surface_total)+" m2 se trouve en de tout")
       pdf.ln(7)
       pdf.cell(0,5,"      perimetre d irrigation ou zone amenagee relevant de la zone dehors d action")
       pdf.ln(7)
       pdf.cell(0,5,"      de l Office Regional de Mise en Valeur agricole du Haouz.")
       pdf.ln(10)    
       pdf.cell(0,5,"      De meme, vous trouverez ci-joint un extrait montrant la position du plan par rapport")
       pdf.ln(30)
       pdf.cell(0,5,"      La presente Attestation est delivree a l interessee pour servir et valoir ce que de ") 
       pdf.ln(5)
       pdf.cell(0,5,"      droit.")
       pdf.ln(60)
       pdf.image(os.path.join(path_bd,"logo1.jpg"),w=182.8,h=13.9)
       pdf.image(os.path.join(path_bd,"ORMVAH.jpg"),w=160, h=120)
       pdf.output(nru)
elif  int(surface_intersection )==int(surface_total ) :
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
       pdf.cell(0,5,"             Le Directeur de l’Office Régional de Mise en Valeur Agricole du Haouz atteste " )
       pdf.ln(5)
       pdf.cell(0,5,"       par la presente que, suite à la demande formulee par"+ str (Nom_du_demandeur) +"et apres ")
       pdf.ln(5)       
       pdf.cell(0,5,"       examen du plan delivre par le service du cadastre,Le titre foncier n"+str (titre))
       pdf.ln(5)
       pdf.cell(0,5,"       situe a "+str(zones[0][0])+ ", d une superficie totale de  "+ str(surface_total)+ "  m2 ")
       pdf.ln(5)
       pdf.cell(0,5,"       est affecte comme suit: "  )
       pdf.ln(5)
       pdf.cell(0,5,"               - Situe en périmètre d’irrigation :")
       pdf.ln(5)
       for zone in zones1:
        
            pdf.cell(0, 5,"                 - "+zone[0]+"                  - superficie:"+str(zone[1])+"m2")
            pdf.ln(5)
       pdf.cell(0, 5,"                - En zone d'action :")
       pdf.ln(5)
       for secteur in communes:
            pdf.cell(0,"                    - superficie:"+str(secteur[0])+"m2")
            pdf.ln(5)
       pdf.ln(10)
       pdf.cell(0, 5,"          De meme, vous trouverez ci-joint un extrait montrant la position du plan par rapport . ")
       pdf.ln(20)
       pdf.cell(0, 5,"      La presente Attestation est delivree a l interessee pour servir et valoir ce que de droit.")
       pdf.cell(0,5,"       que de droit .")
       pdf.ln(50)
       pdf.image(os.path.join(path_bd,"logo1.jpg"), w=182.8,h=13.9)
       pdf.image(os.path.join(path_bd,"ORMVAH.jpg"),w=160, h=120)       
       pdf.output(nru)   

elif int(surface_intersection )<int(surface_total):
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
       pdf.cell(0, 5,"           Le Directeur de l Office Regional de Mise en Valeur Agricole du Haouz atteste " )
       pdf.ln(5)
       pdf.cell(0, 5,"      par le presente que, suite à la demande formulee par "+ str (Nom_du_demandeur) +"et apres ")
       pdf.ln(5)       
       pdf.cell(0,5,"       examen du plan delivre par le service du cadastre, Le titre foncier n°"+str (titre) )
       pdf.ln(5)
       pdf.cell(0, 5,"      d une superficie totale de "+str (surface_total) +" est situe sur la limite .")
       pdf.ln(7)
       pdf.cell (0,5,"      des documents d urbanisme (DU) "+ str(zones[0][0]))
       pdf.ln(5)
       pdf.cell(0, 5,"      La partie du terrain situee a l interieur des DU d une superficie de "+str(surface_intersection)+" m2")
       pdf.ln(5)
       pdf.cell(0, 5,"      est affecte comme suit:")
       
       pdf.cell(0, 5,"               - Situe en périmètre d’irrigation :")
       pdf.ln(5)
       for zone in zones:
        
            pdf.cell(0, 5,"                 - "+zone[0]+"                  - superficie:"+str(zone[1])+" m2")
            pdf.ln(5)
       pdf.cell(0, 5,"                  - En zone d'action :")
       pdf.ln(5)
       for secteur in communes:
            pdf.cell(0,"                    - superficie:"+str(secteur[0])+" m2")
            pdf.ln(5)
       pdf.ln(15)
       pdf.cell(0, 5,"      De meme,vous trouverez ci-joint un extrait montrant la position du plan par rapport . ")
       pdf.ln(30)
       pdf.cell(0, 5,"      La presente Attestation est delivree a l interessee pour servir et valoir ce que de droit.")
       pdf.cell(0,5,"       que de droit .")
       pdf.ln(50)
       pdf.image(os.path.join(path_bd,"logo1.jpg"), w=182.8,h=13.9)
       pdf.image(os.path.join(path_bd,"ORMVAH.jpg"),w=160, h=120)       
       pdf.output(nru)   

