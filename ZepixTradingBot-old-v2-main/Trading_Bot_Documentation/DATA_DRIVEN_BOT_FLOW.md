# ZEPIX BOT: DATA-DRIVEN LOGIC FLOW (PINE PAYLOADS)

Ye document dikhata hai ki kaise **Pine Script ka Data** hi final decision maker hai. Bot ko calculations nahi, bas **Parsing** karni hai.

---

## 🌳 1. THE DATA PACKET (What Pine Sends)

Jab Pine Script `alert()` trigger karta hai, wo yeh Data Packet bhejta hai:

**`BULLISH_ENTRY|EURUSD|60|1.0850|BUY|HIGH|85|28.5|TRENDING|1.0800|1.0900|1.0950|1.1000|3/0|TL_OK`**

Is packet mein sab kuch hai:
1.  **Action:** `BULLISH_ENTRY`
2.  **Symbol:** `EURUSD`
3.  **Confidence:** `HIGH` (Score: 85)
4.  **Trend:** `TRENDING` (ADX: 28.5)
5.  **Risk:** `SL=1.0800`, `TP1=1.0900`
6.  **Multi-Timeframe:** `3/0` (3 TF Bullish aligned)

---

## 🌳 2. BOT'S JOB: "READ & EXECUTE"

Bot ka kaam sirf is packet ko padhna hai.

```mermaid
graph TD
    %% --- SIGNAL SOURCE ---
    PINE[🧠 PINE SCRIPT ALERT] -->|Send Pipe-Separated Data| WEBHOOK[📨 WEBHOOK RECEIVER]

    %% --- PARSING LAYER ---
    WEBHOOK -->|Raw String| PARSER[🔍 SIGNAL PARSER]
    PARSER -->|Extract: Confidence=85| VAR_CONF[Variable: Conf]
    PARSER -->|Extract: ADX=28.5| VAR_ADX[Variable: ADX]
    PARSER -->|Extract: TP/SL| VAR_RISK[Variable: Risk]

    %% --- DECISION LAYER (NO CALCULATIONS) ---
    subgraph "BOT DECISION (Simple Inspection)"
        VAR_CONF --> CHECK_CONF{Confidence > 60?}
        VAR_ADX --> CHECK_ADX{ADX Strength == 'TRENDING'?}
        
        CHECK_CONF -- YES --> PASS_1[✅ Pass]
        CHECK_ADX -- YES --> PASS_2[✅ Pass]
    end

    %% --- EXECUTION LAYER ---
    PASS_1 & PASS_2 --> EXECUTE[🚀 PLACE ORDER (Use Packet SL/TP)]
```

---

## 🌳 3. WHY THIS IS BETTER?

| Feature | **OLD (Devin's Implementation)** | **NEW (Data-Driven)** |
|:---|:---|:---|
| **ADX Source** | Bot calculates using Python (Slow/Delayed) | **Pine Data (Immediate & Synced)** |
| **Trend Source** | Bot checks internal `TrendManager` | **Pine Data (Actual Signal Context)** |
| **Risk Levels** | Bot recalculates ATR | **Pine Data (Visual SL/TP on Chart)** |
| **Conclusion** | **Mismatch Risk High** | **0% Mismatch (What you see is what you get)** |

---

## 🌳 4. COMPLETE LIST OF RECOGNIZED ALERTS

Bot in 14 Alerts ko pehchanega aur unke data ke hisab se act karega.

1.  **Entries:** `BULLISH_ENTRY`, `BEARISH_ENTRY` (Trade Lo)
2.  **Exits:** `EXIT_BULLISH`, `EXIT_BEARISH` (Trade Kaato)
3.  **Trend Info:** `TREND_PULSE`, `MOMENTUM_CHANGE`, `STATE_CHANGE` (Internal State Update karo - Re-entry ke liye)
4.  **Setups:** `BREAKOUT`, `BREAKDOWN`, `SCREENER_*` (Notifications Only / Watchlist Update)

---

Ye architecture ensure karti hai ki **Bot wahi kare jo Pine Script chart par dikha raha hai.**
