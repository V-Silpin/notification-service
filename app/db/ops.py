import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, List, Any, Optional
from contextlib import contextmanager

class DatabaseError(Exception):
    """Custom exception for database operations"""
    pass

class PostgresDB:
    def __init__(self, host: str, database: str, user: str, password: str, port: int = 5432):
        self.connection_params = {
            'host': host,
            'database': 'postgres',  # Connect to default postgres database initially
            'user': user,
            'password': password,
            'port': port
        }
        self.target_database = database
        self.create_database_if_not_exists()
        # Update connection params to use the target database
        self.connection_params['database'] = self.target_database

    def create_database_if_not_exists(self):
        """Create the database if it doesn't exist"""
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            conn.autocommit = True  # Required for creating database
            with conn.cursor() as cur:
                # Check if database exists
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.target_database,))
                exists = cur.fetchone()
                
                if not exists:
                    cur.execute(f'CREATE DATABASE {self.target_database}')
        except psycopg2.Error as e:
            raise DatabaseError(f"Database creation error: {str(e)}")
        finally:
            if conn:
                conn.close()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            yield conn
        except psycopg2.Error as e:
            raise DatabaseError(f"Connection error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute a query and return results as a list of dictionaries"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    cur.execute(query, params)
                    if cur.description:
                        return cur.fetchall()
                    conn.commit()
                    return []
                except psycopg2.Error as e:
                    conn.rollback()
                    raise DatabaseError(f"Query execution error: {str(e)}")

    def insert(self, table: str, data: Dict[str, Any]) -> Dict:
        """Insert a record into the specified table"""
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING *"
        result = self.execute_query(query, tuple(data.values()))
        return result[0] if result else None

    def select(self, table: str, conditions: Dict[str, Any] = None, fields: List[str] = None) -> List[Dict]:
        """Select records from the specified table"""
        fields_str = ', '.join(fields) if fields else '*'
        query = f"SELECT {fields_str} FROM {table}"
        
        if conditions:
            where_clause = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
            query += f" WHERE {where_clause}"
            return self.execute_query(query, tuple(conditions.values()))
        return self.execute_query(query)

    def update(self, table: str, data: Dict[str, Any], conditions: Dict[str, Any]) -> Dict:
        """Update records in the specified table"""
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause} RETURNING *"
        params = tuple(list(data.values()) + list(conditions.values()))
        result = self.execute_query(query, params)
        return result[0] if result else None

    def delete(self, table: str, conditions: Dict[str, Any]) -> bool:
        """Delete records from the specified table"""
        where_clause = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        self.execute_query(query, tuple(conditions.values()))
        return True

    def create_table(self, table: str, columns: Dict[str, str], constraints: List[str] = None) -> bool:
        """Create a new table in the database
        Args:
            table (str): Name of the table
            columns (Dict[str, str]): Dictionary of column names and their SQL types
            constraints (List[str], optional): List of additional constraints
        """
        columns_def = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
        if constraints:
            columns_def += ', ' + ', '.join(constraints)
        
        query = f"CREATE TABLE IF NOT EXISTS {table} ({columns_def})"
        self.execute_query(query)
        return True