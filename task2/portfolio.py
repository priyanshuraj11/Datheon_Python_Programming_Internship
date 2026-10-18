"""
Investment Portfolio Tracker
----------------------------
Uses stock_list.csv (the attached stock-symbol directory) to validate symbols.
Current prices are fetched with yfinance when available. If online lookup fails,
the program asks for a current price manually.

Run:
    python portfolio.py

Optional live-price dependency:
    python -m pip install yfinance
"""

import csv
import os
from datetime import datetime
from decimal import Decimal, InvalidOperation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STOCK_FILE = os.path.join(BASE_DIR, "stock_list.csv")
SUMMARY_FILE = os.path.join(BASE_DIR, "portfolio_summary.csv")
TRANSACTION_LOG_FILE = os.path.join(BASE_DIR, "portfolio_transactions.csv")

SUMMARY_FIELDS = [
    "Timestamp", "Symbol", "Security", "Shares", "Buy Price",
    "Invested Amount", "Current Price", "Market Value",
    "Profit/Loss", "Return (%)"
]
TRANSACTION_FIELDS = [
    "Timestamp", "Symbol", "Security", "Shares", "Buy Price",
    "Current Price", "Invested Amount", "Market Value", "Profit/Loss", "Return (%)"
]


def load_stocks():
    """Load symbols and company names from stock_list.csv."""
    if not os.path.exists(STOCK_FILE):
        raise FileNotFoundError(
            f"Missing {STOCK_FILE}. Keep stock_list.csv in the same folder as portfolio.py."
        )

    stocks = {}
    with open(STOCK_FILE, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or "Symbol" not in reader.fieldnames:
            raise ValueError("stock_list.csv must contain a 'Symbol' column.")
        for row in reader:
            symbol = (row.get("Symbol") or "").strip().upper()
            security = (row.get("Security") or "").strip()
            if symbol:
                stocks[symbol] = security or symbol
    return stocks


def read_decimal(prompt, minimum=None):
    """Read a valid positive numeric value."""
    while True:
        value = input(prompt).strip().replace(",", "")
        try:
            number = Decimal(value)
            if not number.is_finite():
                raise InvalidOperation
            if minimum is not None and number < minimum:
                print(f"Value must be at least {minimum}.")
                continue
            return number
        except (InvalidOperation, ValueError):
            print("Please enter a valid number (for example: 125.50).")


def get_current_price(symbol):
    """Try yfinance first; request a manual price if unavailable."""
    try:
        import yfinance as yf  # Optional dependency
        ticker = yf.Ticker(symbol)
        price = ticker.fast_info.get("lastPrice")
        if price is None:
            history = ticker.history(period="5d", auto_adjust=False)
            if not history.empty:
                price = history["Close"].dropna().iloc[-1]
        if price is not None:
            current = Decimal(str(price))
            if current.is_finite() and current > 0:
                print(f"Fetched current price for {symbol}: {current:.2f}")
                return current
    except Exception as exc:
        print(f"Live price lookup unavailable for {symbol}: {exc}")

    print(f"Could not fetch a live price for {symbol}.")
    return read_decimal(f"Enter the current price for {symbol} manually: ", minimum=Decimal("0.000001"))


def write_csv(path, fieldnames, rows, append=False):
    """Write rows to a CSV, adding headers for a new/empty file."""
    file_exists = os.path.exists(path) and os.path.getsize(path) > 0
    mode = "a" if append else "w"
    with open(path, mode, newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not append or not file_exists:
            writer.writeheader()
        writer.writerows(rows)


def main():
    try:
        stocks = load_stocks()
    except (OSError, ValueError) as exc:
        print(f"Error loading stock list: {exc}")
        return

    print("\n=== Investment Portfolio Tracker ===")
    print("Enter one or more holdings. Type DONE when asked for the next ticker.")
    holdings = []
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

    while True:
        symbol = input("\nStock ticker (or DONE to finish): ").strip().upper()
        if symbol == "DONE":
            break
        if not symbol:
            print("Ticker cannot be empty.")
            continue
        if symbol not in stocks:
            print(f"{symbol} was not found in stock_list.csv. Check the ticker and try again.")
            continue

        buy_price = read_decimal("Buy price per share: ", minimum=Decimal("0.000001"))
        shares = read_decimal("Number of shares (fractional shares allowed): ", minimum=Decimal("0.000001"))
        current_price = get_current_price(symbol)

        invested = buy_price * shares
        market_value = current_price * shares
        profit_loss = market_value - invested
        return_pct = (profit_loss / invested) * Decimal("100") if invested else Decimal("0")

        holdings.append({
            "Timestamp": timestamp,
            "Symbol": symbol,
            "Security": stocks[symbol],
            "Shares": f"{shares:.6f}".rstrip("0").rstrip("."),
            "Buy Price": f"{buy_price:.2f}",
            "Invested Amount": f"{invested:.2f}",
            "Current Price": f"{current_price:.2f}",
            "Market Value": f"{market_value:.2f}",
            "Profit/Loss": f"{profit_loss:.2f}",
            "Return (%)": f"{return_pct:.2f}",
        })

    if not holdings:
        print("No holdings entered. No report was generated.")
        return

    total_invested = sum(Decimal(row["Invested Amount"]) for row in holdings)
    total_market_value = sum(Decimal(row["Market Value"]) for row in holdings)
    total_profit_loss = total_market_value - total_invested
    total_return = (total_profit_loss / total_invested * Decimal("100")) if total_invested else Decimal("0")

    print("\n=== Portfolio Summary ===")
    print(f"{'Symbol':<8} {'Shares':>10} {'Buy Price':>12} {'Current':>12} {'Market Value':>15} {'P/L':>12} {'Return':>10}")
    print("-" * 85)
    for row in holdings:
        print(
            f"{row['Symbol']:<8} {row['Shares']:>10} {row['Buy Price']:>12} "
            f"{row['Current Price']:>12} {row['Market Value']:>15} "
            f"{row['Profit/Loss']:>12} {row['Return (%)'] + '%':>10}"
        )
    print("-" * 85)
    print(f"Total invested:   {total_invested:.2f}")
    print(f"Current value:    {total_market_value:.2f}")
    print(f"Total profit/loss:{total_profit_loss:>12.2f}")
    print(f"Overall return:   {total_return:.2f}%")

    # Summary is replaced each run; transaction log keeps a history across runs.
    write_csv(SUMMARY_FILE, SUMMARY_FIELDS, holdings, append=False)
    write_csv(TRANSACTION_LOG_FILE, TRANSACTION_FIELDS, holdings, append=True)

    print(f"\nSummary saved to: {SUMMARY_FILE}")
    print(f"Transaction history appended to: {TRANSACTION_LOG_FILE}")


if __name__ == "__main__":
    main()
