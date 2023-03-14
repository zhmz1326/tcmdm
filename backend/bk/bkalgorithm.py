import bk.graph as graph
# Without Pivoting

# in this function, P stands for priority queue, where pending vertices are
# R stands for result set, X stands for checked list
def bron_kerbosch(ADT, R=set(), P=set(), X=set()):
    """Bron Kerbosch algorithm to find maximal cliques"""

    # when we have nothing left in the priority queue and checked list
    # by definition, no extra vertex can be added into the clique
    # therefore, we find a maximal clique
    if not P and not X:
        yield R

    # while we still got vertices in priority queue
    # we pick a random adjacent vertex and add into the clique
    while P:
        v = P.pop()

        # the crucial part of the algorithm is here
        yield from bron_kerbosch(ADT,

                                 # we add a new adjacent vertex into the result set
                                 # trying to expand the clique to the maximal
                                 R=R.union([v]),

                                 # the priority queue is bounded by the rule of adjacency
                                 # a vertex can be added into the priority queue
                                 # if and only if it is neighbor to everyone in the current clique
                                 P=P.intersection(ADT.edge(v)),

                                 # the checked list is bounded by the rule of adjacency as well
                                 # hence, we can minimize the iteration we need
                                 X=X.intersection(ADT.edge(v)))

        # the vertex has been checked
        X.add(v)


# print(list(bron_kerbosch(ADT,P=set(ADT.vertex()))))

# print(list(bron_kerbosch(ADT)))

def bron_kerbosch_pivot(ADT, R=set(), P=set(), X=set()):
    """Bron Kerbosch algorithm with pivoting to find maximal cliques"""

    if not P and not X:
        yield R

    # the crucial part of pivoting is here
    # we choose a pivot vertex u from the union of pending and processed vertices
    # we delay the neighbors of pivot vertex from being added to the clique
    # of course they will be added in the future recursive calls
    # we do that, we can make fewer iterations in recursion
    # if you count the recursive calls
    # you will find out pivot version reduce 2 recursive calls
    try:
        u = list(P.union(X)).pop()
        N = P.difference(ADT.edge(u))

    # sometimes our choice sucks
    # the neighbors of pivot u are equivalent to priority queue
    # in that case we just roll back to the function without pivoting
    except IndexError:
        N = P

    for v in N:
        yield from bron_kerbosch_pivot(ADT,
                                       R=R.union([v]),
                                       P=P.intersection(ADT.edge(v)),
                                       X=X.intersection(ADT.edge(v)))
        P.remove(v)
        X.add(v)


# the easiest way to understand is to think of k core
# a maximal clique suffices to the condition of a k core network
# because a maximal clique is fully connected
# each vertex inside is guaranteed to have degree of k
# where k+1 is the order of the maximal clique
# but the reverse does not hold
# each vertex is ranked by its guaranteed degree in degeneracy ordering
# when we choose vertex from degeneracy ordering
# we output the maximal cliques in ascending order
# the later vertices extracted from degeneracy ordering
# are more likely to form a maximal clique of a larger degree altogether
# in this way, we can potentially reduce the iteration
def bron_kerbosch_order(ADT, R=set(), P=set(), X=set()):
    """Bron Kerbosch algorithm with vertex ordering to find maximal cliques"""

    # please check the details of degeneracy ordering from k core
    # https://github.com/je-suis-tm/graph-theory/blob/master/k%20core.ipynb
    # we only need degeneracy ordering L
    deg_order = graph.matula_beck(ADT, ordering=True)

    if not P and not X:
        yield R

    for v in deg_order:
        # yield from bron_kerbosch_pivot(ADT,
        #                                R=R.union([v]),
        #                                P=P.intersection(ADT.edge(v)),
        #                                X=X.intersection(ADT.edge(v)))
        yield from bron_kerbosch(ADT,
                                       R=R.union([v]),
                                       P=P.intersection(ADT.edge(v)),
                                       X=X.intersection(ADT.edge(v)))
        P.remove(v)
        X.add(v)
