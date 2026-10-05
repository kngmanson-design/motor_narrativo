from fastapi import APIRouter, HTTPException

from schemas import PeticionHistoria, RespuestaHistoria
import services

router = APIRouter(prefix="/historia", tags=["Historia"])


@router.get("/inicio/{id_partida}", response_model=RespuestaHistoria)
def iniciar_historia(id_partida: str):
    return services.obtener_nodo_inicial(id_partida)


@router.post("/avanzar", response_model=RespuestaHistoria)
def avanzar(peticion: PeticionHistoria):
    try:
        return services.avanzar_motor_narrativo(
            peticion.id_partida,
            peticion.nodo_actual,
            peticion.decision_usuario,
            peticion.inventario,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del motor narrativo.")
