"""
Plugin Analytics Module - Dedicated analytics queries for plugin performance

This module provides plugin-specific analytics for the V5 Plugin Integration.
Extends the base analytics_queries.py with plugin-focused metrics.

Version: 1.0.0
Date: 2026-01-20

Features:
- Per-plugin performance metrics
- Plugin comparison analytics
- Plugin group aggregation (V3 vs V6)
- Timeframe-specific analytics for V6 plugins
"""

import sqlite3
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date, timedelta
from collections import defaultdict


class PluginAnalytics:
    """
    Plugin-specific analytics provider
    
    Provides detailed performance metrics for:
    - V3 Combined plugin (Logic 1, 2, 3)
    - V6 Price Action plugins (1M, 5M, 15M, 1H)
    """
    
    def __init__(self, db_connection: sqlite3.Connection):
        """
        Initialize plugin analytics
        
        Args:
            db_connection: SQLite database connection from TradeDatabase
        """
        self.conn = db_connection
    
    # ==================== PLUGIN PERFORMANCE ====================
    
    def get_plugin_performance(self, plugin_id: str, period: str = 'all') -> Dict[str, Any]:
        """
        Get performance metrics for specific plugin
        
        Args:
            plugin_id: Plugin identifier (e.g., 'v6_price_action_15m', 'v3_combined')
            period: 'today', 'week', 'month', 'all'
            
        Returns:
            Dict with comprehensive plugin performance metrics
        """
        cursor = self.conn.cursor()
        
        # Base query for plugin performance
        query = """
            SELECT 
                COUNT(*) as trade_count,
                SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN pnl <= 0 THEN 1 ELSE 0 END) as losses,
                SUM(pnl) as total_pnl,
                AVG(pnl) as avg_trade,
                AVG(CASE WHEN pnl > 0 THEN pnl END) as avg_win,
                AVG(CASE WHEN pnl <= 0 THEN pnl END) as avg_loss,
                MAX(pnl) as best_trade,
                MIN(pnl) as worst_trade,
                SUM(CASE WHEN pnl > 0 THEN pnl ELSE 0 END) as total_wins_pnl,
                SUM(CASE WHEN pnl <= 0 THEN ABS(pnl) ELSE 0 END) as total_losses_pnl
            FROM trades
            WHERE status = 'closed' AND logic_type = ?
        """
        
        # Add time filter
        params = [plugin_id]
        if period == 'today':
            query += " AND DATE(close_time) = DATE('now')"
        elif period == 'week':
            query += " AND close_time >= DATE('now', '-7 days')"
        elif period == 'month':
            query += " AND close_time >= DATE('now', '-30 days')"
        
        cursor.execute(query, params)
        row = cursor.fetchone()
        
        if not row or row[0] == 0:
            return self._empty_plugin_stats(plugin_id)
        
        (trade_count, wins, losses, total_pnl, avg_trade, avg_win, avg_loss, 
         best_trade, worst_trade, total_wins_pnl, total_losses_pnl) = row
        
        win_rate = (wins / trade_count * 100) if trade_count > 0 else 0
        profit_factor = (total_wins_pnl / total_losses_pnl) if total_losses_pnl > 0 else 0
        
        return {
            'plugin_id': plugin_id,
            'period': period,
            'trade_count': trade_count or 0,
            'wins': wins or 0,
            'losses': losses or 0,
            'win_rate': round(win_rate, 2),
            'total_pnl': round(total_pnl or 0, 2),
            'avg_trade': round(avg_trade or 0, 2),
            'avg_win': round(avg_win or 0, 2),
            'avg_loss': round(avg_loss or 0, 2),
            'best_trade': round(best_trade or 0, 2),
            'worst_trade': round(worst_trade or 0, 2),
            'profit_factor': round(profit_factor, 2),
            'expectancy': round(avg_trade or 0, 2),  # Same as avg_trade
        }
    
    def get_all_plugins_performance(self, period: str = 'all') -> Dict[str, Dict[str, Any]]:
        """
        Get performance for all plugins
        
        Args:
            period: 'today', 'week', 'month', 'all'
            
        Returns:
            Dict mapping plugin_id to performance metrics
        """
        cursor = self.conn.cursor()
        
        # Get all distinct plugin IDs
        time_filter = ""
        if period == 'today':
            time_filter = " AND DATE(close_time) = DATE('now')"
        elif period == 'week':
            time_filter = " AND close_time >= DATE('now', '-7 days')"
        elif period == 'month':
            time_filter = " AND close_time >= DATE('now', '-30 days')"
        
        cursor.execute(f"""
            SELECT DISTINCT logic_type
            FROM trades
            WHERE status = 'closed' AND logic_type IS NOT NULL{time_filter}
        """)
        
        plugins = [row[0] for row in cursor.fetchall()]
        
        # Get performance for each plugin
        results = {}
        for plugin_id in plugins:
            results[plugin_id] = self.get_plugin_performance(plugin_id, period)
        
        return results
    
    def get_plugin_group_performance(self, plugin_prefix: str, period: str = 'all') -> Dict[str, Any]:
        """
        Get aggregated performance for plugin group (e.g., all V6 plugins)
        
        Args:
            plugin_prefix: 'v3' or 'v6' to filter plugins
            period: 'today', 'week', 'month', 'all'
            
        Returns:
            Aggregated stats for all matching plugins
        """
        cursor = self.conn.cursor()
        
        # Build time filter
        time_filter = ""
        if period == 'today':
            time_filter = " AND DATE(close_time) = DATE('now')"
        elif period == 'week':
            time_filter = " AND close_time >= DATE('now', '-7 days')"
        elif period == 'month':
            time_filter = " AND close_time >= DATE('now', '-30 days')"
        
        like_pattern = f"%{plugin_prefix}%"
        cursor.execute(f"""
            SELECT 
                COUNT(*) as trade_count,
                SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN pnl <= 0 THEN 1 ELSE 0 END) as losses,
                SUM(pnl) as total_pnl,
                AVG(pnl) as avg_trade,
                MAX(pnl) as best_trade,
                MIN(pnl) as worst_trade,
                SUM(CASE WHEN pnl > 0 THEN pnl ELSE 0 END) as total_wins_pnl,
                SUM(CASE WHEN pnl <= 0 THEN ABS(pnl) ELSE 0 END) as total_losses_pnl
            FROM trades
            WHERE status = 'closed' AND (logic_type LIKE ? OR logic_type LIKE ?){time_filter}
        """, (like_pattern, like_pattern.upper()))
        
        row = cursor.fetchone()
        if not row or row[0] == 0:
            return {'plugin_group': plugin_prefix, 'trade_count': 0}
        
        (trade_count, wins, losses, total_pnl, avg_trade, best_trade, worst_trade,
         total_wins_pnl, total_losses_pnl) = row
        
        win_rate = (wins / trade_count * 100) if trade_count > 0 else 0
        profit_factor = (total_wins_pnl / total_losses_pnl) if total_losses_pnl > 0 else 0
        
        return {
            'plugin_group': plugin_prefix,
            'period': period,
            'trade_count': trade_count or 0,
            'wins': wins or 0,
            'losses': losses or 0,
            'win_rate': round(win_rate, 2),
            'total_pnl': round(total_pnl or 0, 2),
            'avg_trade': round(avg_trade or 0, 2),
            'best_trade': round(best_trade or 0, 2),
            'worst_trade': round(worst_trade or 0, 2),
            'profit_factor': round(profit_factor, 2),
        }
    
    def compare_plugins(self, plugin_id_1: str, plugin_id_2: str, period: str = 'all') -> Dict[str, Any]:
        """
        Compare performance between two plugins
        
        Args:
            plugin_id_1: First plugin ID
            plugin_id_2: Second plugin ID
            period: 'today', 'week', 'month', 'all'
            
        Returns:
            Comparison metrics for both plugins
        """
        plugin_1 = self.get_plugin_performance(plugin_id_1, period)
        plugin_2 = self.get_plugin_performance(plugin_id_2, period)
        
        return {
            'plugin_1': plugin_1,
            'plugin_2': plugin_2,
            'comparison': {
                'trade_count_diff': plugin_1['trade_count'] - plugin_2['trade_count'],
                'pnl_diff': round(plugin_1['total_pnl'] - plugin_2['total_pnl'], 2),
                'win_rate_diff': round(plugin_1['win_rate'] - plugin_2['win_rate'], 2),
                'profit_factor_diff': round(plugin_1['profit_factor'] - plugin_2['profit_factor'], 2),
                'better_pnl': plugin_id_1 if plugin_1['total_pnl'] > plugin_2['total_pnl'] else plugin_id_2,
                'better_win_rate': plugin_id_1 if plugin_1['win_rate'] > plugin_2['win_rate'] else plugin_id_2,
            }
        }
    
    def get_v6_timeframe_breakdown(self, period: str = 'all') -> Dict[str, Dict[str, Any]]:
        """
        Get performance breakdown for all V6 timeframes
        
        Args:
            period: 'today', 'week', 'month', 'all'
            
        Returns:
            Dict mapping timeframe to performance metrics
        """
        v6_plugins = [
            'v6_price_action_1m',
            'v6_price_action_5m',
            'v6_price_action_15m',
            'v6_price_action_1h',
        ]
        
        timeframe_map = {
            'v6_price_action_1m': '1M',
            'v6_price_action_5m': '5M',
            'v6_price_action_15m': '15M',
            'v6_price_action_1h': '1H',
        }
        
        results = {}
        for plugin_id in v6_plugins:
            timeframe = timeframe_map.get(plugin_id, plugin_id)
            perf = self.get_plugin_performance(plugin_id, period)
            results[timeframe] = perf
        
        return results
    
    def get_v3_logic_breakdown(self, period: str = 'all') -> Dict[str, Dict[str, Any]]:
        """
        Get performance breakdown for V3 logics
        
        Args:
            period: 'today', 'week', 'month', 'all'
            
        Returns:
            Dict mapping logic to performance metrics
        """
        # V3 combined plugin tracks trades with logic_type 'v3_combined'
        # Individual logics might be tracked differently
        # This is a placeholder - adjust based on actual database structure
        
        v3_logic_types = [
            'v3_combined',
            'combinedlogic-1',
            'combinedlogic-2',
            'combinedlogic-3',
        ]
        
        results = {}
        for logic_type in v3_logic_types:
            perf = self.get_plugin_performance(logic_type, period)
            if perf['trade_count'] > 0:
                results[logic_type] = perf
        
        return results
    
    def get_plugin_daily_summary(self, plugin_id: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get daily performance summary for a plugin
        
        Args:
            plugin_id: Plugin identifier
            days: Number of days to retrieve
            
        Returns:
            List of daily performance dicts
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT 
                DATE(close_time) as trade_date,
                COUNT(*) as trade_count,
                SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                SUM(pnl) as total_pnl
            FROM trades
            WHERE status = 'closed' 
                AND logic_type = ?
                AND close_time >= DATE('now', ?)
            GROUP BY DATE(close_time)
            ORDER BY trade_date DESC
        """, (plugin_id, f'-{days} days'))
        
        results = []
        for row in cursor.fetchall():
            trade_date, trade_count, wins, total_pnl = row
            win_rate = (wins / trade_count * 100) if trade_count > 0 else 0
            results.append({
                'date': trade_date,
                'trade_count': trade_count or 0,
                'wins': wins or 0,
                'win_rate': round(win_rate, 2),
                'total_pnl': round(total_pnl or 0, 2),
            })
        
        return results
    
    # ==================== HELPER METHODS ====================
    
    def _empty_plugin_stats(self, plugin_id: str) -> Dict[str, Any]:
        """Return empty stats structure for plugin with no trades"""
        return {
            'plugin_id': plugin_id,
            'period': 'all',
            'trade_count': 0,
            'wins': 0,
            'losses': 0,
            'win_rate': 0,
            'total_pnl': 0,
            'avg_trade': 0,
            'avg_win': 0,
            'avg_loss': 0,
            'best_trade': 0,
            'worst_trade': 0,
            'profit_factor': 0,
            'expectancy': 0,
        }
