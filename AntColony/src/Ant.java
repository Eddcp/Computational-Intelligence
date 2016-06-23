import java.util.*;

class Ant
{
    private class EdgeWithChance
    {
        private Double chance;
        private Edge edge;

        EdgeWithChance(Edge edge, Double chance) {
            this.edge = edge;
            this.chance = chance;
        }
    }

    Set<Vertex> visitedVertices = new LinkedHashSet<>();
    List<Edge> pathTaken = new LinkedList<>();

    Vertex initialVertex;
    Vertex currentVertex;
    Vertex previousVertex;
    AntColony colony;

    Ant(AntColony colony, Vertex initialVertex)
    {
        this.colony = colony;
        this.previousVertex = null;
        this.currentVertex = initialVertex;
        this.visitedVertices.add(initialVertex);
        this.initialVertex = initialVertex;
    }

    Edge goToNextEdge()
    {
        Edge next = chooseNextEdge();
        if (next == null && currentVertex != initialVertex) {
            next = currentVertex.getEdgeForVertex(initialVertex);
        } else if (next == null && currentVertex == initialVertex) {
            colony.antDidReturn(this);
            return null;
        }

        Vertex v = next.getOtherVertex(currentVertex);
        visitedVertices.add(v);
        pathTaken.add(next);
        previousVertex = currentVertex;
        currentVertex = v;
        return next;
    }

    private Edge chooseNextEdge()
    {
        List<Vertex> neighborsVertices = currentVertex.getNeighborVertices();
        List<Edge> neighborsEdges = currentVertex.getNeighborEdges();

        List<EdgeWithChance> possibleEdges = new LinkedList<>();
        Double costSum = 0.;
        for (Edge e : neighborsEdges) {
            Vertex v = e.getOtherVertex(currentVertex);
            if (visitedVertices.contains(v)) {
                continue;
            }

            possibleEdges.add(new EdgeWithChance(e, costSum));
            costSum += colony.getColonyCost(e);
        }

        if (possibleEdges.size() == 0) {
            return null;
        }

        Random generator = new Random();
        Double randomCost = generator.nextDouble() * costSum;
        EdgeWithChance chosen = possibleEdges.get(0);
        for (EdgeWithChance ec : possibleEdges) {
            if (randomCost < ec.chance) {
                break;
            }
            chosen = ec;
        }

        return chosen.edge;
    }

    
}
