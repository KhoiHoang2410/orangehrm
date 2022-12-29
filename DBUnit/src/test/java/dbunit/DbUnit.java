package dbunit;

import org.dbunit.DBTestCase;
import org.dbunit.PropertiesBasedJdbcDatabaseTester;
import org.dbunit.dataset.IDataSet;
import org.dbunit.dataset.xml.FlatXmlDataSetBuilder;
import org.dbunit.operation.DatabaseOperation;
import org.junit.Test;

import java.io.FileInputStream;
import java.sql.*;

import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.MatcherAssert.assertThat;

public class DbUnit extends DBTestCase {

    private Connection conn = null;
    private Statement stmt = null;
    public DbUnit(String name) throws SQLException {
        super( name );
        System.setProperty( PropertiesBasedJdbcDatabaseTester.DBUNIT_DRIVER_CLASS, "org.mariadb.jdbc.Driver" );
        System.setProperty( PropertiesBasedJdbcDatabaseTester.DBUNIT_CONNECTION_URL, "jdbc:mariadb://localhost:3333/orangehrm" );
        System.setProperty( PropertiesBasedJdbcDatabaseTester.DBUNIT_USERNAME, "root" );
        System.setProperty( PropertiesBasedJdbcDatabaseTester.DBUNIT_PASSWORD, "orangehrm" );

        conn = DriverManager.getConnection("jdbc:mariadb://localhost:3333/orangehrm", "root", "orangehrm");
        stmt = conn.createStatement();
    }

    protected IDataSet getDataSet() throws Exception
    {
        return new FlatXmlDataSetBuilder().build(new FileInputStream("user.xml"));
    }

    protected DatabaseOperation getSetUpOperation() throws Exception
    {
        return DatabaseOperation.REFRESH;
    }

//    protected DatabaseOperation getTearDownOperation() throws Exception
//    {
//        return DatabaseOperation.DELETE_ALL;
//    }

    @Test
    public void testNumberOfUsers() throws SQLException {
        ResultSet rs = stmt.executeQuery(
        "SELECT COUNT(*)\n" +
            "FROM hs_hr_employee\n" +
            "WHERE emp_number IN(\n" +
                "SELECT emp_number\n" +
                "FROM ohrm_leave_entitlement\n" +
                "GROUP BY emp_number\n" +
                "HAVING SUM(days_used) > 12\n" +
            ")"
        );
        rs.next();

        assertThat(rs.getInt(1), is(6139));
    }
}
