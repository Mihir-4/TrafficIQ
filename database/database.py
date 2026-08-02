"""
TrafficIQ - Database Repository Layer (SQLite)
Handles persistent storage of session metadata, frame-by-frame traffic statistics,
and automated event logging in SQLite database (database/traffic.db).
"""

import sqlite3
import json
import time
from typing import Dict, Any, List, Optional
from configs.config import DATABASE_PATH
from utils.logger import setup_logger

logger = setup_logger("Database")

class TrafficDatabase:
    """SQLite Database Interface for TrafficIQ."""
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Returns SQLite database connection with row factory enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Creates database schema if not exists."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Sessions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                source_name TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                total_frames INTEGER DEFAULT 0,
                total_vehicles_counted INTEGER DEFAULT 0,
                peak_density TEXT DEFAULT 'Low',
                avg_congestion_score REAL DEFAULT 0.0,
                peak_vehicles_present INTEGER DEFAULT 0,
                total_co2_g REAL DEFAULT 0.0,
                status TEXT DEFAULT 'Completed'
            )
        """)

        # Frame Metrics Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS frame_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                frame_id INTEGER,
                timestamp TIMESTAMP,
                vehicles_present INTEGER,
                class_distribution_json TEXT,
                density TEXT,
                congestion_score REAL,
                occupancy_ratio REAL,
                signal_timing INTEGER,
                co2_emission_g REAL,
                FOREIGN KEY (session_id) REFERENCES sessions (session_id)
            )
        """)

        # Events Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TIMESTAMP,
                event_type TEXT,
                description TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions (session_id)
            )
        """)

        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")

    def create_session(self, session_id: str, source_name: str) -> bool:
        """Inserts a new session record."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                INSERT INTO sessions (session_id, source_name, start_time, status)
                VALUES (?, ?, ?, 'In Progress')
            """, (session_id, source_name, now))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error creating session {session_id}: {e}")
            return False

    def log_frame_metric(self, session_id: str, frame_id: int, analytics: Dict[str, Any]) -> bool:
        """Logs single frame analytics into frame_metrics table."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            now = time.strftime("%Y-%m-%d %H:%M:%S")

            class_json = json.dumps(analytics.get("class_distribution", {}))
            co2 = analytics.get("emissions_g_per_min", {}).get("CO2", 0.0)

            cursor.execute("""
                INSERT INTO frame_metrics (
                    session_id, frame_id, timestamp, vehicles_present,
                    class_distribution_json, density, congestion_score,
                    occupancy_ratio, signal_timing, co2_emission_g
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id, frame_id, now,
                analytics.get("vehicles", 0),
                class_json,
                analytics.get("density", "Low"),
                analytics.get("congestion_score", 0.0),
                analytics.get("occupancy_ratio", 0.0),
                analytics.get("signal_timing", 30),
                co2
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error logging frame metric: {e}")
            return False

    def complete_session(
        self,
        session_id: str,
        total_frames: int,
        total_vehicles_counted: int,
        peak_density: str,
        avg_congestion: float,
        peak_vehicles: int,
        total_co2: float
    ) -> bool:
        """Updates session status to Completed and logs summary statistics."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            now = time.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                UPDATE sessions SET
                    end_time = ?,
                    total_frames = ?,
                    total_vehicles_counted = ?,
                    peak_density = ?,
                    avg_congestion_score = ?,
                    peak_vehicles_present = ?,
                    total_co2_g = ?,
                    status = 'Completed'
                WHERE session_id = ?
            """, (
                now, total_frames, total_vehicles_counted, peak_density,
                avg_congestion, peak_vehicles, total_co2, session_id
            ))
            conn.commit()
            conn.close()
            logger.info(f"Session {session_id} marked complete.")
            return True
        except Exception as e:
            logger.error(f"Error completing session {session_id}: {e}")
            return False

    def get_all_sessions(self, include_empty: bool = False) -> List[Dict[str, Any]]:
        """Returns list of session dicts. If include_empty=False, filters out 0-frame orphaned sessions."""
        conn = self._get_connection()
        cursor = conn.cursor()
        if include_empty:
            cursor.execute("SELECT * FROM sessions ORDER BY start_time DESC")
        else:
            cursor.execute("SELECT * FROM sessions WHERE total_frames > 0 OR status = 'Completed' ORDER BY start_time DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_session_frames(self, session_id: str) -> List[Dict[str, Any]]:
        """Returns all frame metrics for a given session."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM frame_metrics WHERE session_id = ? ORDER BY frame_id ASC", (session_id,))
        rows = cursor.fetchall()
        conn.close()

        results = []
        for r in rows:
            d = dict(r)
            d["class_distribution"] = json.loads(d["class_distribution_json"]) if d.get("class_distribution_json") else {}
            results.append(d)
        return results

    def get_session_details(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Returns metadata for a specific session."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def delete_session(self, session_id: str) -> bool:
        """Deletes a session and its associated frame metrics."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM frame_metrics WHERE session_id = ?", (session_id,))
            cursor.execute("DELETE FROM events WHERE session_id = ?", (session_id,))
            cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
            conn.commit()
            conn.close()
            logger.info(f"Deleted session: {session_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {e}")
            return False

    def cleanup_empty_sessions(self) -> int:
        """Deletes 0-frame orphaned sessions left in 'In Progress' state."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM frame_metrics WHERE session_id IN (SELECT session_id FROM sessions WHERE total_frames = 0 AND status = 'In Progress')")
            cursor.execute("DELETE FROM sessions WHERE total_frames = 0 AND status = 'In Progress'")
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} empty orphaned sessions.")
            return deleted_count
        except Exception as e:
            logger.error(f"Error cleaning up empty sessions: {e}")
            return 0
