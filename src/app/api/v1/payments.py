from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.session import get_db_session
from src.app.schemas.payment import (
    PaymentWebhookRequest,
    PaymentWebhookResponse,
    PaymentWebhookStatus,
)
from src.app.services.exceptions import (
    AccountOwnershipError,
    InvalidPaymentSignatureError,
    UserNotFoundError,
)
from src.app.services.payment import PaymentService

router = APIRouter(
    prefix='/payments',
    tags=['payments'],
)


@router.post(
    '/webhook',
    response_model=PaymentWebhookResponse,
)
async def process_webhook(
    payload: PaymentWebhookRequest,
    session: AsyncSession = Depends(get_db_session),
) -> PaymentWebhookResponse:
    try:
        processed, balance = await PaymentService(session).process_webhook(payload)
    except InvalidPaymentSignatureError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from None
    except UserNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from None
    except AccountOwnershipError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from None
    return PaymentWebhookResponse(
        status=(PaymentWebhookStatus.PROCESSED if processed else PaymentWebhookStatus.IGNORED),
        user_id=payload.user_id,
        account_id=payload.account_id,
        balance=balance,
    )
