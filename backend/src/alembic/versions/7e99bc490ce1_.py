"""empty message

Revision ID: 7e99bc490ce1
Revises: 
Create Date: 2023-01-06 13:23:59.695378

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils.types.uuid import UUIDType

# revision identifiers, used by Alembic.
revision = '7e99bc490ce1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth_group',
    sa.Column('id', UUIDType(binary=False), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task_group',
    sa.Column('id', UUIDType(binary=False), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', UUIDType(binary=False), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('full_name', sa.String(length=255), nullable=True),
    sa.Column('hashed_password', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('group_id', UUIDType(binary=False), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['auth_group.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('chat_room',
    sa.Column('id', UUIDType(binary=False), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('user_id', UUIDType(binary=False), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('core_cash_flow',
    sa.Column('id', UUIDType(binary=False), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('deadline', sa.DateTime(timezone=True), nullable=True),
    sa.Column('description', sa.String(length=2000), nullable=True),
    sa.Column('value', sa.Float(precision=2), nullable=False),
    sa.Column('type', sa.Enum('entry', 'exit', name='cashflowtype'), nullable=False),
    sa.Column('payment_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_recurring', sa.Boolean(), nullable=False),
    sa.Column('user_id', UUIDType(binary=False), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task',
    sa.Column('id', UUIDType(binary=False), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('user_id', UUIDType(binary=False), nullable=False),
    sa.Column('deadline', sa.DateTime(timezone=True), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('task_group_id', UUIDType(binary=False), nullable=True),
    sa.ForeignKeyConstraint(['task_group_id'], ['task_group.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chat_message',
    sa.Column('id', UUIDType(binary=False), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('room_id', UUIDType(binary=False), nullable=False),
    sa.Column('content', sa.String(length=255), nullable=True),
    sa.Column('user_id', UUIDType(binary=False), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['chat_room.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('list',
    sa.Column('id', UUIDType(binary=False), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('task_id', UUIDType(binary=False), nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('text_line',
    sa.Column('id', UUIDType(binary=False), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('content', sa.String(length=500), nullable=True),
    sa.Column('task_id', UUIDType(binary=False), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('list_text_line',
    sa.Column('id', UUIDType(binary=False), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('content', sa.String(length=500), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('list_id', UUIDType(binary=False), nullable=False),
    sa.ForeignKeyConstraint(['list_id'], ['list.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('list_text_line')
    op.drop_table('text_line')
    op.drop_table('list')
    op.drop_table('chat_message')
    op.drop_table('task')
    op.drop_table('core_cash_flow')
    op.drop_table('chat_room')
    op.drop_table('users')
    op.drop_table('task_group')
    op.drop_table('auth_group')
    # ### end Alembic commands ###