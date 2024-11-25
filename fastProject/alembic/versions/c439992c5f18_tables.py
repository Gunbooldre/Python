"""tables

Revision ID: c439992c5f18
Revises: 6a7294748d31
Create Date: 2024-11-25 15:01:17.773410

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c439992c5f18'
down_revision: Union[str, None] = '6a7294748d31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.add_column('posts', sa.Column('title', sa.String(), nullable=False))
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='True', nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    op.drop_column('posts', 'Title')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('Title', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'content')
    op.drop_column('posts', 'title')
    op.create_table('orders',
    sa.Column('order_id', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('customer_id', sa.NullType(), autoincrement=False, nullable=True),
    sa.Column('employee_id', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.Column('order_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('required_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('shipped_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('ship_via', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.Column('freight', sa.REAL(), autoincrement=False, nullable=True),
    sa.Column('ship_name', sa.VARCHAR(length=40), autoincrement=False, nullable=True),
    sa.Column('ship_address', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
    sa.Column('ship_city', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('ship_region', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('ship_postal_code', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('ship_country', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], name='fk_orders_customers'),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.employee_id'], name='fk_orders_employees'),
    sa.ForeignKeyConstraint(['ship_via'], ['shippers.shipper_id'], name='fk_orders_shippers'),
    sa.PrimaryKeyConstraint('order_id', name='pk_orders'),
    postgresql_ignore_search_path=False
    )
    op.create_table('product',
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('is_sale', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.Column('intentory', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='product_pkey')
    )
    op.create_table('shippers',
    sa.Column('shipper_id', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('company_name', sa.VARCHAR(length=40), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=24), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('shipper_id', name='pk_shippers'),
    postgresql_ignore_search_path=False
    )
    op.create_table('categories',
    sa.Column('category_id', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('category_name', sa.VARCHAR(length=15), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('picture', postgresql.BYTEA(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('category_id', name='pk_categories'),
    postgresql_ignore_search_path=False
    )
    op.create_table('customers',
    sa.Column('customer_id', sa.NullType(), autoincrement=False, nullable=False),
    sa.Column('company_name', sa.VARCHAR(length=40), autoincrement=False, nullable=False),
    sa.Column('contact_name', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('contact_title', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
    sa.Column('city', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('region', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('postal_code', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('country', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(length=24), autoincrement=False, nullable=True),
    sa.Column('fax', sa.VARCHAR(length=24), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('customer_id', name='pk_customers'),
    postgresql_ignore_search_path=False
    )
    op.create_table('region',
    sa.Column('region_id', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('region_description', sa.NullType(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('region_id', name='pk_region'),
    postgresql_ignore_search_path=False
    )
    op.create_table('employee_territories',
    sa.Column('employee_id', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('territory_id', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.employee_id'], name='fk_employee_territories_employees'),
    sa.ForeignKeyConstraint(['territory_id'], ['territories.territory_id'], name='fk_employee_territories_territories'),
    sa.PrimaryKeyConstraint('employee_id', 'territory_id', name='pk_employee_territories')
    )
    op.create_table('territories',
    sa.Column('territory_id', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('territory_description', sa.NullType(), autoincrement=False, nullable=False),
    sa.Column('region_id', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['region_id'], ['region.region_id'], name='fk_territories_region'),
    sa.PrimaryKeyConstraint('territory_id', name='pk_territories')
    )
    op.create_table('us_states',
    sa.Column('state_id', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('state_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('state_abbr', sa.VARCHAR(length=2), autoincrement=False, nullable=True),
    sa.Column('state_region', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('state_id', name='pk_usstates')
    )
    op.create_table('order_details',
    sa.Column('order_id', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('product_id', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('unit_price', sa.REAL(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('discount', sa.REAL(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], name='fk_order_details_orders'),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], name='fk_order_details_products'),
    sa.PrimaryKeyConstraint('order_id', 'product_id', name='pk_order_details')
    )
    op.create_table('employees',
    sa.Column('employee_id', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('title_of_courtesy', sa.VARCHAR(length=25), autoincrement=False, nullable=True),
    sa.Column('birth_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('hire_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
    sa.Column('city', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('region', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('postal_code', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('country', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('home_phone', sa.VARCHAR(length=24), autoincrement=False, nullable=True),
    sa.Column('extension', sa.VARCHAR(length=4), autoincrement=False, nullable=True),
    sa.Column('photo', postgresql.BYTEA(), autoincrement=False, nullable=True),
    sa.Column('notes', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('reports_to', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.Column('photo_path', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['reports_to'], ['employees.employee_id'], name='fk_employees_employees'),
    sa.PrimaryKeyConstraint('employee_id', name='pk_employees')
    )
    op.create_table('customer_customer_demo',
    sa.Column('customer_id', sa.NullType(), autoincrement=False, nullable=False),
    sa.Column('customer_type_id', sa.NullType(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], name='fk_customer_customer_demo_customers'),
    sa.ForeignKeyConstraint(['customer_type_id'], ['customer_demographics.customer_type_id'], name='fk_customer_customer_demo_customer_demographics'),
    sa.PrimaryKeyConstraint('customer_id', 'customer_type_id', name='pk_customer_customer_demo')
    )
    op.create_table('products',
    sa.Column('product_id', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('product_name', sa.VARCHAR(length=40), autoincrement=False, nullable=False),
    sa.Column('supplier_id', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.Column('category_id', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.Column('quantity_per_unit', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('unit_price', sa.REAL(), autoincrement=False, nullable=True),
    sa.Column('units_in_stock', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.Column('units_on_order', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.Column('reorder_level', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.Column('discontinued', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.category_id'], name='fk_products_categories'),
    sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.supplier_id'], name='fk_products_suppliers'),
    sa.PrimaryKeyConstraint('product_id', name='pk_products')
    )
    op.create_table('suppliers',
    sa.Column('supplier_id', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('company_name', sa.VARCHAR(length=40), autoincrement=False, nullable=False),
    sa.Column('contact_name', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('contact_title', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
    sa.Column('city', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('region', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('postal_code', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('country', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(length=24), autoincrement=False, nullable=True),
    sa.Column('fax', sa.VARCHAR(length=24), autoincrement=False, nullable=True),
    sa.Column('homepage', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('supplier_id', name='pk_suppliers')
    )
    op.create_table('customer_demographics',
    sa.Column('customer_type_id', sa.NullType(), autoincrement=False, nullable=False),
    sa.Column('customer_desc', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('customer_type_id', name='pk_customer_demographics')
    )
    op.drop_table('votes')
    op.drop_table('users')
    # ### end Alembic commands ###
