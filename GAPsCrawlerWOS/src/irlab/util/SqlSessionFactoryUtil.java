package irlab.util;
//2017/11/14 
// author = Shaw

import java.io.IOException;

import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

public class SqlSessionFactoryUtil {
    /**
     * 必须单例模式.
     */
    private static SqlSessionFactory sessionFactory = null;

    public static SqlSessionFactory getSessionFactory() {

        if (sessionFactory == null) {
            String resource = "irlab/resource/SqlMapConfig.xml";
            try {
                sessionFactory = new SqlSessionFactoryBuilder().build(Resources
                        .getResourceAsReader(resource));
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return sessionFactory;
    }
}
