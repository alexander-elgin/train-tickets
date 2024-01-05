import graphene
import graphql_jwt

import destinations.schema
import trips.schema


class Mutation(
    destinations.schema.Mutation,
    trips.schema.Mutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(
    destinations.schema.Query,
    trips.schema.Query,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
