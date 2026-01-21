"""
Trading Flow - Zero-Typing Buy/Sell Wizard

Implements the 4-step wizard for placing trades.
1. Symbol Selection
2. Direction (if not started with specific command)
3. Lot Size Selection
4. Confirmation

Version: 1.0.0
Created: 2026-01-21
Part of: TELEGRAM_V5_ZERO_TYPING_UI
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from .base_flow import BaseFlow

class TradingFlow(BaseFlow):

    @property
    def flow_name(self) -> str:
        return "trading_flow"

    async def start_buy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        state = self.state_manager.start_flow(chat_id, self.flow_name)
        state.add_data("direction", "BUY")
        await self.show_step(update, context, 0)

    async def start_sell(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        state = self.state_manager.start_flow(chat_id, self.flow_name)
        state.add_data("direction", "SELL")
        await self.show_step(update, context, 0)

    async def show_step(self, update: Update, context: ContextTypes.DEFAULT_TYPE, step: int):
        chat_id = update.effective_chat.id
        state = self.state_manager.get_state(chat_id)
        direction = state.get_data("direction", "TRADE")

        header = self.header.build_header(style='compact')

        if step == 0:
            # Step 1: Symbol Selection
            text = (
                f"{header}\n"
                f"📊 **{direction} WIZARD (Step 1/3)**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Select a symbol to trade:"
            )

            # Common symbols
            symbols = [
                {"text": "EURUSD", "id": "EURUSD"}, {"text": "GBPUSD", "id": "GBPUSD"},
                {"text": "USDJPY", "id": "USDJPY"}, {"text": "XAUUSD", "id": "XAUUSD"},
                {"text": "AUDUSD", "id": "AUDUSD"}, {"text": "USDCAD", "id": "USDCAD"}
            ]

            keyboard = self.btn.create_paginated_menu(symbols, 0, "flow_trade_sym", n_cols=2)

        elif step == 1:
            # Step 2: Lot Size
            symbol = state.get_data("symbol")
            text = (
                f"{header}\n"
                f"📊 **{direction} {symbol} (Step 2/3)**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Select lot size:"
            )

            lots = [
                {"text": "0.01", "id": "0.01"}, {"text": "0.02", "id": "0.02"},
                {"text": "0.05", "id": "0.05"}, {"text": "0.10", "id": "0.10"},
                {"text": "0.20", "id": "0.20"}, {"text": "0.50", "id": "0.50"}
            ]

            keyboard = self.btn.create_paginated_menu(lots, 0, "flow_trade_lot", n_cols=3)

        elif step == 2:
            # Step 3: Confirmation
            symbol = state.get_data("symbol")
            lot = state.get_data("lot")

            text = (
                f"{header}\n"
                f"⚠️ **CONFIRM ORDER**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"**Type:** {direction}\n"
                f"**Symbol:** {symbol}\n"
                f"**Size:** {lot} lots\n\n"
                f"Proceed?"
            )

            keyboard = self.btn.create_confirmation_menu("flow_trade_confirm", "flow_trade_cancel")

        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode='HTML')
        else:
            await self.bot.send_message(text, reply_markup=keyboard)

    async def process_step(self, update: Update, context: ContextTypes.DEFAULT_TYPE, state):
        query = update.callback_query
        data = query.data

        if "flow_trade_sym_" in data:
            symbol = data.split("_")[-1]
            state.add_data("symbol", symbol)
            state.next_step()
            await self.show_step(update, context, 1)

        elif "flow_trade_lot_" in data:
            lot = data.split("_")[-1]
            state.add_data("lot", lot)
            state.next_step()
            await self.show_step(update, context, 2)

        elif "flow_trade_confirm" in data:
            # Execute Trade
            symbol = state.get_data("symbol")
            lot = state.get_data("lot")
            direction = state.get_data("direction")

            # Call trading engine
            # mock execution for now
            if hasattr(self.bot, 'trading_engine') and self.bot.trading_engine:
                # self.bot.trading_engine.place_trade(...)
                pass

            await query.edit_message_text(
                f"✅ **ORDER EXECUTED**\n\n{direction} {symbol} ({lot} lots)\n\nTicket: #12345678",
                parse_mode='Markdown'
            )
            self.state_manager.clear_state(update.effective_chat.id)

        elif "flow_trade_cancel" in data:
            await self.cancel(update, context)
