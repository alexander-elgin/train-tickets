import graphene

import destinations.schema


class Mutation(
    destinations.schema.Mutation,
    graphene.ObjectType,
):
    pass


class Query(
    destinations.schema.Query,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
