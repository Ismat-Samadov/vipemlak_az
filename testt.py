%%time
def predict_cashback_summary(df, days):
    # Create a copy of the DataFrame
    df = df.copy()
    df_2 = df.copy()


    # Drop unused columns
    columns_to_drop = ['TERMOWNER', 'ID', 'CURRENCY', 'NAME', 'MCC_DESCRIPTION', 'MCC', 'DIRECTION', 'PIN']
    df = df.drop(columns_to_drop, axis=1)

    # Replace null values with mode
    mode_values = df.mode().iloc[0]
    df = df.fillna(mode_values)

    # Convert date columns to datetime
    date_columns = ['HIREDATE', 'BIRTH_DATE', 'BANK_TIME']
    for column in date_columns:
        df[column] = pd.to_datetime(df[column])

    # Extract features from date columns
    current_date = pd.to_datetime('now').tz_localize(df['BANK_TIME'].dt.tz)
    df['HIREDATE_Time_diff'] = (current_date - df['HIREDATE']).dt.days
    df['HIREDATE_Hours'] = df['HIREDATE'].dt.hour
    df['HIREDATE_Weekday'] = df['HIREDATE'].dt.weekday
    df['HIREDATE_Year'] = df['HIREDATE'].dt.year
    df['HIREDATE_Day_of_Year'] = df['HIREDATE'].dt.dayofyear
    df['HIREDATE_Month'] = df['HIREDATE'].dt.month

    df['BIRTH_DATE_Time_diff'] = (current_date - df['BIRTH_DATE']).dt.days
    df['BIRTH_DATE_Hours'] = df['BIRTH_DATE'].dt.hour
    df['BIRTH_DATE_Weekday'] = df['BIRTH_DATE'].dt.weekday
    df['BIRTH_DATE_Year'] = df['BIRTH_DATE'].dt.year
    df['BIRTH_DATE_Day_of_Year'] = df['BIRTH_DATE'].dt.dayofyear
    df['BIRTH_DATE_Month'] = df['BIRTH_DATE'].dt.month

    df['BANK_TIME_Time_diff'] = (current_date - df['BANK_TIME']).dt.days
    df['BANK_TIME_Hours'] = df['BANK_TIME'].dt.hour
    df['BANK_TIME_Weekday'] = df['BANK_TIME'].dt.weekday
    df['BANK_TIME_Year'] = df['BANK_TIME'].dt.year
    df['BANK_TIME_Day_of_Year'] = df['BANK_TIME'].dt.dayofyear
    df['BANK_TIME_Month'] = df['BANK_TIME'].dt.month

    # Drop date columns
    df = df.drop(date_columns, axis=1)

    # Encode 'MARSTAT' and 'MCC_GROUP' columns as dummy variables
    df = pd.get_dummies(df, columns=['MARSTAT', 'MCC_GROUP'], drop_first=True)

    # Split the data into features (X) and target (y)
    X = df.drop('CASHBACK_AMOUNT', axis=1)
    y = df['CASHBACK_AMOUNT']

    # Initialize the Random Forest model
    model = RandomForestRegressor()

    # Fit the model on the data
    model.fit(X, y)

    # Predict cashback amounts for the next 'days' days
    future_dates = pd.date_range(df_2['BANK_TIME'].max(), periods=days, freq='D')
    future_features = pd.DataFrame(index=future_dates, columns=X.columns)
    future_features.fillna(0, inplace=True)
    future_cashback = model.predict(future_features)

    return future_cashback