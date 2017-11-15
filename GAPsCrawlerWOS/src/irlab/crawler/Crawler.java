package irlab.crawler;
//2017/11/13 
// author = Shaw

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.io.InputStream;
import java.util.Scanner;

/**
 * Created by Roger on 2015/10/7.
 */
public class Crawler {
    private CloseableHttpClient httpclient;
    private ResponseHandler<String> responseHandler;

    public void init() {
        httpclient = HttpClients.createDefault();
        responseHandler = new ResponseHandler<String>() {

            @Override
            public String handleResponse(final HttpResponse response)
                    throws ClientProtocolException, IOException {
                int status = response.getStatusLine().getStatusCode();
                if (status >= 200 && status < 300) {
                    HttpEntity entity = response.getEntity();
                    // 利用getContent()方法代替EntityUtils.toString()方法获取实体内容
                    // 否则会出现异常：ConnectionClosedException: Premature end of chunk coded message body: closing chunk ....
                    if(entity != null){
                        InputStream is = entity.getContent();
                        Scanner scanner = new Scanner(is);
                        String content = "";
                        while(scanner.hasNextLine()) {
                            content += scanner.nextLine();
                        }
                        return content;
                    }else{
                        return null;
                    }
//                    return entity != null ? EntityUtils.toString(entity, "GBK")
//                            : null;
                } else {
                    throw new ClientProtocolException(
                            "Unexpected response status: " + status);
                }
            }

        };
    }

    public String crawl(String url) throws ClientProtocolException, IOException {
        HttpGet httpget = new HttpGet(url);
        // System.out.println("Executing request " + httpget.getRequestLine());

        // Create a custom response handler
        return httpclient.execute(httpget, responseHandler);

    }

    public void close() throws IOException {
        httpclient.close();
    }
}

