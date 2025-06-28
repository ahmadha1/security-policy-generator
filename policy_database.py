#!/usr/bin/env python3
"""
Policy Database Module
Handles saving and loading of generated policies and controls organized by organization name
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class PolicyDatabase:
    def __init__(self, db_path: Optional[str] = None):
        """Initialize the policy database"""
        if db_path is None:
            # Use absolute path to ensure we always use the correct database
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(current_dir, "policy_tracker.db")
        else:
            self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create organizations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS organizations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    industry TEXT,
                    framework TEXT,
                    organization_size TEXT,
                    countries TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create policies table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS policies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    organization_id INTEGER,
                    policy_content TEXT NOT NULL,
                    filename TEXT,
                    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    generator_type TEXT DEFAULT 'standard',
                    FOREIGN KEY (organization_id) REFERENCES organizations (id)
                )
            ''')
            
            # Create controls table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS controls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    organization_id INTEGER,
                    controls_content TEXT NOT NULL,
                    filename TEXT,
                    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (organization_id) REFERENCES organizations (id)
                )
            ''')
            
            # Create implementation guides table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS implementation_guides (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    organization_id INTEGER,
                    guide_content TEXT NOT NULL,
                    filename TEXT,
                    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (organization_id) REFERENCES organizations (id)
                )
            ''')
            
            conn.commit()
    
    def save_organization(self, name: str, industry: List[str], framework: List[str], 
                         organization_size: str = "", countries: Optional[List[str]] = None) -> int:
        """Save or update organization information"""
        if countries is None:
            countries = []
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if organization exists
            cursor.execute("SELECT id FROM organizations WHERE name = ?", (name,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing organization
                cursor.execute('''
                    UPDATE organizations 
                    SET industry = ?, framework = ?, organization_size = ?, countries = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE name = ?
                ''', (json.dumps(industry), json.dumps(framework), organization_size, json.dumps(countries), name))
                return existing[0]
            else:
                # Create new organization
                cursor.execute('''
                    INSERT INTO organizations (name, industry, framework, organization_size, countries)
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, json.dumps(industry), json.dumps(framework), organization_size, json.dumps(countries)))
                return cursor.lastrowid or 0
    
    def save_policy(self, organization_name: str, policy_content: str, 
                   filename: str = "", generator_type: str = "standard") -> bool:
        """Save a generated policy"""
        try:
            org_id = self.save_organization(organization_name, [], [])
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO policies (organization_id, policy_content, filename, generator_type)
                    VALUES (?, ?, ?, ?)
                ''', (org_id, policy_content, filename, generator_type))
                return True
        except Exception as e:
            print(f"Error saving policy: {e}")
            return False
    
    def save_controls(self, organization_name: str, controls_content: str, 
                     filename: str = "") -> bool:
        """Save generated controls"""
        try:
            org_id = self.save_organization(organization_name, [], [])
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO controls (organization_id, controls_content, filename)
                    VALUES (?, ?, ?)
                ''', (org_id, controls_content, filename))
                return True
        except Exception as e:
            print(f"Error saving controls: {e}")
            return False
    
    def save_implementation_guide(self, organization_name: str, guide_content: str, 
                                 filename: str = "") -> bool:
        """Save generated implementation guide"""
        try:
            org_id = self.save_organization(organization_name, [], [])
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO implementation_guides (organization_id, guide_content, filename)
                    VALUES (?, ?, ?)
                ''', (org_id, guide_content, filename))
                return True
        except Exception as e:
            print(f"Error saving implementation guide: {e}")
            return False
    
    def get_organizations(self) -> List[Dict]:
        """Get all organizations with their latest policy info"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    o.id, o.name, o.industry, o.framework, o.organization_size, o.countries,
                    o.created_at, o.updated_at,
                    COUNT(p.id) as policy_count,
                    COUNT(c.id) as controls_count,
                    COUNT(ig.id) as guides_count
                FROM organizations o
                LEFT JOIN policies p ON o.id = p.organization_id
                LEFT JOIN controls c ON o.id = c.organization_id
                LEFT JOIN implementation_guides ig ON o.id = ig.organization_id
                GROUP BY o.id
                ORDER BY o.updated_at DESC
            ''')
            
            rows = cursor.fetchall()
            organizations = []
            
            for row in rows:
                org = {
                    'id': row[0],
                    'name': row[1],
                    'industry': json.loads(row[2]) if row[2] else [],
                    'framework': json.loads(row[3]) if row[3] else [],
                    'organization_size': row[4],
                    'countries': json.loads(row[5]) if row[5] else [],
                    'created_at': row[6],
                    'updated_at': row[7],
                    'policy_count': row[8],
                    'controls_count': row[9],
                    'guides_count': row[10]
                }
                organizations.append(org)
            
            return organizations
    
    def get_organization_policies(self, organization_name: str) -> List[Dict]:
        """Get all policies for a specific organization"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.id, p.policy_content, p.filename, p.generated_at, p.generator_type
                FROM policies p
                JOIN organizations o ON p.organization_id = o.id
                WHERE o.name = ?
                ORDER BY p.generated_at DESC
            ''', (organization_name,))
            
            rows = cursor.fetchall()
            policies = []
            
            for row in rows:
                policy = {
                    'id': row[0],
                    'content': row[1],
                    'filename': row[2],
                    'generated_at': row[3],
                    'generator_type': row[4]
                }
                policies.append(policy)
            
            return policies
    
    def get_organization_controls(self, organization_name: str) -> List[Dict]:
        """Get all controls for a specific organization"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.id, c.controls_content, c.filename, c.generated_at
                FROM controls c
                JOIN organizations o ON c.organization_id = o.id
                WHERE o.name = ?
                ORDER BY c.generated_at DESC
            ''', (organization_name,))
            
            rows = cursor.fetchall()
            controls = []
            
            for row in rows:
                control = {
                    'id': row[0],
                    'content': row[1],
                    'filename': row[2],
                    'generated_at': row[3]
                }
                controls.append(control)
            
            return controls
    
    def get_organization_guides(self, organization_name: str) -> List[Dict]:
        """Get all implementation guides for a specific organization"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ig.id, ig.guide_content, ig.filename, ig.generated_at
                FROM implementation_guides ig
                JOIN organizations o ON ig.organization_id = o.id
                WHERE o.name = ?
                ORDER BY ig.generated_at DESC
            ''', (organization_name,))
            
            rows = cursor.fetchall()
            guides = []
            
            for row in rows:
                guide = {
                    'id': row[0],
                    'content': row[1],
                    'filename': row[2],
                    'generated_at': row[3]
                }
                guides.append(guide)
            
            return guides
    
    def delete_organization(self, organization_name: str) -> bool:
        """Delete an organization and all its associated data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM organizations WHERE name = ?", (organization_name,))
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting organization: {e}")
            return False 