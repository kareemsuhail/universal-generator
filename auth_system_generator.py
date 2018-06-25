import os
def generate_auth_system(schema):
    auth_literal = """from django.contrib.auth import get_user_model

import graphene
import graphql_jwt
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        only_fields = ("username","email")


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
class Query(graphene.ObjectType):
    pass
"""
    auth_sys_file = open(os.path.join(os.getcwd(), "./{}/{}/graphql/auth/auth.py".format(
            schema['project_title'], schema['main_app'])), "w+")
    auth_sys_file.write(auth_literal)
    auth_sys_file.close()
