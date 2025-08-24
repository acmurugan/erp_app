#!/usr/bin/env python3
"""
Run parameter visibility SQL update
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db_connection

def run_sql_file(filename):
    """Execute SQL file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print(f"Executing SQL from {filename}...")
        
        with get_db_connection() as connection:
            cursor = connection.cursor()
            
            # Split by statement and execute each
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
            
            for i, statement in enumerate(statements, 1):
                if statement.upper().startswith('UPDATE') or statement.upper().startswith('COMMIT'):
                    print(f"Executing statement {i}: {statement[:50]}...")
                    cursor.execute(statement)
                    if statement.upper().startswith('UPDATE'):
                        print(f"  Rows affected: {cursor.rowcount}")
                    
            connection.commit()
            cursor.close()
            
        print("✅ SQL execution completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error executing SQL: {e}")
        return False

if __name__ == "__main__":
    success = run_sql_file("update_parameter_visibility.sql")
    if success:
        print("\n🎉 Parameter visibility update completed!")
        print("Now the admin interface will show proper visibility checkboxes.")
    else:
        print("\n💥 Update failed - check the error above.")