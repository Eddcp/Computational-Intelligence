import java.awt.Point;
import java.util.LinkedList;
import java.util.List;

class Vertex {

    Point position;
    List<Edge> neighborEdges;
    List<Vertex> neighborVertices;

    Vertex(Point position) {
        this.position = position;
    }

    List<Vertex> getNeighborVertices() {
        List<Vertex> neighbors = new LinkedList<>();
        for(Edge e : neighborEdges) {
            Vertex v;
            if (e.vertex1 != this) {
                v = e.vertex1;
            } else {
                v = e.vertex2;
            }
            neighbors.add(v);
        }
        return neighbors;
    }

    List<Edge> getNeighborEdges() {
        return neighborEdges;
    }

    Edge getEdgeForVertex(Vertex other) {
        for (Edge e : neighborEdges) {
            Vertex v = e.getOtherVertex(this);
            if (v == other) {
                return e;
            }
        }
        return null;
    }
}
