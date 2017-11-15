package irlab.dao;

import irlab.model.GapsArticle;

public interface GapsArticleMapper {
    int deleteByPrimaryKey(Integer id);

    int insert(GapsArticle record);

    int insertSelective(GapsArticle record);

    GapsArticle selectByPrimaryKey(Integer id);

    int updateByPrimaryKeySelective(GapsArticle record);

    int updateByPrimaryKey(GapsArticle record);
}