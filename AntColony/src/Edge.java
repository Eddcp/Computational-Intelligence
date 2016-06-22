
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

}
