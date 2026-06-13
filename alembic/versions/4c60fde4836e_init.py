"""init

Revision ID: 4c60fde4836e
Revises:
Create Date: 2026-06-12 20:27:26.627617

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
from src.app.core.constants import (
    SEED_ADMIN_EMAIL,
    SEED_ADMIN_FULL_NAME,
    SEED_ADMIN_PASSWORD_HASH,
    SEED_USER_EMAIL,
    SEED_USER_FULL_NAME,
    SEED_USER_PASSWORD_HASH,
)

# revision identifiers, used by Alembic.
revision: str = '4c60fde4836e'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_admin', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('balance', sa.Numeric(precision=12, scale=2), server_default='0', nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.CheckConstraint('balance >= 0', name='ck_accounts_balance_non_negative'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_accounts_user_id'), 'accounts', ['user_id'], unique=False)
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('transaction_id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.CheckConstraint('amount > 0', name='ck_payments_amount_positive'),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_payments_account_id'), 'payments', ['account_id'], unique=False)
    op.create_index(op.f('ix_payments_transaction_id'), 'payments', ['transaction_id'], unique=True)
    op.create_index(op.f('ix_payments_user_id'), 'payments', ['user_id'], unique=False)

    user_table = sa.table(
        'users',
        sa.column('id', sa.Integer),
        sa.column('email', sa.String),
        sa.column('full_name', sa.String),
        sa.column('hashed_password', sa.String),
        sa.column('is_admin', sa.Boolean),
        sa.column('is_active', sa.Boolean),
    )
    account_table = sa.table(
        'accounts',
        sa.column('id', sa.Integer),
        sa.column('user_id', sa.Integer),
        sa.column('balance', sa.Numeric),
    )

    op.bulk_insert(
        user_table,
        [
            {
                'id': 1,
                'email': SEED_USER_EMAIL,
                'full_name': SEED_USER_FULL_NAME,
                'hashed_password': SEED_USER_PASSWORD_HASH,
                'is_admin': False,
                'is_active': True,
            },
            {
                'id': 2,
                'email': SEED_ADMIN_EMAIL,
                'full_name': SEED_ADMIN_FULL_NAME,
                'hashed_password': SEED_ADMIN_PASSWORD_HASH,
                'is_admin': True,
                'is_active': True,
            },
        ],
    )
    op.bulk_insert(
        account_table,
        [
            {
                'id': 1,
                'user_id': 1,
                'balance': 0,
            }
        ],
    )

    op.execute(
        "SELECT setval(pg_get_serial_sequence('users', 'id'), (SELECT COALESCE(MAX(id), 1) FROM users), true)"
    )
    op.execute(
        "SELECT setval(pg_get_serial_sequence('accounts', 'id'), (SELECT COALESCE(MAX(id), 1) FROM accounts), true)"
    )
    op.execute(
        "SELECT setval(pg_get_serial_sequence('payments', 'id'), (SELECT COALESCE(MAX(id), 1) FROM payments), true)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_payments_user_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_transaction_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_account_id'), table_name='payments')
    op.drop_table('payments')
    op.drop_index(op.f('ix_accounts_user_id'), table_name='accounts')
    op.drop_table('accounts')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
