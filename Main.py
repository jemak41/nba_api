from nba_api.stats.endpoints import playerfantasyprofile as pfp
import pandas as pd

lis = ['203507','203078', '202355', '204060', '1629027', '201144', '202326', '203471', '203939']
lis2 = ['1627732','202711', '202331', '201599', '203095', '1628398', '201950', '1628367', '203473']

def cleanse(df):
    df = df.drop(columns=['GROUP_SET',
                          'GROUP_VALUE',
                          'W',
                          'L',
                          'W_PCT',
                          'MIN',
                          'OREB',
                          'DREB',
                          'BLKA',
                          'PF',
                          'PFD',
                          'PLUS_MINUS',
                          'DD2',
                          'TD3',
                          'FAN_DUEL_PTS',
                          'NBA_FANTASY_PTS',
                          'FG3A',
                          'FG3_PCT',
                          'FGM',
                          'FTM'
                          ])
    df.insert(2, 'FGAPG', df.FGA / df.GP)
    df.insert(7, '3PTMPG', df.FG3M / df.GP)
    df.insert(4, 'FTAPG', df.FTA/ df.GP)
    df.insert(9, 'RPG', df.REB / df.GP)
    df.insert(11, 'APG', df.AST / df.GP)
    df.insert(16, 'TOPG', df.TOV / df.GP)
    df.insert(13, 'SPG', df.STL / df.GP)
    df.insert(15, 'BPG', df.BLK / df.GP)
    df.insert(8, 'PPG', df.PTS / df.GP)
    df = df.drop(columns=['PTS',
                          'AST',
                          'REB',
                          'BLK',
                          'STL',
                          'TOV',
                          'FGA',
                          'FG3M',
                          'GP',
                          'FTA'
                          ])
    return df

def cleanseSomeMore(df_final):

    #FIELD GOALS
    df_final.insert(1, 'TotalFGA', df_final.FGAPG.sum())
    df_final.insert(2, 'FGAPCT', df_final.FGAPG / df_final.TotalFGA)
    df_final.insert(3, 'FGAPCT_Cont', df_final.FGAPCT * df_final.FG_PCT)

    #FREE THROWS
    df_final.insert(7, 'TotalFTA', df_final.FTAPG.sum())
    df_final.insert(8, 'FTAPCT', df_final.FTAPG / df_final.TotalFTA)
    df_final.insert(9, 'FTAPCT_Cont', df_final.FTAPCT * df_final.FT_PCT)

    df_final = df_final.drop(columns=['FGAPG',
                           'TotalFGA',
                           'FGAPCT',
                           'FG_PCT',
                           'FTAPG',
                           'FT_PCT',
                           'TotalFTA',
                           'FTAPCT'])
    cols = list(df_final)

    df = pd.DataFrame(columns = cols)

    df = df.append(df_final.sum(axis=0),ignore_index=True)

    return df

def main():

    df_final = pd.DataFrame()
    df_opponent = pd.DataFrame()

    for x in range(len(lis)):
        df_final = df_final.append(cleanse(pfp.PlayerFantasyProfile(lis[x]).get_data_frames()[0]), ignore_index=True)

    for x in range(len(lis2)):
        df_opponent = df_opponent.append(cleanse(pfp.PlayerFantasyProfile(lis2[x]).get_data_frames()[0]), ignore_index=True)

    print(df_final)
    print(df_opponent)

    df_final = cleanseSomeMore(df_final)
    df_opponent = cleanseSomeMore(df_opponent)

    print(df_final)
    print(df_opponent)

if __name__ == '__main__':
    main()