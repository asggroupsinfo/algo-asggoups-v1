# ZEPIX BOT: SIMPLE WORKING FLOW (TREE DIAGRAM)

Ye document explain karta hai ki **Bot kaise sochta hai aur kaam karta hai** jab TradingView se signal aata hai.

---

## 🌳 1. SIGNAL AAYA (Signal Received)

Jab TradingView "Alert" bhejta hai, toh Bot ka pehla reaction:

```text
🌎 TRADINGVIEW (External World)
      │
      │ (Signal packet bheja) 📨
      ▼
🛑 BOT SERVER (Gatekeeper)
      │
      ├── "Signal kiska hai?" (Identification)
      │
      ├── Case A: "V3 COMBINED" likha hai? ───►  Jao Rasta #1 (V3 Lane)
      │
      └── Case B: "V6 PRICE ACTION" hai? ────►  Jao Rasta #2 (V6 Lane)
```

---

## 🌳 2. IMPOTANT DECISION (Router Logic)

Ab signal apne-apne "Plugin" (Dimaag) ke paas jata hai logic check karne.

### **Rasta #1: V3 Logic (Aggressive)**

```text
🚀 V3 LANE (Combined Logic)
      │
      ▼
🤔 SHART #1: "Kya Consensus Score > 5 hai?"
      │
      ├── ❌ NO (Score 3) ────► STOP (Trade mat lo) 🛑
      │
      └── ✅ YES (Score 8) ───► PROFIT! (Aage badho)
            │
            ▼
🤔 SHART #2: "Kya Trend Validation Pass hua?"
            │
            ├── ❌ NO ────► STOP 🛑
            │
            └── ✅ YES ───► FINAL STEP (Order Calculation)
                  │
                  ▼
📦 ORDER PREPARATION (V3 Style)
      │
      ├── Order A: "TP tak targets lo" (Safe)
      └── Order B: "Profit ko run karne do" (Risky)
```

### **Rasta #2: V6 Logic (Price Action)**

```text
🏎️ V6 LANE (Price Action Logic)
      │
      ▼
🤔 SHART #1: "Kya market Trend mein hai?" (ADX Check)
      │
      ├── ❌ NO (ADX < 15) ───► STOP (Market slow hai) 🛑
      │
      └── ✅ YES (ADX > 25) ──► PROFIT! (Aage badho)
            │
            ▼
🤔 SHART #2: "Kya Higher Timeframe match kar raha hai?"
            │
            ├── ❌ NO ────► STOP 🛑
            │
            └── ✅ YES ───► FINAL STEP (Order Calculation)
                  │
                  ▼
📦 ORDER PREPARATION (V6 Style)
      │
      └── Order A: "Single strong entry" (High Risk, 1.5x)
```

---

## 🌳 3. EXECUTION (Order Lagana)

Ab Bot finally MT5 (Trading Platform) ko order deta hai.

```text
🛠️ SERVICE API (The Hand that Trades)
      │
      │ (Dono orders ek saath handle kar sakta hai)
      │
      ├── 📥 V3 Order Request (BUY EURUSD)
      │     │
      │     └──👉 MT5 mein TICKET #101 generate hua ✅
      │
      └── 📥 V6 Order Request (SELL EURUSD) - (Hedging allowed)
            │
            └──👉 MT5 mein TICKET #102 generate hua ✅
```

---

## 🌳 4. RESULT (Notification)

Aapko mobile pe kya dikhega?

```text
📱 TELEGRAM NOTIFICATIONS
      │
      ├── 🔔 Tring! (V3 Alert)
      │     "✅ BUY EURUSD Executed (V3 Strategy)"
      │     "Risk: Low | Score: 8/10"
      │
      └── 🔔 Tring! (V6 Alert)
            "⚡ SELL EURUSD Executed (V6 1H Swing)"
            "Risk: High (1.5x) | Trend: Strong"
```

---

## 📝 SUMMARY TABLE (Antar Kya Hai?)

| Feature | V3 Lane (Rasta #1) | V6 Lane (Rasta #2) |
|---------|-------------------|-------------------|
| **Pehchan (ID)** | `v3_combined` | `v6_price_action` |
| **Shart (Condition)** | Consensus Score (Voting) | ADX (Trend Strength) |
| **Orders** | 2 Orders (Dual) | 1 Order (Single) |
| **Main Focus** | Consistency | Big Moves |

---

Bot basically ek **Smart Manager** hai—wo har signal ko uske sahi department (V3 ya V6) mein bhejta hai, rules check karta hai, aur sirf tabhi trade lagata hai jab sab kuch perfect ho.
