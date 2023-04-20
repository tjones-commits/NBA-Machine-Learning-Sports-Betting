import sqlite3
con = sqlite3.connect("../../Data/odds.sqlite")
c = con.cursor()

# Define the SQL statement to delete rows with specified values in the Date column
sql_statement = """DELETE FROM "odds_2019-20" WHERE Date IN ('2019-20-0214', '2019-20-0216')"""
sql_statement1 = """DELETE FROM "odds_2020-21" WHERE Date IN ('2020-21-0307')"""
# Execute the SQL statement
c.execute(sql_statement)

# Commit the changes to the database
con.commit()
c.execute(sql_statement1)
con.commit()
# Close the database connection
con.close()
