
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.schemas.order import OrderCreateSchema
from models.schemas.order import OrderUpdateSchema
from models.schemas.order import OrderReadSchema
from models.schemas.order import OrderPatchSchema

from core.dependencies import get_database, get_order_service
from services.order_service_impl import OrderService

order_router = APIRouter(
    prefix="/api/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)


@order_router.post("/", response_model=OrderReadSchema, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreateSchema,
    session: AsyncSession = Depends(get_database),
    service: OrderService = Depends(get_order_service),
):
    try:
        return await service.CreateAsync(data, session=session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@order_router.get("/", response_model=list[OrderReadSchema])
async def get_all_orders(
    session: AsyncSession = Depends(get_database),
    service: OrderService = Depends(get_order_service),
):
    try:
        return await service.GetAllAsync(session=session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@order_router.get("/{id}", response_model=OrderReadSchema)
async def get_order_by_id(
    id: str,
    session: AsyncSession = Depends(get_database),
    service: OrderService = Depends(get_order_service),
):
    try:
        dto = await service.GetByIdAsync(id, session=session)
        if dto is None:
            raise HTTPException(status_code=404, detail="Record not found")
        return dto
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")



@order_router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_order(
    id: str,
    data: OrderUpdateSchema,
    session: AsyncSession = Depends(get_database),
    service: OrderService = Depends(get_order_service),
):
    try:
        success = await service.UpdateAsync(data, session=session)
        if not success:
            raise HTTPException(status_code=404, detail="Record not found")
        return {"message": "Updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")



@order_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    id: str,
    session: AsyncSession = Depends(get_database),
    service: OrderService = Depends(get_order_service),
):
    try:
        deleted = await service.DeleteAsync(id, session=session)
        if not deleted:
            raise HTTPException(status_code=404, detail="Record not found")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")



@order_router.patch("/{id}/status", response_model=OrderReadSchema)
async def patch_order_status(
    id: str,
    data: OrderPatchSchema,
    session: AsyncSession = Depends(get_database),
    service: OrderService = Depends(get_order_service),
):
    try:
        updated = await service.PatchAsync(id, data, session=session)
        if not updated:
            raise HTTPException(status_code=404, detail="Record not found")
        return await service.GetByIdAsync(id, session=session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

