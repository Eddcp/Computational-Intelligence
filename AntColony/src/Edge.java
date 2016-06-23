import java.util.List;

class Edge {

    Double cost;
    Vertex vertex1;
    Vertex vertex2;

    Edge(Vertex v1, Vertex v2, Double cost) {
        this.vertex1 = v1;
        this.vertex2 = v2;
        this.cost = cost;
    }

    Vertex getOtherVertex(Vertex v) {
        Vertex other;
        if (v == this.vertex1) {
            other = this.vertex2;
        } else {
            other = this.vertex1;
        }
        return other;
    }

    static Double getEdgePathCost(List<Edge> edges) {
        Double cost = 0.;
        for (Edge e : edges) {
            cost += e.cost;
        }
        return cost;
    }

    @Override
    public String toString() {
        return String.format("(%1$s %2$s): %3$.0f", vertex1, vertex2, cost);
    }

    @Override
    public int hashCode() {
        return (vertex1.hashCode() + vertex2.hashCode() + cost.hashCode());
    }
}
