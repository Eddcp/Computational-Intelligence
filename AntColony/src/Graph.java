import java.awt.*;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.List;

public class Graph {

    public List<Vertex> vertices;
    public List<Edge> edges;


    public Graph(File fileWithXandYOfVertices) {
        try {
            BufferedReader reader = new BufferedReader(new FileReader(fileWithXandYOfVertices));

            String line;
            while( (line = reader.readLine()) != null ) {
                String[] parts = line.split("\\s");
                Integer x = Integer.parseInt(parts[0]);
                Integer y = Integer.parseInt(parts[1]);

                Point position = new Point(x, y);
                vertices.add(new Vertex(position));
            }

            for(Vertex v1 : vertices) {
                for (Vertex v2 : vertices) {
                    if(v1 == v2) {
                        continue;
                    }
                    Edge edge = new Edge(v1, v2, v1.position.distance(v2.position));
                    v1.neighborEdges.add(edge);
                    v2.neighborEdges.add(edge);
                    v1.neighborVertices.add(v2);
                    v2.neighborVertices.add(v1);
                    edges.add(edge);
                }
            }

        } catch (java.io.IOException e) {
            e.printStackTrace();
        }
    }

}
