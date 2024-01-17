public class FakeServer {
    public static void main(String[] args) throws Exception {
        System.setProperty("javax.net.ssl.keyStore", "fake_keystore.jks");
        System.setProperty("javax.net.ssl.keyStorePassword", "changeit");

        try (Server fakeServer = new Server(8081)) {
            fakeServer.start();
        }
    }
}
