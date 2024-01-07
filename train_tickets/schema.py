import graphene
import graphql_jwt

import carriages.schema
import destinations.schema
import trains.schema
import trips.schema


class Mutation(
    carriages.schema.Mutation,
    destinations.schema.Mutation,
    trains.schema.Mutation,
    trips.schema.Mutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(
    carriages.schema.Query,
    destinations.schema.Query,
    trains.schema.Query,
    trips.schema.Query,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
