
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.schemas.address import AddressCreateSchema
from models.schemas.address import AddressUpdateSchema
from models.schemas.address import AddressReadSchema

from core.dependencies import get_database, get_address_service
from services import AddressService

address_router = APIRouter(
    prefix="/api/addresses",
    tags=["addresses"],
    responses={404: {"description": "Not found"}},
)


@address_router.post("/", response_model=AddressReadSchema, status_code=status.HTTP_201_CREATED)
async def create_address(
    address_data: AddressCreateSchema,
    session: AsyncSession = Depends(get_database),
    service: AddressService = Depends(get_address_service),
):
    try:
        return await service.CreateAsync(address_data, session=session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@address_router.get("/", response_model=list[AddressReadSchema])
async def get_all_addresses(
    session: AsyncSession = Depends(get_database),
    service: AddressService = Depends(get_address_service),
):
    try:
        return await service.GetAllAsync(session=session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@address_router.get("/{address_id}", response_model=AddressReadSchema)
async def get_address_by_id(
    address_id: str,
    session: AsyncSession = Depends(get_database),
    service: AddressService = Depends(get_address_service),
):
    try:
        dto = await service.GetByIdAsync(address_id, session=session)
        if dto is None:
            raise HTTPException(status_code=404, detail="Address not found")
        return dto
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@address_router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_address(
    id: str,
    address_data: AddressUpdateSchema,
    session: AsyncSession = Depends(get_database),
    service: AddressService = Depends(get_address_service),
):
    try:
        success = await service.UpdateAsync(id, address_data, session=session)
        if not success:
            raise HTTPException(status_code=404, detail="Address not found")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@address_router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    address_id: str,
    session: AsyncSession = Depends(get_database),
    service: AddressService = Depends(get_address_service),
):
    try:
        deleted = await service.DeleteAsync(address_id, session=session)
        if not deleted:
            raise HTTPException(status_code=404, detail="Address not found")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
