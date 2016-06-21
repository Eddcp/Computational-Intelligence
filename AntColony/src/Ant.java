import java.util.*;

public class Ant {

    private class VertexWithChance {
        private Double chance;
        private Vertex vertex;

        VertexWithChance(Vertex vertex, Double chance) {
            this.vertex = vertex;
            this.chance = chance;
        }
    }

    public Set<Vertex> visitedVertices = new LinkedHashSet<>();
    public Vertex currentVertex;

    Ant(Vertex initialVertex) {
        this.currentVertex = initialVertex;
        this.visitedVertices.add(initialVertex);
    }

    public void goToNextVertice() {
        List<Vertex> neighborsVertices = currentVertex.getNeighborVertices();
        List<Edge> neighborsEdges = currentVertex.getNeighborEdges();

        List<VertexWithChance> possibleVertices = new LinkedList<>();
        Double costSum = 0.;
        for (Edge e : neighborsEdges) {
            Vertex v = e.getOtherVertex(currentVertex);
            if (visitedVertices.contains(v)) {
                continue;
            }

            possibleVertices.add(new VertexWithChance(v, costSum));
            costSum += (1 / e.cost);
        }

        Random generator = new Random();
        Double randomCost = generator.nextDouble() % costSum;
        VertexWithChance chosen = possibleVertices.get(0);
        for (VertexWithChance vc : possibleVertices) {
            if (randomCost < vc.chance) {
                break;
            }
            chosen = vc;
        }



    }



}
