import datetime
import smtplib
import RSS.transform_rss
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY


def juntar_datos(diccionario_noticias):
    TEXTO = ""
    lista_todas_las_noticias = list()
    lista_contenido = list()
    for fuente in diccionario_noticias.keys():
        # Se ordena la lista de noticias respectiva a cada fuente según su
        # puntaje
        lista_links_noticias = list()
        for noticia in diccionario_noticias[fuente]:
            # Se revisa si la noticia no está repetida
            if noticia["link"] not in lista_links_noticias:
                lista_links_noticias.append(noticia["link"])
                lista_todas_las_noticias.append(noticia)
    lista_ordenada_todas_las_noticias = sorted(lista_todas_las_noticias,
                                               key=lambda k: int(k['puntaje']))
    top_noticias = [n for n in lista_ordenada_todas_las_noticias if n[
        'puntaje'] > 0]
    temas_ejes = ["DLT", "Criptoactivos", "Ciberseguridad",
                  "Pagos Digitales", "Monitoreo Tecnológico", "Big Data"
        , "CBDC", "Banca Abierta", "Otro"]
    lista_links_noticias_incluidas = list()
    for eje in temas_ejes:
        TEXTO += (str(eje) + "\n" + "\n")
        lista_contenido.append(eje)
        indice_lista_top = 0
        for noticia in top_noticias:
            if noticia["tema"] == eje and noticia["link"] not in \
                    lista_links_noticias_incluidas:
                del top_noticias[indice_lista_top]
                lista_links_noticias_incluidas.append(noticia["link"])
                TEXTO += noticia["titulo"] + " {" + noticia["estadisticas"] + \
                         "}" + "\n" +noticia["link"] + "\n" + \
                         str(noticia["puntaje"]) + "\n" + "\n"
                lista_contenido.append(noticia["titulo"] + " {" + noticia["estadisticas"] + \
                         "}")
                lista_contenido.append(noticia["link"])
            indice_lista_top += 1
    if len(top_noticias) > 0:
        for noticia in top_noticias:
            TEXTO += (noticia["titulo"] + " {" +
                                            noticia[
                                                "estadisticas"] + "} " + "\n" +
                                            noticia[
                                                "link"] + "\n" + str(
                noticia["puntaje"]) + "\n" + "\n")
            lista_contenido.append(noticia["titulo"] + " {" +
                                            noticia[
                                                "estadisticas"] + "} ")
            lista_contenido.append(noticia["link"])
    return TEXTO, lista_contenido

def enviar_mail(contenido):
    SERVER = ""
    FROM = "mmingo@bcch.local"
    TO = ["lsanz@bcentral.cl", "mamusa@bcentral.cl"]
    SUBJECT = "Noticias {}".format(datetime.datetime.now().date())
    message = """From: {}\r\nTo: {}\r\nSubject: {}\r\n

    {}
    """.format(FROM, ",".join(TO), SUBJECT, contenido)
    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, message)


def escribir_pdf(lista_contenido):
    doc = SimpleDocTemplate("Noticias {}.pdf".format(datetime.datetime.now().date()), pagesize=letter)
    width, height = letter
    Story = []
    logo = "logo_bcch.png"
    im = Image(logo, inch, inch)
    Story.append(im)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    titulo = "Noticias {}".format(datetime.datetime.now().date())
    ptext = '<font size=12>%s</font>'%titulo
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    for linea in lista_contenido:
        ptext = '<font size=12>%s</font>'%linea
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
    doc.build(Story)


def crear_txt(contenido):
    """FUNCIÓN QUE ESCRIBE EN UN DOCUMENTO .txt LAS MEJORES NOTICIAS DEL DÍA"""
    with open("Recopilaciones/{}.txt".format(datetime.datetime.now().date()),
              "w") as recopilacion_del_dia_file:
        recopilacion_del_dia_file.write(contenido)

def load_todo():
    diccionario_fuentes_noticias_rss = RSS.transform_rss.transformar()
    contenido, lista_contenido = juntar_datos(diccionario_fuentes_noticias_rss)
    escribir_pdf(lista_contenido)
    crear_txt(contenido)

