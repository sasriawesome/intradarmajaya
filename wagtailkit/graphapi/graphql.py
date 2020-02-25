import graphene


class GraphqlSchema(object):
    _queries = []
    _mutations = []
    _matrix = {}

    def __init__(self):
        pass

    def register_query(self, klass):
        self._queries.append(klass)

    def register_mutation(self, klass):
        self._mutations.append(klass)

    def get_query(self):
        """ Generate Query on the fly"""
        if not self._queries:
            self._queries.append(graphene.ObjectType)
        query = type('Query', tuple(self._queries), {})
        return query

    def get_mutation(self):
        """ Generate Mutation on the fly"""
        if not self._mutations:
            self._mutations.append(graphene.ObjectType)
        mutation = type('Mutation', tuple(self._mutations), {})
        return mutation

    def get_schema(self):
        if self._mutations:
            self._matrix.setdefault('mutation', self.get_mutation())
        if self._queries:
            self._matrix.setdefault('query',self.get_query())
        return graphene.Schema(**self._matrix)


graphql_schema = GraphqlSchema()
