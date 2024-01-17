public class Main {
    public static void main(String[] args) throws Exception {
        System.setProperty("javax.net.ssl.keyStore", "fake_keystore.jks");
        System.setProperty("javax.net.ssl.keyStorePassword", "changeit");

        try (FakeServer fakeServer = new FakeServer(8081)) {
            fakeServer.start();
        }
    }
}
