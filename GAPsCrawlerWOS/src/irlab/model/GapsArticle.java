package irlab.model;

public class GapsArticle {
    private Integer id;

    private String articletitle;

    private String articleauthor;

    private String articleyear;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getArticletitle() {
        return articletitle;
    }

    public void setArticletitle(String articletitle) {
        this.articletitle = articletitle == null ? null : articletitle.trim();
    }

    public String getArticleauthor() {
        return articleauthor;
    }

    public void setArticleauthor(String articleauthor) {
        this.articleauthor = articleauthor == null ? null : articleauthor.trim();
    }

    public String getArticleyear() {
        return articleyear;
    }

    public void setArticleyear(String articleyear) {
        this.articleyear = articleyear == null ? null : articleyear.trim();
    }
}