import javax.net.ssl.SSLServerSocket;
import javax.net.ssl.SSLServerSocketFactory;
import javax.net.ssl.SSLSocket;
import java.io.*;

public class Server implements AutoCloseable {
    private final Integer port;
    private final SSLServerSocket sslServerSocket;
    private final String response;

    public Server(Integer port) throws IOException {

        this.port = port;
        sslServerSocket = (SSLServerSocket) SSLServerSocketFactory.getDefault().createServerSocket(port);
        BufferedReader in = new BufferedReader(new FileReader("bnr.html"));
        StringBuilder sb = new StringBuilder();
        String s;
        while ((s = in.readLine()) != null) {
            sb.append(s);
        }
        response = sb.toString();
    }

    @Override
    public void close() throws Exception {
        if (sslServerSocket != null && !sslServerSocket.isClosed()) {
            sslServerSocket.close();
        }
    }

    public void start() {
        System.out.println("Server started on port: " + port);
        while (true) {
            try (SSLSocket socket = (SSLSocket) sslServerSocket.accept()) {
                System.out.println("Got the connection");

                BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                String s;
                while((s = in.readLine())!=null){
                    System.out.println(s);
                    if(s.isEmpty()){
                        break;
                    }
                }

                OutputStream clientOutput = socket.getOutputStream();
                clientOutput.write("HTTP/1.1 200 OK\r\n".getBytes());
                clientOutput.write("\r\n".getBytes());
                clientOutput.write(response.getBytes());
                clientOutput.write("\r\n\r\n".getBytes());
                clientOutput.flush();
                System.out.println("Client connection closed!");
                // in.close();
                clientOutput.close();
            } catch (IOException e) {
                System.out.println(e);
            }
        }
    }
}
