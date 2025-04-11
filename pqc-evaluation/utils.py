def one_level(df_all, level, graphics):
    for graphic in graphics:
        if level != graphic['level']:
            df_all = df_all.drop([i for i in graphic['mechanisms']])
    return df_all
