package irlab.htmlStore;
//2017/11/13 
// author = Shaw

import irlab.crawler.Crawler;
import irlab.model.GapsArticle;
import irlab.service.GapsArticleService;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class CrawlerTest {

    private static final String BASE_URI = "http://apps.webofknowledge.com/";

    public static void main(String[] args) throws IOException, InterruptedException {

        Crawler crawler = new Crawler();
        crawler.init();

        GapsArticleService gapsArticleService = new GapsArticleService();

        int i = 0;
        int j = 0;

        try {
            for (i = 501; i <= 600; i++) {

                String url = "http://apps.webofknowledge.com/summary.do?product=WOS&parentProduct=WOS&search_mode=GeneralSearch&qid=3&SID=Y1Wa2XcxL7nwsHLiviX&colName=WOS&page="+ i +"&action=changePageSize&pageSize=50";

                //爬取检索结果列表页面，然后从列表页面找到名称和连接，进而再爬取找到的文章连接，将其下载下来
                String content = crawler.crawl(url);
                Document document = Jsoup.parse(content, BASE_URI);

                Thread.sleep(2000);

                for (j = 1;j < 51;j++) {
                    //构造文章记录id
                    Element resultBlock = document.getElementById("RECORD_"+((i-1)*50+j));
                    Element link = resultBlock.getElementsByClass("smallV110").first();

                    String articleLink = link.attr("abs:href").toString();//文章连接
                    String articleName = link.text();//文章标题
                    String articleAuthor = resultBlock.getElementsByClass("label").first().parent().text().split("\\:")[1];

                    String articleYear = resultBlock.getElementsByClass("data_bold").last().text();

                    GapsArticle gapsArticle = new GapsArticle();
                    gapsArticle.setArticletitle(articleName);
                    gapsArticle.setArticleauthor(articleAuthor);
                    gapsArticle.setArticleyear(articleYear);

                    gapsArticleService.insertSelective(gapsArticle);

                    String articleContent = crawler.crawl(articleLink);

                    FileWriter fw=new FileWriter(new File("G:/wos/"+((i-1)*50+j)+".html"));
                    BufferedWriter bw=new BufferedWriter(fw);

                    bw.write(articleContent);
                    bw.close();
                    fw.close();

                    //控制时间，每次爬取一个休息一秒钟
                    if (j%2 == 0) {
                        Thread.sleep(1000);
                    }else {
                        Thread.sleep(2000);
                    }

                }
            }
        }catch (Exception e) {
            e.printStackTrace();
            System.out.println(i+","+j);
        }


    }
}
