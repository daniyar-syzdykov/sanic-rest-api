from marshmallow import Schema, fields


class TransactionSchema(Schema):
    id = fields.Integer(required=True)
    transfered = fields.Integer(required=True)
    uuid = fields.UUID(required=True)
    bill_id = fields.Integer(required=True)


class BillSchema(Schema):
    id = fields.Integer()
    balance = fields.Integer()
    user_id = fields.Integer()
    transactions = fields.List(fields.Nested(TransactionSchema, required=True))


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String(required=True)
    uuid = fields.UUID()
    is_active = fields.Boolean()
    is_admin = fields.Boolean()
    bills = fields.List(fields.Nested(
        BillSchema))
    refresh_token = fields.String()


class UserRegisterSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class UserAuthSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    uuid = fields.UUID()



class ProductSchema(Schema):
    id = fields.Integer(required=True)
    uuid = fields.UUID(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    price = fields.Float(required=True)


user_schema = UserSchema()
user_register_schema = UserRegisterSchema()
bill_schema = BillSchema()
transaction_schema = TransactionSchema()
product_schema = ProductSchema()
user_auth_schema = UserAuthSchema()
