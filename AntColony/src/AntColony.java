import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

class AntColony {

    static final double pheromoneInitialQty = 1;

    Map<Edge, Double> mapEdgeToPheromone;
    List<Ant> ants;
    Double evaporationRate;
    Double pheromoneWeight;
    Double heuristicWeight;
    Graph graph;

    AntColony(Graph graph, Integer antsQty, Double evaporationRate, Double pheromoneWeight, Double heuristicWeight) {

        this.graph = graph;
        this.evaporationRate = evaporationRate;
        this.pheromoneWeight = pheromoneWeight;
        this.heuristicWeight = heuristicWeight;

        if (antsQty <= graph.vertices.size()) {
            for (int i = 0; i < antsQty; i++) {
                ants.add(new Ant(this, graph.vertices.get(i)));
            }
        } else {
            for (int i = 0; i < antsQty; i++) {
                Random generator = new Random();
                int j = generator.nextInt(graph.vertices.size());
                ants.add(new Ant(this, graph.vertices.get(j)));
            }
        }

        mapEdgeToPheromone = new HashMap<>();
        for (Edge e : graph.edges) {
            mapEdgeToPheromone.put(e, pheromoneInitialQty);
        }
    }

    Double getPheromoneCost(Edge e) {
        return (Math.pow(mapEdgeToPheromone.get(e), pheromoneWeight));
    }

    Double getHeuristicCost(Edge e) {
        return Math.pow((1 / e.cost), heuristicWeight);
    }

    void updatePheromones() {

    }

    void welcomeReturningAnt(Ant ant) {

    }

}
