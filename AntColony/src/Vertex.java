import javafx.geometry.Point2D;
import java.util.LinkedList;
import java.util.List;

class Vertex {

    Integer id;
    Point2D position;
    List<Edge> neighborEdges = new LinkedList<>();
    List<Vertex> neighborVertices = new LinkedList<>();

    Vertex(Integer id, Point2D position) {
        this.id = id;
        this.position = position;
    }

    List<Vertex> getNeighborVertices() {
        return neighborVertices;
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

    @Override
    public String toString() {
        return id.toString();
    }

    @Override
    public int hashCode() {
        return this.id.hashCode();
    }
}
