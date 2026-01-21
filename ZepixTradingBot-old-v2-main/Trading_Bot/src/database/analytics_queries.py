"""
Analytics Query Module - Provides analytics data for Telegram commands

This module provides all analytics queries needed for the analytics commands:
- Performance statistics
- Plugin comparisons
- Time-based reports (daily/weekly/monthly)
- Symbol and strategy breakdowns
- Export data preparation

Version: 1.0.0
Date: 2026-01-20
"""

import sqlite3
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date, timedelta
from collections import defaultdict


class AnalyticsQueries:
    """
    Analytics query provider for trading bot statistics
    
    All queries work with the existing database schema from src/database.py
    """
    
    def __init__(self, db_connection: sqlite3.Connection):
        """
        Initialize analytics queries
        
        Args:
            db_connection: SQLite database connection from TradeDatabase
        """
        self.conn = db_connection
    
    # ==================== PERFORMANCE STATISTICS ====================
    
    def get_performance_stats(self, timeframe: str = 'all') -> Dict[str, Any]:
        """
        Get comprehensive performance statistics
        
        Args:
            timeframe: 'today', 'week', 'month', 'all'
            
        Returns:
            Dict with performance metrics
        """
        cursor = self.conn.cursor()
        
        # Base query
        base_query = """
            SELECT 
                COUNT(*) as total_trades,
                SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END) as losses,
                SUM(pnl) as total_pnl,
                AVG(pnl) as avg_pnl,
                AVG(CASE WHEN pnl > 0 THEN pnl END) as avg_win,
                AVG(CASE WHEN pnl < 0 THEN pnl END) as avg_loss,
                MAX(pnl) as best_trade,
                MIN(pnl) as worst_trade
            FROM trades
            WHERE status = 'closed'
        """
        
        # Add time filter
        if timeframe == 'today':
            base_query += " AND DATE(close_time) = DATE('now')"
        elif timeframe == 'week':
            base_query += " AND close_time >= DATE('now', '-7 days')"
        elif timeframe == 'month':
            base_query += " AND close_time >= DATE('now', '-30 days')"
        
        cursor.execute(base_query)
        row = cursor.fetchone()
        
        if not row or row[0] == 0:
            return self._empty_performance_stats()
        
        total_trades, wins, losses, total_pnl, avg_pnl, avg_win, avg_loss, best, worst = row
        
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        profit_factor = abs(wins * (avg_win or 0) / (losses * (avg_loss or 1))) if losses > 0 else 0
        
        # Get current streak
        streak_info = self._get_current_streak()
        
        # Get time-based PnL
        time_pnl = self._get_time_based_pnl()
        
        return {
            'total_trades': total_trades or 0,
            'wins': wins or 0,
            'losses': losses or 0,
            'win_rate': win_rate,
            'total_pnl': total_pnl or 0,
            'avg_pnl': avg_pnl or 0,
            'avg_win': avg_win or 0,
            'avg_loss': avg_loss or 0,
            'best_trade': best or 0,
            'worst_trade': worst or 0,
            'profit_factor': profit_factor,
            'current_streak': streak_info['current'],
            'streak_type': streak_info['type'],
            'best_streak': streak_info['best'],
            'worst_streak': streak_info['worst'],
            'today_pnl': time_pnl['today'],
            'week_pnl': time_pnl['week'],
            'month_pnl': time_pnl['month'],
            'lifetime_pnl': total_pnl or 0
        }
    
    def _empty_performance_stats(self) -> Dict[str, Any]:
        """Return empty performance stats"""
        return {
            'total_trades': 0, 'wins': 0, 'losses': 0, 'win_rate': 0,
            'total_pnl': 0, 'avg_pnl': 0, 'avg_win': 0, 'avg_loss': 0,
            'best_trade': 0, 'worst_trade': 0, 'profit_factor': 0,
            'current_streak': 0, 'streak_type': 'none', 'best_streak': 0,
            'worst_streak': 0, 'today_pnl': 0, 'week_pnl': 0, 'month_pnl': 0,
            'lifetime_pnl': 0
        }
    
    def _get_current_streak(self) -> Dict[str, Any]:
        """Calculate current win/loss streak"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT pnl FROM trades 
            WHERE status = 'closed' 
            ORDER BY close_time DESC 
            LIMIT 50
        """)
        
        recent_trades = [row[0] for row in cursor.fetchall()]
        
        if not recent_trades:
            return {'current': 0, 'type': 'none', 'best': 0, 'worst': 0}
        
        # Current streak
        current = 1
        streak_type = 'win' if recent_trades[0] > 0 else 'loss'
        
        for pnl in recent_trades[1:]:
            if (pnl > 0 and streak_type == 'win') or (pnl < 0 and streak_type == 'loss'):
                current += 1
            else:
                break
        
        # Best/worst streaks
        best_streak = 0
        worst_streak = 0
        temp_win = 0
        temp_loss = 0
        
        for pnl in recent_trades:
            if pnl > 0:
                temp_win += 1
                worst_streak = max(worst_streak, temp_loss)
                temp_loss = 0
            else:
                temp_loss += 1
                best_streak = max(best_streak, temp_win)
                temp_win = 0
        
        best_streak = max(best_streak, temp_win)
        worst_streak = max(worst_streak, temp_loss)
        
        return {
            'current': current,
            'type': streak_type,
            'best': best_streak,
            'worst': worst_streak
        }
    
    def _get_time_based_pnl(self) -> Dict[str, float]:
        """Get PnL for different timeframes"""
        cursor = self.conn.cursor()
        
        # Today
        cursor.execute("""
            SELECT COALESCE(SUM(pnl), 0) FROM trades 
            WHERE status = 'closed' AND DATE(close_time) = DATE('now')
        """)
        today = cursor.fetchone()[0]
        
        # Week
        cursor.execute("""
            SELECT COALESCE(SUM(pnl), 0) FROM trades 
            WHERE status = 'closed' AND close_time >= DATE('now', '-7 days')
        """)
        week = cursor.fetchone()[0]
        
        # Month
        cursor.execute("""
            SELECT COALESCE(SUM(pnl), 0) FROM trades 
            WHERE status = 'closed' AND close_time >= DATE('now', '-30 days')
        """)
        month = cursor.fetchone()[0]
        
        return {'today': today, 'week': week, 'month': month}
    
    # ==================== PLUGIN PERFORMANCE ====================
    
    def get_plugin_performance(self, plugin_id: str = None) -> Dict[str, Any]:
        """
        Get performance for specific plugin or all plugins
        
        Args:
            plugin_id: Specific plugin ID (e.g., 'v6_price_action_15m') or None for all
            
        Returns:
            Dict with plugin performance stats
        """
        cursor = self.conn.cursor()
        
        query = """
            SELECT 
                logic_type,
                COUNT(*) as trade_count,
                SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                SUM(pnl) as total_pnl,
                AVG(pnl) as avg_trade,
                MAX(pnl) as best_trade,
                MIN(pnl) as worst_trade
            FROM trades
            WHERE status = 'closed' AND logic_type IS NOT NULL
        """
        
        if plugin_id:
            query += " AND logic_type = ?"
            cursor.execute(query, (plugin_id,))
        else:
            query += " GROUP BY logic_type"
            cursor.execute(query)
        
        results = {}
        for row in cursor.fetchall():
            logic, count, wins, pnl, avg, best, worst = row
            if logic:
                results[logic] = {
                    'trade_count': count or 0,
                    'wins': wins or 0,
                    'win_rate': (wins / count * 100) if count > 0 else 0,
                    'total_pnl': pnl or 0,
                    'avg_trade': avg or 0,
                    'best_trade': best or 0,
                    'worst_trade': worst or 0,
                    'profit_factor': self._calc_profit_factor(logic)
                }
        
        return results if not plugin_id else results.get(plugin_id, {})
    
    def get_plugin_group_performance(self, plugin_prefix: str) -> Dict[str, Any]:
        """
        Get aggregated performance for plugin group (e.g., all V6 plugins)
        
        Args:
            plugin_prefix: 'v3' or 'v6' to filter plugins
            
        Returns:
            Aggregated stats for all matching plugins
        """
        cursor = self.conn.cursor()
        
        like_pattern = f"%{plugin_prefix}%"
        cursor.execute("""
            SELECT 
                COUNT(*) as trade_count,
                SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END) as losses,
                SUM(pnl) as total_pnl,
                AVG(pnl) as avg_trade,
                MAX(pnl) as max_dd
            FROM trades
            WHERE status = 'closed' AND (logic_type LIKE ? OR logic_type LIKE ?)
        """, (like_pattern, like_pattern.upper()))
        
        row = cursor.fetchone()
        if not row or row[0] == 0:
            return {}
        
        count, wins, losses, pnl, avg, max_dd = row
        
        return {
            'trade_count': count or 0,
            'wins': wins or 0,
            'losses': losses or 0,
            'win_rate': (wins / count * 100) if count > 0 else 0,
            'total_pnl': pnl or 0,
            'avg_trade': avg or 0,
            'max_drawdown': max_dd or 0,
            'profit_factor': abs((wins * avg) / ((losses * avg) or 1)) if losses > 0 else 0,
            'sharpe_ratio': 0  # Placeholder
        }
    
    def _calc_profit_factor(self, logic_type: str) -> float:
        """Calculate profit factor for a logic type"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN pnl > 0 THEN pnl ELSE 0 END) as total_profit,
                ABS(SUM(CASE WHEN pnl < 0 THEN pnl ELSE 0 END)) as total_loss
            FROM trades
            WHERE status = 'closed' AND logic_type = ?
        """, (logic_type,))
        
        profit, loss = cursor.fetchone()
        return (profit / loss) if loss and loss > 0 else 0
    
    # ==================== TIME-BASED REPORTS ====================
    
    def get_trades_for_date(self, target_date: date) -> List[Dict[str, Any]]:
        """Get all trades for a specific date"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM trades 
            WHERE DATE(close_time) = DATE(?) AND status = 'closed'
            ORDER BY close_time DESC
        """, (target_date.isoformat(),))
        
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_daily_summaries_last_n_days(self, days: int) -> List[Dict[str, Any]]:
        """Get daily summary for last N days"""
        summaries = []
        
        for i in range(days):
            target_date = date.today() - timedelta(days=i)
            trades = self.get_trades_for_date(target_date)
            
            if trades:
                total_pnl = sum(t['pnl'] for t in trades)
                wins = sum(1 for t in trades if t['pnl'] > 0)
                losses = sum(1 for t in trades if t['pnl'] < 0)
                
                summaries.append({
                    'date': target_date,
                    'trade_count': len(trades),
                    'wins': wins,
                    'losses': losses,
                    'win_rate': (wins / len(trades) * 100) if trades else 0,
                    'pnl': total_pnl,
                    'v3_pnl': sum(t['pnl'] for t in trades if t.get('logic_type', '').lower().startswith('v3')),
                    'v6_pnl': sum(t['pnl'] for t in trades if t.get('logic_type', '').lower().startswith('v6'))
                })
        
        return summaries
    
    def get_weekly_summary(self, start_date: date = None) -> Dict[str, Any]:
        """Get weekly summary starting from date"""
        if not start_date:
            start_date = date.today() - timedelta(days=date.today().weekday())
        
        end_date = start_date + timedelta(days=7)
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as trades,
                SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                SUM(pnl) as total_pnl,
                DATE(close_time) as day
            FROM trades
            WHERE status = 'closed' 
              AND DATE(close_time) >= DATE(?)
              AND DATE(close_time) < DATE(?)
            GROUP BY DATE(close_time)
            ORDER BY close_time
        """, (start_date.isoformat(), end_date.isoformat()))
        
        daily_breakdown = []
        for row in cursor.fetchall():
            trades, wins, pnl, day = row
            daily_breakdown.append({
                'day': day,
                'trades': trades,
                'wins': wins,
                'pnl': pnl,
                'win_rate': (wins / trades * 100) if trades else 0
            })
        
        # Get totals
        cursor.execute("""
            SELECT 
                COUNT(*) as total_trades,
                SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as total_wins,
                SUM(pnl) as total_pnl
            FROM trades
            WHERE status = 'closed' 
              AND DATE(close_time) >= DATE(?)
              AND DATE(close_time) < DATE(?)
        """, (start_date.isoformat(), end_date.isoformat()))
        
        total_row = cursor.fetchone()
        
        return {
            'start_date': start_date,
            'end_date': end_date,
            'total_trades': total_row[0] or 0,
            'total_wins': total_row[1] or 0,
            'total_pnl': total_row[2] or 0,
            'win_rate': (total_row[1] / total_row[0] * 100) if total_row[0] else 0,
            'daily_breakdown': daily_breakdown,
            'best_day': max(daily_breakdown, key=lambda x: x['pnl']) if daily_breakdown else None,
            'worst_day': min(daily_breakdown, key=lambda x: x['pnl']) if daily_breakdown else None
        }
    
    def get_monthly_summary(self, year: int = None, month: int = None) -> Dict[str, Any]:
        """Get monthly summary for year/month"""
        if not year:
            year = date.today().year
        if not month:
            month = date.today().month
        
        # Get first and last day of month
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        cursor = self.conn.cursor()
        
        # Overall stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total_trades,
                SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                SUM(pnl) as total_pnl,
                AVG(pnl) as avg_pnl,
                MAX(pnl) as best_trade,
                MIN(pnl) as worst_trade
            FROM trades
            WHERE status = 'closed' 
              AND DATE(close_time) >= DATE(?)
              AND DATE(close_time) < DATE(?)
        """, (start_date.isoformat(), end_date.isoformat()))
        
        stats = cursor.fetchone()
        
        # Weekly breakdown
        weekly_data = []
        current_week_start = start_date
        while current_week_start < end_date:
            week_end = min(current_week_start + timedelta(days=7), end_date)
            week_summary = self.get_weekly_summary(current_week_start)
            weekly_data.append(week_summary)
            current_week_start = week_end
        
        return {
            'year': year,
            'month': month,
            'total_trades': stats[0] or 0,
            'wins': stats[1] or 0,
            'total_pnl': stats[2] or 0,
            'avg_pnl': stats[3] or 0,
            'best_trade': stats[4] or 0,
            'worst_trade': stats[5] or 0,
            'win_rate': (stats[1] / stats[0] * 100) if stats[0] else 0,
            'weekly_breakdown': weekly_data
        }
    
    # ==================== SYMBOL & STRATEGY REPORTS ====================
    
    def get_pair_performance(self) -> Dict[str, Dict[str, Any]]:
        """Get performance breakdown by trading pair"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                symbol,
                COUNT(*) as trades,
                SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END) as losses,
                SUM(pnl) as total_pnl,
                AVG(pnl) as avg_pnl
            FROM trades
            WHERE status = 'closed' AND symbol IS NOT NULL
            GROUP BY symbol
            ORDER BY total_pnl DESC
        """)
        
        results = {}
        for row in cursor.fetchall():
            symbol, trades, wins, losses, pnl, avg = row
            results[symbol] = {
                'trades': trades or 0,
                'wins': wins or 0,
                'losses': losses or 0,
                'win_rate': (wins / trades * 100) if trades else 0,
                'pnl': pnl or 0,
                'avg': avg or 0
            }
        
        return results
    
    def get_strategy_performance(self) -> Dict[str, Dict[str, Any]]:
        """Get performance breakdown by strategy (logic type)"""
        return self.get_plugin_performance()
    
    def get_tp_reentry_stats(self) -> Dict[str, Any]:
        """Get TP re-entry statistics"""
        cursor = self.conn.cursor()
        
        # Get chains completed
        cursor.execute("""
            SELECT COUNT(*) FROM reentry_chains WHERE status = 'completed'
        """)
        chains_completed = cursor.fetchone()[0] or 0
        
        # Get level breakdown from trades
        cursor.execute("""
            SELECT 
                chain_level,
                COUNT(*) as entries,
                SUM(pnl) as level_pnl
            FROM trades
            WHERE is_re_entry = 1 AND status = 'closed'
            GROUP BY chain_level
            ORDER BY chain_level
        """)
        
        level_breakdown = {}
        total_reentry_pnl = 0
        
        for row in cursor.fetchall():
            level, entries, pnl = row
            level_breakdown[f'L{level}'] = {
                'entries': entries,
                'pnl': pnl or 0,
                'percentage': 0  # Will calculate later
            }
            total_reentry_pnl += (pnl or 0)
        
        # Calculate percentages
        if level_breakdown and chains_completed > 0:
            for level_key in level_breakdown:
                level_breakdown[level_key]['percentage'] = (
                    level_breakdown[level_key]['entries'] / chains_completed * 100
                )
        
        return {
            'chains_completed': chains_completed,
            'level_breakdown': level_breakdown,
            'total_reentry_pnl': total_reentry_pnl
        }
    
    # ==================== EXPORT DATA PREPARATION ====================
    
    def prepare_trades_export(self, days: int = 30) -> List[Dict[str, Any]]:
        """Prepare trade data for CSV export"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                open_time, symbol, direction, logic_type,
                entry_price, exit_price, pnl,
                CAST((exit_price - entry_price) * 10000 AS INTEGER) as pips,
                CAST((julianday(close_time) - julianday(open_time)) * 24 * 60 AS INTEGER) as duration_mins
            FROM trades
            WHERE status = 'closed' 
              AND close_time >= DATE('now', ?)
            ORDER BY close_time DESC
        """, (f'-{days} days',))
        
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def prepare_daily_summary_export(self, days: int = 30) -> List[Dict[str, Any]]:
        """Prepare daily summary data for CSV export"""
        return self.get_daily_summaries_last_n_days(days)
    
    # ==================== V6 SPECIFIC ANALYTICS ====================
    
    def get_v6_timeframe_performance(self) -> Dict[str, Dict[str, Any]]:
        """Get V6 Price Action performance breakdown by timeframe"""
        timeframes = ['15m', '30m', '1h', '4h']
        results = {}
        
        for tf in timeframes:
            # Match logic_type patterns for V6 timeframes
            pattern = f"%v6%{tf}%"
            
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as trade_count,
                    SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                    SUM(pnl) as total_pnl,
                    AVG(pnl) as avg_trade
                FROM trades
                WHERE status = 'closed' AND logic_type LIKE ?
            """, (pattern,))
            
            row = cursor.fetchone()
            if row and row[0] > 0:
                count, wins, pnl, avg = row
                results[tf] = {
                    'trade_count': count or 0,
                    'wins': wins or 0,
                    'win_rate': (wins / count * 100) if count else 0,
                    'total_pnl': pnl or 0,
                    'avg_trade': avg or 0
                }
        
        return results
