import graphene

import destinations.schema


class Query(
    destinations.schema.Query,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query)
