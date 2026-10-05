"""
Capa de servicios del motor narrativo.
Historia original: "El Secreto de la Mina de Cristal Dormido".

Toda la logica de ramificacion, validacion de inventario y seleccion de
textos vive aqui. El router solo recibe el JSON y atrapa errores.
"""

# Cada nodo tiene:
#   texto    -> lo que lee el jugador al llegar
#   final    -> True si es un final (no hay mas decisiones)
#   opciones -> {letra: {descripcion, destino, [requiere], [destino_fallo], [otorga]}}
MAPA_HISTORIA_LOTE = {
    "inicio": {
        "texto": (
            "Llegas a Brumaluz, una aldea cubierta de niebla. Los vecinos dicen que "
            "la vieja mina de cristal despierta cada noche y que nadie vuelve de ella. "
            "Frente a ti hay una caseta abandonada y, al fondo, la entrada de la mina."
        ),
        "final": False,
        "opciones": {
            "A": {"descripcion": "Revisar la caseta del guardia", "destino": "caseta_guardia"},
            "B": {"descripcion": "Ir directo a la entrada de la mina", "destino": "entrada_mina"},
        },
    },
    "caseta_guardia": {
        "texto": (
            "Dentro de la caseta encuentras un tablero con dos objetos: una llave de "
            "cobre cubierta de verdin y un farol de aceite que aun tiene combustible. "
            "Solo alcanzas a llevarte uno antes de que la niebla cierre la puerta."
        ),
        "final": False,
        "opciones": {
            "A": {
                "descripcion": "Tomar la llave de cobre",
                "destino": "entrada_mina",
                "otorga": "llave_de_cobre",
            },
            "B": {
                "descripcion": "Tomar el farol de aceite",
                "destino": "entrada_mina",
                "otorga": "farol_de_aceite",
            },
        },
    },
    "entrada_mina": {
        "texto": (
            "Ante ti se alza una reja de hierro con una cerradura de cobre. "
            "Del otro lado se escucha un zumbido suave, como si el cristal respirara."
        ),
        "final": False,
        "opciones": {
            "A": {
                "descripcion": "Abrir la reja",
                "destino": "galeria_cristales",
                "requiere": "llave_de_cobre",
                "destino_fallo": "final_reja_cerrada",
            },
            "B": {"descripcion": "Regresar a la aldea", "destino": "final_huida"},
        },
    },
    "galeria_cristales": {
        "texto": (
            "La reja cede con un chirrido. Una galeria de cristales opacos se pierde "
            "hacia las profundidades. Mas alla de la luz de la entrada, todo es negro."
        ),
        "final": False,
        "opciones": {
            "A": {
                "descripcion": "Adentrarte por el tunel oscuro",
                "destino": "camara_cristal",
                "requiere": "farol_de_aceite",
                "destino_fallo": "final_perdido_oscuridad",
            },
            "B": {"descripcion": "Volver a la entrada", "destino": "entrada_mina"},
        },
    },
    "camara_cristal": {
        "texto": (
            "Tu farol revela una camara enorme. En el centro late el Cristal Dormido, "
            "y una voz tenue te pide que lo dejes descansar. Sus destellos prometen "
            "riquezas a quien se lo lleve."
        ),
        "final": False,
        "opciones": {
            "A": {"descripcion": "Cubrir el cristal y dejarlo dormir", "destino": "final_guardian_cristal"},
            "B": {"descripcion": "Arrancar el cristal para venderlo", "destino": "final_tesoro_maldito"},
        },
    },
    # ---------------- FINALES ----------------
    "final_guardian_cristal": {
        "texto": (
            "FINAL 1 - GUARDIAN DE BRUMALUZ: El cristal se calma y la niebla se disipa. "
            "La aldea te nombra su guardian y la mina vuelve a dormir en paz."
        ),
        "final": True,
        "opciones": {},
    },
    "final_tesoro_maldito": {
        "texto": (
            "FINAL 2 - TESORO MALDITO: Al arrancar el cristal, la mina se derrumba. "
            "Sales con una fortuna... pero la niebla te sigue para siempre."
        ),
        "final": True,
        "opciones": {},
    },
    "final_perdido_oscuridad": {
        "texto": (
            "FINAL 3 - PERDIDO EN LA OSCURIDAD: Sin luz, el tunel te traga. "
            "Tus pasos se pierden y la mina suma una historia mas a su leyenda."
        ),
        "final": True,
        "opciones": {},
    },
    "final_reja_cerrada": {
        "texto": (
            "FINAL 4 - LA REJA CERRADA: Sin la llave de cobre, la reja no cede. "
            "Al amanecer la niebla te devuelve a la aldea sin respuestas."
        ),
        "final": True,
        "opciones": {},
    },
    "final_huida": {
        "texto": (
            "FINAL 5 - EL QUE HUYO: Decides que la mina no es asunto tuyo. "
            "Vuelves a casa y nunca sabras que dormia bajo la montana."
        ),
        "final": True,
        "opciones": {},
    },
}

NODO_INICIAL = "inicio"


def _formatear_opciones(nodo: dict) -> dict:
    return {letra: datos["descripcion"] for letra, datos in nodo["opciones"].items()}


def _construir_respuesta(id_partida, nombre_nodo: str, inventario: list) -> dict:
    nodo = MAPA_HISTORIA_LOTE[nombre_nodo]
    return {
        "id_partida": id_partida,
        "nodo_actual": nombre_nodo,
        "texto": nodo["texto"],
        "opciones": _formatear_opciones(nodo),
        "inventario": inventario,
        "es_final": nodo["final"],
    }


def obtener_nodo_inicial(id_partida) -> dict:
    """Devuelve el nodo de arranque para mostrar la primera escena."""
    return _construir_respuesta(id_partida, NODO_INICIAL, [])


def avanzar_motor_narrativo(
    id_partida, nodo_actual: str, decision_usuario: str, inventario: list
) -> dict:
    # 1. Validacion de nodo
    if nodo_actual not in MAPA_HISTORIA_LOTE:
        raise ValueError(f"El nodo '{nodo_actual}' no existe en la historia.")

    nodo = MAPA_HISTORIA_LOTE[nodo_actual]

    if nodo["final"]:
        raise ValueError("La historia ya termino: este nodo es un final.")

    decision = decision_usuario.strip().upper()
    if decision not in nodo["opciones"]:
        raise ValueError(
            f"La decision '{decision_usuario}' no es valida en el nodo '{nodo_actual}'. "
            f"Opciones: {list(nodo['opciones'].keys())}"
        )

    opcion = nodo["opciones"][decision]
    nuevo_inventario = list(inventario)  # copia para no mutar la entrada

    # 2. Validacion de restricciones (logica condicional)
    objeto_requerido = opcion.get("requiere")
    if objeto_requerido and objeto_requerido not in nuevo_inventario:
        destino = opcion["destino_fallo"]
        return _construir_respuesta(id_partida, destino, nuevo_inventario)

    # 3. Actualizacion de estado
    objeto_nuevo = opcion.get("otorga")
    if objeto_nuevo and objeto_nuevo not in nuevo_inventario:
        nuevo_inventario.append(objeto_nuevo)

    # 4. Respuesta narrativa
    return _construir_respuesta(id_partida, opcion["destino"], nuevo_inventario)
