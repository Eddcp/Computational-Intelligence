import java.awt.*;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;

class Graph {

    List<Vertex> vertices;
    List<Edge> edges;


    Graph(File fileWithXandYOfVertices) {
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

    List<Edge> getEdgePath(List<Vertex> vertices) {
        List<Edge> edges = new LinkedList<>();
        Vertex current;
        Vertex next;
        for (int i = 0; i < (vertices.size() - 1); i++) {
            current = vertices.get(i);
            next = vertices.get(i+1);
            Edge e = current.getEdgeForVertex(next);
            if (e == null) {
                System.out.println("Couldn't find edge path for this vertices");
                return null;
            }
            edges.add(e);
        }
        return edges;
    }

    // criar a sequencia de vertices, dado um caminho de arestas, nao eh tao trivial
    // pq se o grafo for nao-direcionado,
    List<Vertex> getVerticesOfEdgePath(List<Edge> edges) {
        List<Vertex> vertices = new LinkedList<>();
        Vertex initialVertex;

        Vertex v1, v2, v3, v4;
        v1 = edges.get(0).vertex1;
        v2 = edges.get(0).vertex2;
        v3 = edges.get(1).vertex1;
        v4 = edges.get(1).vertex2;

        Set<Vertex> auxSet = new HashSet<>(2);
        auxSet.add(v3);
        auxSet.add(v4);
        if (auxSet.contains(v1)) {
            initialVertex = v2;
        } else if (auxSet.contains(v2)) {
            initialVertex = v1;
        } else {
            System.out.println("Error in finding sequency of vertices for an edge path");
            return null;
        }

        Vertex v = initialVertex;
        vertices.add(v);
        for (Edge e : edges) {
            v = e.getOtherVertex(v);
            if (v == null) {
                System.out.println("Error in finding sequency of vertices for an edge path");
                return null;
            }
            vertices.add(v);
        }
        
        return vertices;
    }

}
