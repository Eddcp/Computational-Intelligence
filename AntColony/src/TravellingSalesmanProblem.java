
import java.io.File;
import java.util.List;

class TravellingSalesmanProblem
{
    public static void main (String[] args)
    {
        Graph graph = new Graph(new File("data/m38.txt"));
        AntColony colony = new AntColony(graph, 30, 0.10, 1., 1., 10, 10000);
        List<Edge> path = colony.findBetterPath();
        System.out.println(path);
        System.out.println(Edge.getEdgePathCost(path));
    }
}
