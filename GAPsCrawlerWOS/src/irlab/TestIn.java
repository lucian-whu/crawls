package irlab;
//2017/11/14 
// author = Shaw

import irlab.model.GapsArticle;
import irlab.service.GapsArticleService;

public class TestIn {
    public static void main(String[] args) {
        GapsArticleService gapsArticleService = new GapsArticleService();

        String a = "hahha";

        GapsArticle gapsArticle = new GapsArticle();
        gapsArticle.setArticletitle(a);
        gapsArticleService.insertSelective(gapsArticle);
        System.out.println("dong");
    }
}
