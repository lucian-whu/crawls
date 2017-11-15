package irlab.service;
//2017/11/14
// author = Shaw

import irlab.dao.GapsArticleMapper;
import irlab.model.GapsArticle;
import irlab.util.SqlSessionFactoryUtil;
import org.apache.ibatis.session.SqlSession;

public class GapsArticleService {

    SqlSession sqlSession = SqlSessionFactoryUtil.getSessionFactory().openSession();
    GapsArticleMapper gapsArticleMapper = sqlSession.getMapper(GapsArticleMapper.class);

    public int deleteByPrimaryKey(Integer id) {
        int i = gapsArticleMapper.deleteByPrimaryKey(id);
        sqlSession.commit();
        return i;
    }

    public int insert(GapsArticle record) {
        int i = gapsArticleMapper.insert(record);
        sqlSession.commit();
        return i;
    }

    public int insertSelective(GapsArticle record) {
        int i = gapsArticleMapper.insertSelective(record);
        sqlSession.commit();
        return i;
    }

    public GapsArticle selectByPrimaryKey(Integer id) {
        return gapsArticleMapper.selectByPrimaryKey(id);
    }

    public int updateByPrimaryKeySelective(GapsArticle record) {
        int i = gapsArticleMapper.updateByPrimaryKeySelective(record);
        sqlSession.commit();
        return i;
    }

    public int updateByPrimaryKey(GapsArticle record) {
        int i = gapsArticleMapper.updateByPrimaryKey(record);
        sqlSession.commit();
        return i;
    }
}