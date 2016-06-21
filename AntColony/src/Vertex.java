import java.awt.Point;
import java.util.LinkedList;
import java.util.List;

public class Vertex {

    public Point position;
    public List<Edge> neighborEdges;
    public List<Vertex> neighborVertices;

    Vertex(Point position) {
        this.position = position;
    }

    public List<Vertex> getNeighborVertices() {
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

    public List<Edge> getNeighborEdges() {
        return neighborEdges;
    }
}
