public class TrustedClient {
    public static void main(String[] args) {
        System.setProperty("javax.net.ssl.keyStore", "client_keystore.jks");
        System.setProperty("javax.net.ssl.keyStorePassword", "changeit");
        System.setProperty("javax.net.ssl.trustStore", "server_keystore.jks");
        System.setProperty("javax.net.ssl.trustStorePassword", "changeit");

        Client.req("https://bnr.ro/Home-Mobile.aspx");
    }
}
