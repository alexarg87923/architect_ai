#!/usr/bin/env python3
"""
Script to clear old roadmap data from the database.
This will set all roadmap_data fields to NULL in the projects table
and delete all entries in the roadmaps table.
"""

import sqlite3
import os

# Database path (relative to backend directory)
DB_PATH = "roadmap.db"

def clear_roadmaps():
    """Clear all old roadmap data from the database"""

    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        print(f"   Current directory: {os.getcwd()}")
        return False

    try:
        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("🗑️  Clearing old roadmap data...")

        # Clear roadmap_data from projects table
        cursor.execute("UPDATE projects SET roadmap_data = NULL WHERE roadmap_data IS NOT NULL")
        projects_updated = cursor.rowcount
        print(f"   ✅ Cleared roadmap_data from {projects_updated} projects")

        # Delete all roadmaps from roadmaps table
        cursor.execute("DELETE FROM roadmaps")
        roadmaps_deleted = cursor.rowcount
        print(f"   ✅ Deleted {roadmaps_deleted} roadmap entries")

        # Commit the changes
        conn.commit()
        print("\n✅ Successfully cleared all old roadmap data!")
        print("   You can now refresh your app without schema errors.")

        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  Clear Old Roadmap Data")
    print("=" * 60)
    print()

    success = clear_roadmaps()

    print()
    print("=" * 60)

    exit(0 if success else 1)
