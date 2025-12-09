from stocktoolkit import (
    download_price_data,
    get_close_price,
    compute_returns,
    plot_price,
    plot_returns,
)

def main():
    df = download_price_data("AAPL", "2024-01-01", "2024-06-30")
    close = get_close_price(df)
    returns = compute_returns(close, method="simple")

    # Plot price with 20-day and 60-day MA
    plot_price(close, ma_windows=[20, 60], title="AAPL Price with MAs")

    # Plot returns
    plot_returns(returns, title="AAPL Daily Returns")


if __name__ == "__main__":
    main()