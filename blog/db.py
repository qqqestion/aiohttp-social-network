import sqlalchemy as sa


from datetime import datetime

from sqlalchemy.sql.ddl import CreateTable

metadata = sa.MetaData()


def parse_columns(table, value_to_parse):
    return {column.name: value for column, value in zip(table.columns, value_to_parse.values())}


users = sa.Table(
    'users', metadata,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('first_name', sa.String(32), nullable=False),
    sa.Column('last_name', sa.String(32), nullable=False),
    sa.Column('email', sa.String(256), nullable=False),
    sa.Column('password', sa.String(256), nullable=False),
    sa.Column('is_superuser', sa.Boolean, nullable=False,
              server_default='FALSE'),
    sa.Column('is_deleted', sa.Boolean, nullable=False,
              server_default='FALSE'),
    sa.Column('image', sa.String, default='default.jpg'),

    # indices
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key'),
)
# CreateTable(users)
# print(CreateTable(users))


posts = sa.Table(
    'posts', metadata,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('user_id', sa.Integer, nullable=False),
    sa.Column('title', sa.String(64), nullable=False),
    sa.Column('content', sa.String(2048), nullable=False),
    sa.Column('posted_at', sa.DateTime, default=datetime.now, nullable=False),

    # indices
    sa.PrimaryKeyConstraint('id', name='post_pkey'),
    sa.ForeignKeyConstraint(['user_id'], [users.c.id],
                            name='user_post_fkey',
                            ondelete='CASCADE'),
)


permissions = sa.Table(
    'permissions', metadata,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('user_id', sa.Integer, nullable=False),
    sa.Column('perm_name', sa.String(64), nullable=False),

    # indices
    sa.PrimaryKeyConstraint('id', name='permission_pkey'),
    sa.ForeignKeyConstraint(['user_id'], [users.c.id],
                            name='user_permission_fkey',
                            ondelete='CASCADE'),
)
