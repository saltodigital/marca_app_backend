class ResponseNC:
    message = "message"
    status = "status"
    data = "data"

class StatusNC:
    ok = "ok"
    fail = "fail"
    data = "data"

MessageNC = {
    'vacio': 'No se encontraron datos', 
    'errorServidor': 'Se presentaron errores de comunicacion con el servidor'
}

meses=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
dias=['31','28','31','30','31','30','31','31','30','31','30','31']