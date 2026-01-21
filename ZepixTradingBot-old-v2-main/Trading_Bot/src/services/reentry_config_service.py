"""
Re-entry Config Service - Per-Plugin Configuration Management
Version: 1.0.0
Date: 2026-01-21

Provides per-plugin re-entry configuration management with fallback to global settings.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ReentryConfigService:
    """Service for per-plugin re-entry configuration management"""
    
    def __init__(self, config):
        """
        Initialize service with config object.
        
        Args:
            config: Config object with get() and update_nested() methods
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.logger.info("[ReentryConfigService] Initialized")
    
    def is_tp_continuation_enabled(self, plugin_id: str) -> bool:
        """
        Check if TP continuation enabled for plugin.
        
        Args:
            plugin_id: 'v3_combined' or 'v6_price_action'
        
        Returns:
            bool: True if enabled
        """
        # Check per-plugin config first
        per_plugin = self.config.get("re_entry_config", {}) \
            .get("per_plugin", {}) \
            .get(plugin_id, {}) \
            .get("tp_continuation", {}) \
            .get("enabled")
        
        if per_plugin is not None:
            return per_plugin
        
        # Fallback to global
        return self.config.get("re_entry_config", {}) \
            .get("global", {}) \
            .get("tp_reentry_enabled", 
                 self.config.get("re_entry_config", {}).get("tp_reentry_enabled", True))
    
    def is_sl_hunt_enabled(self, plugin_id: str) -> bool:
        """
        Check if SL hunt enabled for plugin.
        
        Args:
            plugin_id: 'v3_combined' or 'v6_price_action'
        
        Returns:
            bool: True if enabled
        """
        # Check per-plugin config first
        per_plugin = self.config.get("re_entry_config", {}) \
            .get("per_plugin", {}) \
            .get(plugin_id, {}) \
            .get("sl_hunt_recovery", {}) \
            .get("enabled")
        
        if per_plugin is not None:
            return per_plugin
        
        # Fallback to global
        return self.config.get("re_entry_config", {}) \
            .get("global", {}) \
            .get("sl_hunt_reentry_enabled",
                 self.config.get("re_entry_config", {}).get("sl_hunt_reentry_enabled", True))
    
    def is_exit_continuation_enabled(self, plugin_id: str) -> bool:
        """
        Check if exit continuation enabled for plugin.
        
        Args:
            plugin_id: 'v3_combined' or 'v6_price_action'
        
        Returns:
            bool: True if enabled
        """
        # Check per-plugin config first
        per_plugin = self.config.get("re_entry_config", {}) \
            .get("per_plugin", {}) \
            .get(plugin_id, {}) \
            .get("exit_continuation", {}) \
            .get("enabled")
        
        if per_plugin is not None:
            return per_plugin
        
        # Fallback to global
        return self.config.get("re_entry_config", {}) \
            .get("global", {}) \
            .get("exit_continuation_enabled",
                 self.config.get("re_entry_config", {}).get("exit_continuation_enabled", True))
    
    def toggle_feature(
        self,
        plugin_id: str,
        feature_type: str,  # 'tp_continuation', 'sl_hunt_recovery', 'exit_continuation'
        new_value: Optional[bool] = None
    ) -> bool:
        """
        Toggle re-entry feature for plugin.
        
        Args:
            plugin_id: Plugin identifier ('v3_combined' or 'v6_price_action')
            feature_type: Feature to toggle
            new_value: Force specific value (None = toggle current)
        
        Returns:
            New value
        """
        # Get current value
        if feature_type == 'tp_continuation':
            current = self.is_tp_continuation_enabled(plugin_id)
        elif feature_type == 'sl_hunt_recovery':
            current = self.is_sl_hunt_enabled(plugin_id)
        elif feature_type == 'exit_continuation':
            current = self.is_exit_continuation_enabled(plugin_id)
        else:
            raise ValueError(f"Invalid feature type: {feature_type}")
        
        # Determine new value
        target_value = not current if new_value is None else new_value
        
        # Ensure per_plugin structure exists
        if "re_entry_config" not in self.config.config:
            self.config.config["re_entry_config"] = {}
        
        if "per_plugin" not in self.config.config["re_entry_config"]:
            self.config.config["re_entry_config"]["per_plugin"] = {}
        
        if plugin_id not in self.config.config["re_entry_config"]["per_plugin"]:
            self.config.config["re_entry_config"]["per_plugin"][plugin_id] = {}
        
        if feature_type not in self.config.config["re_entry_config"]["per_plugin"][plugin_id]:
            self.config.config["re_entry_config"]["per_plugin"][plugin_id][feature_type] = {}
        
        # Update config
        self.config.config["re_entry_config"]["per_plugin"][plugin_id][feature_type]["enabled"] = target_value
        
        # Save config
        if hasattr(self.config, 'save_config'):
            self.config.save_config()
        
        self.logger.info(
            f"[ReentryConfigService] Toggle: {plugin_id} > {feature_type} → {target_value}"
        )
        
        return target_value
    
    def get_plugin_status(self, plugin_id: str) -> Dict[str, Any]:
        """
        Get all re-entry settings for a plugin.
        
        Args:
            plugin_id: Plugin identifier
        
        Returns:
            Dict with status of all features
        """
        return {
            'tp_continuation': {
                'enabled': self.is_tp_continuation_enabled(plugin_id),
                'config': self.config.get("re_entry_config", {}) \
                    .get("per_plugin", {}) \
                    .get(plugin_id, {}) \
                    .get("tp_continuation", {})
            },
            'sl_hunt_recovery': {
                'enabled': self.is_sl_hunt_enabled(plugin_id),
                'config': self.config.get("re_entry_config", {}) \
                    .get("per_plugin", {}) \
                    .get(plugin_id, {}) \
                    .get("sl_hunt_recovery", {})
            },
            'exit_continuation': {
                'enabled': self.is_exit_continuation_enabled(plugin_id),
                'config': self.config.get("re_entry_config", {}) \
                    .get("per_plugin", {}) \
                    .get(plugin_id, {}) \
                    .get("exit_continuation", {})
            }
        }
    
    def get_global_overview(self) -> Dict[str, Any]:
        """
        Get overview of all plugins' re-entry settings.
        
        Returns:
            Dict with all plugin statuses
        """
        return {
            'v3_combined': self.get_plugin_status('v3_combined'),
            'v6_price_action': self.get_plugin_status('v6_price_action')
        }
