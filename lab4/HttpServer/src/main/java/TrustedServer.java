public class TrustedServer {
    public static void main(String[] args) throws Exception {
        System.setProperty("javax.net.ssl.keyStore", "server_keystore.jks");
        System.setProperty("javax.net.ssl.keyStorePassword", "changeit");
        System.setProperty("javax.net.ssl.trustStore", "client_keystore.jks");
        System.setProperty("javax.net.ssl.trustStorePassword", "changeit");

        try (Server server = new Server(8082)) {
            server.start();
        }
    }
}
