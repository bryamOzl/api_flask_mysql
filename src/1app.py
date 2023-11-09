from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

from config import config


app = Flask(__name__)

conexion = MySQL(app)


@app.route('/cursos')
def listar_cursos():
    try:
        cursor = conexion.connect.cursor()
        sql = 'SELECT codigo, nombre , creditos FROM curso'
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursos = []
        for fila in datos:
            curso = {
                'codigo': fila[0],
                'nombre': fila[1],
                'creditos': fila[2]
            }
            cursos.append(curso)
        return jsonify({'cursos': cursos, 'memsaje': 'Crusos listados.'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error %s' % ex})


@app.route('/cursos/<codigo>', methods=['GET'])
def leer_curso(codigo):
    try:
        cursor = conexion.connect.cursor()
        sql = "SELECT codigo, nombre, creditos FROM curso WHERE codigo = '{0}'".format(
            codigo)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            curso = {
                'codigo': datos[0],
                'nombre': datos[1],
                'creditos': datos[2]
            }
            return jsonify({'curso': curso, 'mensaje': 'Curso leido.'})
        else:
            return jsonify({'mensaje': 'Curso no encontrado.'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error %s' % ex})


@app.route('/cursos', methods=['POST'])
def registrar_curso():
    try:
        if request.json != None:
            codigo = request.json['codigo']
            nombre = request.json['nombre']
            creditos = request.json['creditos']
            if conexion.connection is not None:
                cursor = conexion.connection.cursor()
                # Resto del código que utiliza el cursor
                sql = "INSERT INTO curso (codigo, nombre, creditos) VALUES ('{0}','{1}',{2})".format(
                    codigo, nombre, creditos)
                cursor.execute(sql)
                conexion.connection.commit()
                return jsonify({'mensaje': 'Curso registrado.'})
            else:
                return jsonify({'mensaje': 'Error: La conexión no se ha establecido correctamente.'}), 500
                # print("Error: La conexión no se ha establecido correctamente.")
        else:
            return jsonify({'mensaje': 'No se envian datos.'}), 500
    except Exception as ex:
        return jsonify({'mensaje': 'Error %s' % ex}), 500


@app.route('/cursos/<codigo>', methods=['PUT'])
def eliminar_curso(codigo):
    try:
        if conexion.connection is not None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM curso WHERE codigo = '{0}'".format(codigo)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': 'Curso eliminado.'})
        else:
            return jsonify({'mensaje': 'Error: La conexión no se ha establecido correctamente.'}), 500
    except Exception as ex:
        return jsonify({'mensaje': 'Error %s' % ex}), 500


def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
