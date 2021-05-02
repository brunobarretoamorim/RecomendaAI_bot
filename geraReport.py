import math
import os
import re
import subprocess
import sys
from io import BytesIO
from shutil import which
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import pylab as pl
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
class Visualization:
    import os
    image_dir = os.getcwd()
    
    def retornaDicionarioHabilidades(self,dc):
        a  = pd.DataFrame(data=dc.values(),index=dc.keys())
        a.reset_index(inplace=True)
        a.columns = ['Habil','Erro Medio']
        cod_hab = pd.read_parquet(os.path.join(os.getcwd(),'config','parametros_provas.parquet'))[['CO_HABILIDADE','Descricao_Habilidade']]
        b = pd.merge(cod_hab,a,left_on='Descricao_Habilidade',right_on='Habil')[['CO_HABILIDADE','Erro Medio']]
        b.drop_duplicates(inplace=True)
        return b
        #print('Deu certo')
    def bar(self,b):
        image_dir =  image_dir = os.getcwd()
        print("Generating Bar Plot.....")
        plt.figure(figsize=(10, 5))
        sns.set(style="white", font_scale=1.5)
        sns.barplot(x = b['CO_HABILIDADE'],y=b['Erro Medio'],color='#4169E1')
        plt.title("Seus principais erros por habilidades",
                  fontsize=24,
                  color="steelblue",
                  fontweight="bold",
                  fontname="Comic Sans MS")
        plt.savefig(os.path.join(image_dir,"bar.png"), dpi=400)
        plt.clf()
    def errosAlunoxBase(self,a,dc,materia):
        import pandas as pd
        image_dir =  image_dir = os.getcwd()
        erros_aluno = pd.DataFrame(dc.items(),columns=['Habil','erros'])
        media_erros = pd.DataFrame(a[materia.lower()].items(),columns=['Habil','erros'])
        df = pd.merge(erros_aluno,media_erros,on='Habil',suffixes=('_aluno', '_geral'))
        texto = 'Seus principais erros comparados com a média nacional'
        P = df.plot(kind='bar', stacked=True,
                    color = {'erros_aluno':'#4169E1','erros_geral':'#D3D3D3'},
                  figsize=(10,5),grid=False,rot=0,width=1)
        plt.title(texto,
                  fontsize=24,
                  color="steelblue",
                  fontweight="bold",
                  fontname="Comic Sans MS")
        P.set_facecolor('w')
        plt.savefig(os.path.join(image_dir,"bar_stacked.png"), dpi=400)
        plt.clf()
    
    def gen_wordcloud(self,lista_habilidades):
        image_dir =  image_dir = os.getcwd()
        #bg = np.array(Image.open('logo.png'))
        stopwords_lista = stopwords.words('portuguese')
        unique_string = ""

        texto_tratado = []
        for i in list(lista_habilidades):
            texto_para_analisar = i.split(' ')
            texto_tratado.append([c for c in texto_para_analisar if c not in(stopwords_lista)])

        for texto in texto_tratado:
            for palavra in texto:
                unique_string = unique_string+' '+palavra
        cloud = WordCloud(color_func=lambda *args, **kwargs: "gray",background_color='white',prefer_horizontal=1,contour_width=10).generate(unique_string)
        #plt.figure()
        plt.xticks([])
        plt.yticks([])
        plt.imshow(cloud) 
        #plt.axis('off') 
        texto = 'Termos mais frequentes em seus erros'
        #plt.rcParams["axes.linewidth"]  = True
        plt.title(texto,
                      fontsize=24,
                      color="steelblue",
                      fontweight="bold",
                      fontname="Comic Sans MS")
        plt.savefig(os.path.join(image_dir,"wordcloud.png"), dpi=400)
        plt.clf()
        #plt.show()
    
    def gen_pdf(self):
        image_dir = os.getcwd()
        print("Combining Images into PDF.....")
#         path1 = os.path.join(image_dir, "week_heatmap.png")
#         path2 = os.path.join(image_dir, "memory.png")
        path3 = os.path.join(image_dir, "bar_stacked.png")
        path4 = os.path.join(image_dir, "bar.png")
        path5 = os.path.join(image_dir, "wordcloud.png")
#         path6 = os.path.join(image_dir, "red.png")
        pdf = PdfFileWriter()

        # Using ReportLab Canvas to insert image into PDF
        img_temp = BytesIO()
        img_doc = canvas.Canvas(img_temp, pagesize=(3000, 2300))
        

        # heat map x, y - start position
#         img_doc.drawImage(path1, -150, 1400, width=2600, height=650)
#         # memory
#         img_doc.drawImage(path2, 1070, 681, width=697, height=667)
#         # bar_stacked
        img_doc.drawImage(path3, 1300, 1300, width=1286, height=620)
#         # word_cloud
        img_doc.drawImage(path5, -28, 300, width=1286, height=920)
#         # bar
        img_doc.drawImage(path4, -28, 1300, width=1286, height=620)
#         # logo
#         img_doc.drawImage(logo, 99, 2068, width=105, height=80)
        # red square
#         img_doc.drawImage(path6, inch * 24.3, inch * 16.25, width=91, height=45)
#         img_doc.drawImage(path6, inch * 24.3, inch * 14.69, width=91, height=45)
#         img_doc.drawImage(path6, inch * 24.3, inch * 13.14, width=91, height=45)
#         img_doc.drawImage(path6, inch * 24.3, inch * 11.60, width=91, height=45)

        # draw three lines, x,y,width,height
        img_doc.rect(0.83 * inch, 28.5 * inch, 40.0 * inch, 0.04 * inch, fill=1)
#         img_doc.rect(0.83 * inch, 18.9 * inch, 26.0 * inch, 0.04 * inch, fill=1)
#         img_doc.rect(0.83 * inch, 8.5 * inch, 26.0 * inch, 0.04 * inch, fill=1)
        # title
        img_doc.setFont("Helvetica-Bold", 82)
        img_doc.drawString(212, 2078, "Relatório de Erros Enem 2019",)

        img_doc.save()
        pdf.addPage(PdfFileReader(BytesIO(img_temp.getvalue())).getPage(0))
        with open(os.path.join(os.getcwd(),'resultados','Enem_Report.pdf'),"wb") as f:
            pdf.write(f)
        print("Congratulations! You have successfully created your personal YouTube report!")
        if sys.platform == "win32":
            os.startfile(os.path.join(os.getcwd(),'resultados','Enem_Report.pdf'))
        elif sys.platform == "darwin":
            subprocess.call(["open", "Enem_Report.pdf"])
        elif which("xdg-open") is not None:
            subprocess.call(["xdg-open", "Enem_Report.pdf"])
        else:
            print("No opener found for your platform. Just open Enem_Report.pdf.")
            
    def executar(dc):
        z = Visualization()
        dic = z.retornaDicionarioHabilidades(dc)
        z.bar(dic)
        with open(os.path.join(os.getcwd(),'config','media_erros.json'), 'r') as lp:
             a = json.load(lp)

        z.errosAlunoxBase(a,dc,'ch')
        z.gen_wordcloud(dc.keys())
        z.gen_pdf()
