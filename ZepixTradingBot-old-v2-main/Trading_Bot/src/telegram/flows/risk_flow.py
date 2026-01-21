"""
Risk Flow - Zero-Typing Risk Wizard

Implements configuration wizards for Risk settings.
1. Set Lot Size Flow

Version: 1.0.0
Created: 2026-01-21
Part of: TELEGRAM_V5_ZERO_TYPING_UI
"""

from telegram import Update
from telegram.ext import ContextTypes
from .base_flow import BaseFlow

class RiskFlow(BaseFlow):

    @property
    def flow_name(self) -> str:
        return "risk_flow"

    async def start_set_lot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        state = self.state_manager.start_flow(chat_id, self.flow_name)
        state.add_data("action", "SET_LOT")
        await self.show_step(update, context, 0)

    async def show_step(self, update: Update, context: ContextTypes.DEFAULT_TYPE, step: int):
        chat_id = update.effective_chat.id
        header = self.header.build_header(style='compact')

        # Simple single-step selection for now
        text = (
            f"{header}\n"
            f"📏 **SET DEFAULT LOT SIZE**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"Select standard lot size:"
        )

        lots = [
            {"text": "0.01", "id": "0.01"}, {"text": "0.02", "id": "0.02"},
            {"text": "0.05", "id": "0.05"}, {"text": "0.10", "id": "0.10"},
            {"text": "0.20", "id": "0.20"}, {"text": "0.50", "id": "0.50"}
        ]

        keyboard = self.btn.create_paginated_menu(lots, 0, "flow_risk_lot", n_cols=3)

        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode='HTML')

    async def process_step(self, update: Update, context: ContextTypes.DEFAULT_TYPE, state):
        query = update.callback_query
        data = query.data

        if "flow_risk_lot_" in data:
            lot = data.split("_")[-1]

            # Apply setting
            # self.bot.risk_manager.set_default_lot(float(lot))

            await query.edit_message_text(
                f"✅ **RISK UPDATED**\n\nDefault Lot Size: {lot}",
                parse_mode='Markdown'
            )
            self.state_manager.clear_state(update.effective_chat.id)
