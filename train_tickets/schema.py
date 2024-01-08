import graphene
import graphql_jwt

import carriages.schema
import destinations.schema
import payment_gateways.schema
import payments.schema
import routes.schema
import seats.schema
import tickets.schema
import trains.schema
import trips.schema


class Mutation(
    carriages.schema.Mutation,
    destinations.schema.Mutation,
    payment_gateways.schema.Mutation,
    payments.schema.Mutation,
    routes.schema.Mutation,
    seats.schema.Mutation,
    tickets.schema.Mutation,
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
    payment_gateways.schema.Query,
    payments.schema.Query,
    routes.schema.Query,
    seats.schema.Query,
    tickets.schema.Query,
    trains.schema.Query,
    trips.schema.Query,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
