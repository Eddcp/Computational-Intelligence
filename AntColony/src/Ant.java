import java.util.*;

class Ant {

    private class EdgeWithChance {
        private Double chance;
        private Vertex vertex;

        EdgeWithChance(Vertex vertex, Double chance) {
            this.vertex = vertex;
            this.chance = chance;
        }
    }

    Set<Vertex> visitedVertices = new LinkedHashSet<>();
    Vertex initialVertex;
    Vertex currentVertex;
    Vertex previousVertex;
    AntColony colony;
    List<Edge> pathTaken;

    Ant(AntColony colony, Vertex initialVertex) {
        this.colony = colony;
        this.previousVertex = null;
        this.currentVertex = initialVertex;
        this.visitedVertices.add(initialVertex);
        this.initialVertex = initialVertex;

    }

    boolean goToNextVertex() {
        Vertex next = chooseNextVertex();
        if (next == initialVertex) {
            return false;
        }
        visitedVertices.add(next);
        pathTaken.add();
        previousVertex = currentVertex;
        currentVertex = next;
        return true;
    }

    private Vertex chooseNextVertex() {
        List<Vertex> neighborsVertices = currentVertex.getNeighborVertices();
        List<Edge> neighborsEdges = currentVertex.getNeighborEdges();

        List<EdgeWithChance> possibleEdges = new LinkedList<>();
        Double costSum = 0.;
        for (Edge e : neighborsEdges) {
            Vertex v = e.getOtherVertex(currentVertex);
            if (visitedVertices.contains(v)) {
                continue;
            }

            Double cost = (colony.getHeuristicCost(e) * colony.getPheromoneCost(e));
            possibleEdges.add(new EdgeWithChance(e, costSum));
            costSum += cost;
        }

        if (possibleEdges.size() == 0) {
            return initialVertex;
        }

        Random generator = new Random();
        Double randomCost = generator.nextDouble() % costSum;
        EdgeWithChance chosen = possibleEdges.get(0);
        for (EdgeWithChance vc : possibleEdges) {
            if (randomCost < vc.chance) {
                break;
            }
            chosen = vc;
        }

        return chosen.vertex;
    }



}
