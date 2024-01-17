import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLSocketFactory;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.net.URL;
import java.security.cert.X509Certificate;
import java.util.Arrays;

public class Client {
    public static void main(String[] args) {
        req("https://bnr.ro/Home-Mobile.aspx");
    }

    public static void req(String urlstr) {
        try {
            URL url = new URL(urlstr);
            HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();
            connection.setSSLSocketFactory((SSLSocketFactory) SSLSocketFactory.getDefault());

            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;
            StringBuilder sb = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                sb.append(inputLine);
            }

            X509Certificate certificate = (X509Certificate) Arrays.stream(connection.getServerCertificates())
                .filter((e) -> e instanceof X509Certificate)
                .findFirst()
                .orElseThrow(() -> new RuntimeException("No valid X509certificate"));

            System.out.println("Verzioszam: " + certificate.getVersion());
            System.out.println("Szeriaszam: " + certificate.getSerialNumber());
            System.out.println("Tanusito hatosag neve: " + certificate.getIssuerX500Principal());
            System.out.println("Kibocsatas datuma: " + certificate.getNotBefore());
            System.out.println("Ervenyessegi ido: " + certificate.getNotAfter());
            System.out.println("Tanusitvany alanyak adatai: " + certificate.getSubjectX500Principal());
            System.out.println("Nyilvanos kulcs adatai: " + certificate.getPublicKey());

            in.close();

            BufferedWriter writer = new BufferedWriter(new FileWriter("bnr.html"));
            writer.write(sb.toString());
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
