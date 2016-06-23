import java.util.*;

class AntColony
{
    static final double pheromoneInitialQty = 1;

    Map<Edge, Double> mapEdgeToPheromone = new HashMap<>();
    List<Ant> ants = new LinkedList<>();
    Integer currentIteration = 0;

    Integer antsQty;
    Double evaporationRate;
    Double pheromoneWeight;
    Double heuristicWeight;
    Graph graph;
    Integer excrementedPheromonePerAnt;
    Integer maxIterations;
    Integer minIterations;

    private List<Ant> antsReturned = new LinkedList<>();
    private List<Edge> bestEdgePath;

    AntColony(Graph graph, Integer antsQty, Double evaporationRate, Double pheromoneWeight, Double heuristicWeight, Integer excrementedPheromonePerAnt, Integer maxIterations)
    {
        this.graph = graph;
        this.evaporationRate = evaporationRate;
        this.pheromoneWeight = pheromoneWeight;
        this.heuristicWeight = heuristicWeight;
        this.excrementedPheromonePerAnt = excrementedPheromonePerAnt;
        this.maxIterations = maxIterations;
        this.minIterations = (int)(0.01 * maxIterations);
        this.antsQty = antsQty;
        this.mapEdgeToPheromone = new HashMap<>(graph.edges.size());

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

    List<Edge> findBetterPath()
    {
        List<Edge> path = null;
        while ( (currentIteration < minIterations) ||
                (currentIteration < maxIterations && hasDivergency())
                ) {
            replaceReturnedAnts();
            for (Ant ant : ants) {
                ant.goToNextEdge();
            }
            if (antsReturned.size() != 0) {
                path = getBestEdgePathOfIteration();
                if (Edge.getEdgePathCost(path) < Edge.getEdgePathCost(bestEdgePath)) {
                    bestEdgePath = path;
                }
                updatePheromones();
                this.currentIteration++;
            }
        }
        System.out.println("Iteration: " + currentIteration);
        return bestEdgePath;
    }

    boolean hasDivergency()
    {
        if (antsReturned.size() == 0) {
            return true;
        }

        Set< Set<Edge> > set = new HashSet<>(2);
        for (Ant a : antsReturned) {
            set.add(new HashSet<>(a.pathTaken));
            if (set.size() > 1) {
                return true;
            }
        }
        return false;
    }

    Double getPheromoneCost(Edge e)
    {
        return (Math.pow(mapEdgeToPheromone.get(e), pheromoneWeight));
    }

    Double getPheromoneCost(List<Edge> edges)
    {
        Double total = 0.;
        for (Edge e : edges) {
            total += mapEdgeToPheromone.get(e);
        }
        return total;
    }

    Double getHeuristicCost(Edge e)
    {
        return Math.pow((1 / e.cost), heuristicWeight);
    }

    Double getColonyCost(Edge e)
    {
        return getPheromoneCost(e) * getHeuristicCost(e);
    }

    Double getColonyCost(List<Edge> edges)
    {
        Double total = 0.;
        for (Edge e : edges) {
            total += getColonyCost(e);
        }
        return total;
    }

    private boolean updatePheromones()
    {
        if (antsReturned.size() == 0) {
            return false;
        }

        for (Edge e : mapEdgeToPheromone.keySet()) {
            Double previous = mapEdgeToPheromone.get(e);
            Double newPheromone = previous * (1 - this.evaporationRate);
            mapEdgeToPheromone.replace(e, newPheromone);
        }

        for (Ant ant : antsReturned) {
            Double pathCost = Edge.getEdgePathCost(ant.pathTaken);
            for (Edge e : ant.pathTaken) {
                Double previous = mapEdgeToPheromone.get(e);
                Double update = excrementedPheromonePerAnt / pathCost;
                mapEdgeToPheromone.replace(e, previous + update);
            }
        }
        return true;
    }


    private void replaceReturnedAnts()
    {
        for (Ant a : antsReturned) {
            ants.remove(a);
            ants.add(new Ant(this, a.initialVertex));
        }
        antsReturned.clear();
    }


    void antDidReturn(Ant ant)
    {
        antsReturned.add(ant);
    }



    List<Edge> getBestEdgePathOfIteration()
    {
        if (antsReturned.size() == 0) {
            return new LinkedList<>();
        }

        List<Edge> bestPath = antsReturned.get(0).pathTaken;
        Double bestCost = getColonyCost(bestPath);
        for (Ant a : antsReturned) {
            Double cost = getColonyCost(a.pathTaken);
            if (Objects.equals(cost, bestCost)) {
                if (Edge.getEdgePathCost(a.pathTaken) < Edge.getEdgePathCost(bestPath)) {
                    bestCost = cost;
                    bestPath = a.pathTaken;
                }
            } else if (cost.compareTo(bestCost) > 0) {
                bestCost = cost;
                bestPath = a.pathTaken;
            }
        }

        if (bestEdgePath == null) {
            bestEdgePath = bestPath;
        }

        return bestPath;
    }

    List<Vertex> getBetterVertexPathOfIteration()
    {
        List<Edge> edges = getBestEdgePathOfIteration();
        return Graph.getVerticesOfEdgePath(edges);
    }

}
