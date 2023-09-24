

def minPivotPoints(prices, length_left=10, length_right=10):
    if len(prices) == 0:
        return []

    pivot_points = []
    for i in range(length_left, len(prices) - length_right - 1):
        local_min = min(prices[i - length_left: i + length_right])
        if prices[i] == local_min:
            pivot_points.append(i)

    # remove duplicate pivot points
    tmp = pivot_points.copy()
    for i in range(len(tmp) - 1):
        if tmp[i + 1] - tmp[i] < length_right:
            del pivot_points[i + 1]

    return pivot_points


def highPivotPoints(prices, length_left=10, length_right=10):
    if len(prices) == 0:
        return []

    pivot_points = []
    for i in range(length_left, len(prices) - length_right - 1):
        local_max = max(prices[i - length_left: i + length_right])
        if prices[i] == local_max:
            pivot_points.append(i)

    # remove duplicate pivot points
    tmp = pivot_points.copy()
    for i in range(len(tmp) - 1):
        if tmp[i + 1] - tmp[i] < length_right:
            del pivot_points[i + 1]

    return pivot_points


# Pivot low : [[row,pivot_low_price],[]...[]]
def get_low_pivot_row_and_price(df):
    res = []
    for index, row in df.iterrows():
        if (row['pivot_point_low']):
            res.append([index, row['low']])
    return res


def get_high_pivot_row_and_price(df):
    res = []
    for index, row in df.iterrows():
        if (row['pivot_point_high']):
            res.append([index, row['high']])
    return res


def low_pivot_win_loss(df, pivot):
    pivot_index = pivot[0]
    pivot_price = pivot[1]
    print(f"Pivot index is {pivot_index}")
    bought = False
    for index, row in df.iloc[pivot_index+1:].iterrows():
        if not bought and row['low'] < pivot_price:
            print(
                f"Bought at {row['timestamp']} for price:{pivot_price} index:{index}")
            bought = True
            if pivot_price*0.98 > row['low']:
                print(
                    f"Stop loss(2%) triggered at {row['timestamp']} sold for price:{pivot_price*0.98}")
                return ['Loss', index]
            if row['high'] > pivot_price*1.02:
                print(
                    f"Sold with profit(2%) {row['timestamp']} for price:{pivot_price*1.02}")
                return ['Win', index]
        if bought:
            if pivot_price*0.98 > row['low']:
                print(
                    f"Stop loss(2%) triggered at {row['timestamp']} sold for price:{pivot_price*0.98}")
                return ['Loss', index]
            if row['high'] > pivot_price*1.02:
                print(
                    f"Sold with profit(2%) {row['timestamp']} for price:{pivot_price*1.02}")
                return ['Win', index]
    return ['Neutral', 0]
