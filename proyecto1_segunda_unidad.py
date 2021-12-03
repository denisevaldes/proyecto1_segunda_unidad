import json
# Se importa la librería Gobject Instrospection (gi)
import gi
# Selecciona que la versión de GTK a trabajar (3.0)
gi.require_version("Gtk", "3.0")
# Importa Gtk
from gi.repository import Gtk

#funcion abrir el archivo json
def open_file(fichero):
    try:
        with open(fichero, 'r') as archivo:
            data = json.load(archivo)
    except IOError:#si no encuentra un fichero crea uno
        data = {"impresiones":[], "stickers":[], "cuadernos":[]}
    return data

#funcion guardar el archivo y el return del fichero = data 
def save_file(data,fichero):
    """Guarda los datos en un archivo json."""

    # guardamos en modo escritura
    with open(fichero, "w") as archivo:
        json.dump(data, archivo, indent=4)


#se crea clase de ventana de inicio 
class ventana_inicio:
    def __init__(self):
        self.builder = Gtk.Builder()
        #se selecciona archivo.ui del que se extrae la interfaz
        self.builder.add_from_file("proyecto1.ui")
        #se crea ventana principal
        ventana = self.builder.get_object("ventana_principal")
        ventana.set_default_size(850, 650)
        ventana.set_title("archivos")
        ventana.connect("destroy", Gtk.main_quit)
        #se crea boton, el cual abrira otra pestaña en donde 
        #se podrá elegir que se desea cotizar
        boton_cotizar = self.builder.get_object("boton_cotizar")
        boton_cotizar.set_label("cotizar")
        boton_cotizar.connect("clicked", self.botoncotizar)
        boton_cotizaciones = self.builder.get_object("boton_cotizaciones")
        boton_cotizaciones.connect("clicked", self.botoncotizaciones)

        ventana.show_all()
    #se crean funciones que serviran para llamar a diferentes clases
    def botoncotizar(self, btn= None):
        ventanadialogo = ventana_opciones_cotizar()
    
    def botoncotizaciones(self,btn=None):
        ventanacotizaciones = ver_cotizaciones()

#clase de ventana con opciones de cotizacion
class ventana_opciones_cotizar:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("proyecto1.ui")
        #se llama a la ventana de opciones de cotizacion
        self.ventanadialogo = self.builder.get_object("ventana_cotizar")

        self.ventanadialogo.set_default_size(850, 650)
        self.ventanadialogo.set_title("archivos")

        self.ventanadialogo.show_all()
        #se llama a botones, los cuales abriran nuevas pestañas 
        boton_impresion = self.builder.get_object("boton_impresion")
        boton_impresion.set_label("cotizar impresion")
        boton_impresion.connect("clicked", self.botonimprimir)

        boton_cuaderno = self.builder.get_object("btncotizar_cuaderno")
        boton_cuaderno.set_label("cotizar cuaderno")
        boton_cuaderno.connect("clicked", self.botoncuaderno)

        boton_stickers = self.builder.get_object("btncotizar_stickers")
        boton_stickers.set_label("cotizar stickers")
        boton_stickers.connect("clicked", self.botonstickers)

    #funciones encargadas de llamar a distintas clases 
    def botonimprimir(self, btn= None):
        ventanaimprimir = ventana_imprimir()

    def botoncuaderno(self, btn = None):
        ventanacuaderno = ventana_cotizar_cuaderno()

    def botonstickers(self, btn = None):
        ventanastickers = ventana_cotizar_stickers()


#clase de ventana encargada de cotizar stickers
class ventana_cotizar_stickers:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("proyecto1.ui")
        #se llama a ventana de cotizacion de estickers
        self.ventanacuadernos = self.builder.get_object("ventana_stickers")
        self.ventanacuadernos.set_default_size(850, 650)
        self.ventanacuadernos.set_title("cotizacion de stickers")
        self.ventanacuadernos.show_all()

        #se le da un nombre a los diferentes label en la pestaña
        self.label_numstickers = self.builder.get_object("numero_stickers")
        self.label_numstickers.set_label("Numero de stickers requerido: ")
        self.label_tamaño_stickers = self.builder.get_object("tamaño_stickers")
        self.label_tamaño_stickers.set_label("tamaño de stickers: ")
        self.label_total_stickers = self.builder.get_object("total_stickers")
        self.label_total_stickers.set_label("Total: ")
        self.total_stickers = self.builder.get_object("total_pegatina")
        self.total_stickers.set_label("")

        #se llama a entrada en donde se ponda el numero de stickers necesitados
        self.entrada_numero_stickers= self.builder.get_object("entrada_numero_stickers")
        #se llama a botones y se le conecta una función 
        self.btncotizar_stickers = self.builder.get_object("btn_cotizar_stickers")
        self.btncotizar_stickers.connect("clicked", self.boton_sticker_cotizar)
        self.btnguardar_cotizar = self.builder.get_object("guardar_stickers")
        self.btnguardar_cotizar.connect("clicked",self.boton_guardar_cotizacion)
        #se llama a comboboxtext
        self.eleccion_tamaño_stickers = self.builder.get_object("eleccion_tamaño")
        #se crea lista, esta ira dentro de combobox llamado self.eleccion_tamaño_stickers
        lista_gramaje = ["seleccione una opción",
                         "3x3 cm",
                         "5x5 cm",
                         "10x10 cm"]
        
        #se añaden los elementos de la lista a comboboxtext
        for item in lista_gramaje:
            self.eleccion_tamaño_stickers.append_text(item)

        #se indica que posición 0 de self.eleccion tamaño este de forma predeterminada
        self.eleccion_tamaño_stickers.set_active(0)
        self.eleccion_tamaño_stickers.connect("changed", self.combobox_eleccion_tamaño)

    #se le da un valor seleccionado de combobox a una variable
    def combobox_eleccion_tamaño(self, cmb=None):
        self.valor_tamaño_stickers = self.eleccion_tamaño_stickers.get_active_text() 

    #se le entrega el numero de stickers requerido a una variable
    def boton_sticker_cotizar(self, enter=None):
        self.texto = self.entrada_numero_stickers.get_text()

        try:
            #se entrega valor de cotizacion, dependiendo de 
            #las elecciones del usuario
            numero_de_stickers = int(float(self.texto))
            if self.valor_tamaño_stickers == "3x3 cm":
                valor_total = numero_de_stickers * 30
            if self.valor_tamaño_stickers == "5x5 cm":
                valor_total = numero_de_stickers * 50
            if self.valor_tamaño_stickers == "10x10 cm":
                valor_total = numero_de_stickers * 60 

            #se entrega valor total como str a label total de stickers
            self.valor_sticker = str(valor_total)
            self.total_stickers.set_text(self.valor_sticker)

        #ante una excepcion de value error se abrira una ventana de advertencia
        except ValueError:
            self.total_stickers.set_text("no se admiten letras, solo numeros")
            ventana_advertencia()

    # funcion que guarda lo cotizado de stickers en un json
    def boton_guardar_cotizacion(self,btn = None):
        self.btncotizar_stickers.clicked()#se llama al boton para que haga lo mismo al momento de guardar
        data = open_file("cotizaciones.json")#abre el "fichero" que esta en la funcion open json
        cotizaciones = {"cantidad de stickers" : str(self.texto),
                        "tamanio" : self.valor_tamaño_stickers,
                        "precio total" : self.valor_sticker}
        if cotizaciones not in data["stickers"]:#if que verifica que no se repitan las cosas 
            data["stickers"].append(cotizaciones)
        save_file(data,"cotizaciones.json")


#clase de ventana encargada de cotizar cuadernos 
class ventana_cotizar_cuaderno:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("proyecto1.ui")
        #se llama ventana de cotizacion de cuadernos
        self.ventanacuadernos = self.builder.get_object("ventana_cuadernos")
        self.ventanacuadernos.set_default_size(850, 650)
        self.ventanacuadernos.set_title("cotizacion de cuadernos personalizados")
        self.ventanacuadernos.show_all()

        #se le añade valor a los diferentes label 
        self.label_numhojas = self.builder.get_object("numero_hojas")
        self.label_numhojas.set_label("Numero de hojas: ")
        self.label_tipodetapa = self.builder.get_object("tipo_tapa")
        self.label_tipodetapa.set_label("Tipo de tapa: ")
        self.label_gramaje_hoja = self.builder.get_object("gramaje_hoja")
        self.label_gramaje_hoja.set_label("Gramaje de hoja: ")
        self.label_total_cuaderno = self.builder.get_object("total_cuaderno")
        self.label_total_cuaderno.set_label("Total: ")
        self.total_cotizacion_cuaderno = self.builder.get_object("total_cotizacion_cuaderno")
        self.total_cotizacion_cuaderno.set_label(" ")
        #se llaman diferentes botones y sus funciones 
        self.btncotizar_cuaderno = self.builder.get_object("btn_cotizar_cuaderno")
        self.btncotizar_cuaderno.connect("clicked", self.boton_cuaderno_clicked)
        self.btnguardar_cotizar = self.builder.get_object("guardar_cuaderno")
        self.btnguardar_cotizar.connect("clicked",self.boton_guardar_cotizacion)

        #se llaman diferentes combobox y se crean listas requeridas 
        self.eleccion_num_hojas = self.builder.get_object("eleccion_numero_hojas")

        #se crea lista para combobox en la cual se eligen las hojas del cuaderno
        lista_numero_hojas = ["Seleccione una opción",
                              "75 hojas",
                              "100 hojas",
                              "180 hojas"]

        #se agregan opciones a combobox
        for item in lista_numero_hojas:
            self.eleccion_num_hojas.append_text(item)

        #se selecciona primera opcion, como opcion predeterminada para combobox
        self.eleccion_num_hojas.set_active(0)
        self.eleccion_num_hojas.connect("changed", self.combobox_hojas_change)


        #se carga combobox para seleccionar tipo de tapa
        self.eleccion_tapa = self.builder.get_object("eleccion_tapa")

        #se crea lista para combobox de eleccion de tapa
        lista_tapas = ["Seleccione una opción",
                              "tapa dura",
                              "tapa blanda"]

        #se agregan opciones a combobox
        for item in lista_tapas:
            self.eleccion_tapa.append_text(item)
        
        #se selecciona primera opcion, como opcion predeterminada para combobox
        self.eleccion_tapa.set_active(0)
        self.eleccion_tapa.connect("changed", self.combobox_tipo_tapa)

        #se crea combobox para elegir gramaje deseado
        self.eleccion_gramaje = self.builder.get_object("eleccion_gramaje")

        #se crea lista para combobox de gramaje
        lista_gramaje = ["seleccione una opción",
                         "70 gramos",
                         "120 gramos",
                         "170 gramos"]
        
        #se agregan elemenos de lista a combobox de gramaje
        for item in lista_gramaje:
            self.eleccion_gramaje.append_text(item)

        #se selecciona primera opcion, como opcion predeterminada para combobox 
        self.eleccion_gramaje.set_active(0)
        self.eleccion_gramaje.connect("changed", self.combobox_gramaje)

    #funciones en donde se le pasa las elecciones a una variable determinada
    def combobox_hojas_change(self, cmb=None):
        self.eleccion_de_num_hojas = self.eleccion_num_hojas.get_active_text() 
        
    def combobox_tipo_tapa(self, cmb=None):
        self.eleccion_de_tapa = self.eleccion_tapa.get_active_text() 

    def combobox_gramaje(self, cmb=None):
        self.eleccion_de_gramaje = self.eleccion_gramaje.get_active_text()      

    #funcion encargada de realizar cotizacion
    def boton_cuaderno_clicked(self, btn = None):
        tapa_blanda = 500
        tapa_dura = 900
        gramos_70 = 15
        gramos_120 = 25 
        gramos_170 = 35

        try:
            #dependiendo de la eleccion del usuario 
            #se crea la cotizacion
            if self.eleccion_de_num_hojas == "75 hojas":
                if self.eleccion_de_tapa == "tapa dura":
                    if self.eleccion_de_gramaje == "70 gramos":
                        valor = (75 * gramos_70) + tapa_dura
                    elif self.eleccion_de_gramaje == "120 gramos":
                        valor = (75 * gramos_120) + tapa_dura
                    elif self.eleccion_de_gramaje == "170 gramos":
                        valor = (75 * gramos_170) + tapa_dura
                elif self.eleccion_de_tapa == "tapa blanda":
                    if self.eleccion_de_gramaje == "70 gramos":
                        valor = (75 * gramos_70) + tapa_blanda
                    elif self.eleccion_de_gramaje == "120 gramos":
                        valor = (75 * gramos_120) + tapa_blanda
                    elif self.eleccion_de_gramaje == "170 gramos":
                        valor = (75 * gramos_170) + tapa_blanda
            elif self.eleccion_de_num_hojas == "100 hojas":
                if self.eleccion_de_tapa == "tapa dura":
                    if self.eleccion_de_gramaje == "70 gramos":
                        valor = (100 * gramos_70) + tapa_dura
                    elif self.eleccion_de_gramaje == "120 gramos":
                        valor = (100 * gramos_120) + tapa_dura
                    elif self.eleccion_de_gramaje == "170 gramos":
                        valor = (100 * gramos_170) + tapa_dura
                elif self.eleccion_de_tapa == "tapa blanda":
                    if self.eleccion_de_gramaje == "70 gramos":
                        valor = (100 * gramos_70) + tapa_blanda
                    elif self.eleccion_de_gramaje == "120 gramos":
                        valor = (100 * gramos_120) + tapa_blanda
                    elif self.eleccion_de_gramaje == "170 gramos":
                        valor = (100 * gramos_170) + tapa_blanda
            elif self.eleccion_de_num_hojas == "180 hojas":
                if self.eleccion_de_tapa == "tapa dura":
                    if self.eleccion_de_gramaje == "70 gramos":
                        valor = (180 * gramos_70) + tapa_dura
                    elif self.eleccion_de_gramaje == "120 gramos":
                        valor = (180 * gramos_120) + tapa_dura
                    elif self.eleccion_de_gramaje == "170 gramos":
                        valor = (180 * gramos_170) + tapa_dura
                elif self.eleccion_de_tapa == "tapa blanda":
                    if self.eleccion_de_gramaje == "70 gramos":
                        valor = (180 * gramos_70) + tapa_blanda
                    elif self.eleccion_de_gramaje == "120 gramos":
                        valor = (180 * gramos_120) + tapa_blanda
                    elif self.eleccion_de_gramaje == "170 gramos":
                        valor = (180 * gramos_170) + tapa_blanda
            
            #se da el valor de la cotizacion a una variable
            self.valor_final = str(valor)
            #se le da el valor de la cotizacion a label total_cotizacion
            self.total_cotizacion_cuaderno.set_text(self.valor_final)

        #se crean excepciones en donde se abrira una ventana de advertencia
        except AttributeError:
            self.total_cotizacion_cuaderno.set_text("debe tener todas las opciones elegidas")
            ventana_advertencia()

        except UnboundLocalError:
            self.total_cotizacion_cuaderno.set_text("debe tener todas las opciones elegidas")
            ventana_advertencia()

    # funcion que guarda lo cotizado de stickers en un json
    def boton_guardar_cotizacion(self,btn = None):
        self.btncotizar_cuaderno.clicked()#se llama al boton para que haga lo mismo al momento de guardar
        data = open_file("cotizaciones.json")#abre el "fichero" que esta en la funcion open json
        cotizaciones = {"cantidad de hojas" : str(self.eleccion_de_num_hojas),
                        "tipo de tapa" : self.eleccion_de_tapa,
                        "gramaje" : self.eleccion_de_gramaje,
                        "valor total" : self.valor_final}
        if cotizaciones not in data["cuadernos"]:#if que verifica en el json para no guardar 2 veces
            data["cuadernos"].append(cotizaciones)
        save_file(data,"cotizaciones.json")

#clase encargada de abrir ventana de cotizacion de impresiones
class ventana_imprimir:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("proyecto1.ui")
        #se abre ventana de cotizacion de impresion
        self.ventanaimprimir = self.builder.get_object("ventana_impresion")
        self.ventanaimprimir.set_default_size(850, 650)
        self.ventanaimprimir.set_title("datos de impresion")
        self.ventanaimprimir.show_all()

        #se llaman botones y sus funciones 
        self.entrada_num_pagina = self.builder.get_object("entrada_pagina")
        self.btncotizar_impresion = self.builder.get_object("btn_cotizar_impresion")
        self.btnguardar_cotizar = self.builder.get_object("boton_guardar_impresion")
        self.btncotizar_impresion.connect("clicked", self.boton_ejemplo_clicked)
        self.btnguardar_cotizar.connect("clicked",self.boton_guardar_cotizacion)
        self.label_valor = self.builder.get_object("valor_total")
        self.label_valor.set_label(" ")
        
        #se crea comboboxtext en el cual se elije el tipo de hoja deseada 
        self.eleccion_hoja = self.builder.get_object("opcion_tipohoja")

        #se crea lista de combobox 
        lista_tipo_hoja = ["seleccione una opcion",
                            "oficio",
                            "carta",
                            "B5",
                            "A4"]
        #se añaden los str de la lista a comboboxtext
        for item in lista_tipo_hoja:
            self.eleccion_hoja.append_text(item)
        
        #se deja primera opcion de combobox como opcion predeterminada 
        self.eleccion_hoja.set_active(0)
        self.eleccion_hoja.connect("changed", self.combobox_eleccion_hoja)

        #se crea combobox de eleccion de color 
        self.eleccion_color = self.builder.get_object("eleccion_color")

        #se crea lista de eleccion de color para combobox
        lista_color = ["Seleccione una opción",
                        "blanco y negro",
                        "color"]

        #se añade item de lista a combobox
        for item in lista_color:
            self.eleccion_color.append_text(item)
        
        #se deja opcion 1 como opcion predeterminada a combobox
        self.eleccion_color.set_active(0)
        self.eleccion_color.connect("changed", self.combobox_color_change)

    #funciones encargadas de darle a una variable la opcion escogida
    def combobox_color_change(self, cmb=None):
        self.valor_color = self.eleccion_color.get_active_text() 

    def combobox_eleccion_hoja(self, cmb=None):
        self.valor_seleccion_hoja = self.eleccion_hoja.get_active_text() 
    
    #se crea cotizacion de impresiones
    def boton_ejemplo_clicked(self, enter=None):
        self.texto = self.entrada_num_pagina.get_text()

        try:
            self.texto = int(float(self.texto))
            #se crea cotizacion dependiendo de las opciones elegidas por usuario
            if self.valor_color == "blanco y negro":
                if self.valor_seleccion_hoja == "oficio":
                    valor = self.texto * 20 
                elif self.valor_seleccion_hoja == "carta":
                    valor = self.texto * 15
                elif self.valor_seleccion_hoja == "B5":
                    valor = self.texto * 10
                elif self.valor_seleccion_hoja == "A4": 
                    valor = self.texto * 17
            if self.valor_color == "color":
                if self.valor_seleccion_hoja == "oficio":
                    valor = self.texto * 30
                elif self.valor_seleccion_hoja == "carta":
                    valor = self.texto * 25
                elif self.valor_seleccion_hoja == "B5":
                    valor = self.texto * 15
                elif self.valor_seleccion_hoja == "A4": 
                    valor = self.texto * 28

            self.valor_final = str(valor)
            self.label_valor.set_text(self.valor_final)

        #se añade un excepcion en donde se abrira una ventana de error 
        #en caso de que usuario no ingrese bien los datos
        except ValueError:
            self.label_valor.set_text("no se admiten letras, solo numeros")
            ventana_advertencia()


    #funcion guardar cotizacion 
    def boton_guardar_cotizacion(self,btn = None):
        self.btncotizar_impresion.clicked()#preciona el boton aceptar ahorrando codigo y cumpliendo la misma funcion
        data = open_file("cotizaciones.json")
        cotizaciones = {"cantidad de hojas" : str(self.texto),
                        "color de hoja" : self.valor_color,
                        "tamanio de hoja" : self.valor_seleccion_hoja,
                        "precio cotizacion impresion" : self.valor_final}
        if cotizaciones not in data["impresiones"]:# if que verifica que no se guarden 2 elementos iguales
            data["impresiones"].append(cotizaciones)
        save_file(data,"cotizaciones.json")
       
#se crea clase de ventana de advertencia
class ventana_advertencia:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("proyecto1.ui")
        #se llama ventana de advertencia
        self.advertencia = self.builder.get_object("ventana_advertencia")
        self.advertencia.set_default_size(200, 200)
        #se le agrega titulo a ventana de advertencia
        self.advertencia.set_title("ERROR")
        #se añade boton para salir 
        self.boton_salir = self.builder.get_object("boton_salir")
        #se añade label y se le añade texto
        self.label_numhojas = self.builder.get_object("label_advertencia")
        self.label_numhojas.set_label("REVISE SUS RESPUESTAS")
        #se llama a funcion de cerrar ventana 
        self.boton_salir.connect("clicked",self.cerrar_ventanta)
        self.advertencia.show_all() 

    #funcion encargada de cerrar ventana
    def cerrar_ventanta(self, btn=None):
        self.advertencia.destroy()


#clase ventana tree que muestra los valores que estan guardados los json


class ver_cotizaciones:
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("proyecto1.ui")
        #abrimos el tree view con id cotizaciones de impresiones realizadas
        self.ver_cotizaciones = builder.get_object("cotizaciones_realizadas")
        self.tree = builder.get_object("cotizaciones_impresiones")
        #entregamos la cantidad de str para crear la lista 
        self.modelo = Gtk.ListStore(str, str, str, str)
        self.tree.set_model(model=self.modelo)

        nombre_columnas = ("cantidad de hojas", "color de hoja", "tamanio de hoja", "precio cotizacion impresion")
        cell = Gtk.CellRendererText()
        #crea una columna para el tree view por cada elemento en nombre_columnas
        for item in range(len(nombre_columnas)):
            column = Gtk.TreeViewColumn(nombre_columnas[item],
                                        cell,
                                        text=item)
            self.tree.append_column(column)

        #entrega la informacion recolectada  y lo guardar en def load_data_from_json(self,tipo_de_pedido):
        self.load_data_from_json("impresiones")
        #abrimos el tree view con id cotizaciones de stickers
        self.tree = builder.get_object("cotizaciones_stickers")
        #se ingresa la cantidad  str para crear variables 
        self.modelo = Gtk.ListStore(str, str, str)
        self.tree.set_model(model=self.modelo)

        nombre_columnas = ("cantidad de stickers", "tamanio", "precio total")
        cell = Gtk.CellRendererText()
        #crea una columna para el tree view por cada elemento en nombre_columnas
        for item in range(len(nombre_columnas)):
            column = Gtk.TreeViewColumn(nombre_columnas[item],
                                        cell,
                                        text=item)
            self.tree.append_column(column)

        #entrega la informacion recolectada  y lo guardar en def load_data_from_json(self,tipo_de_pedido):
        self.load_data_from_json("stickers")


        self.tree = builder.get_object("cotizaciones_cuadernos")
        self.modelo = Gtk.ListStore(str, str, str, str)
        self.tree.set_model(model=self.modelo)

        nombre_columnas = ("cantidad de hojas", "tipo de tapa", "gramaje", "valor total")
        cell = Gtk.CellRendererText()
        #crea una columna para el tree view por cada elemento en nombre_columnas
        for item in range(len(nombre_columnas)):
            column = Gtk.TreeViewColumn(nombre_columnas[item],
                                        cell,
                                        text=item)
            self.tree.append_column(column)

        #entrega la informacion recolectada  y lo guardar en def load_data_from_json(self,tipo_de_pedido):
        self.load_data_from_json("cuadernos")
        
        self.ver_cotizaciones.show_all()

    #funcion guarda los datos en el self.modelo.append(line)
    def load_data_from_json(self,tipo_de_pedido):
        # llamamos al metodo de abrir el archivo
        datos = open_file("cotizaciones.json")
        for item in datos[tipo_de_pedido]:
            # procesa por medio de listas por comprensión
            line = [x for x in item.values()]
            self.modelo.append(line)

        

if __name__ == "__main__":
    ventana_inicio()
    Gtk.main()
