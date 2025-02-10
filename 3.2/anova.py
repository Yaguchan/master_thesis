import os
import pandas as pd
import pingouin as pg
import statsmodels.formula.api as smf
from scipy.stats import t
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm


# python 3.2/anova.py
OUTPUTDIR = '/Users/user/Desktop/授業/lab/資料/知覚実験/output_/test1'


def get_df(path):
    # output data
    names = os.listdir(path)
    names = [name for name in names if name != '.DS_Store']
    M = 800
    # output list
    data = {}
    # 要因
    # Subject       : 被験者番号
    # Sl            : 前/後
    # P             : 信号長
    # Length : 信号長
    # Delta         : 知覚可能な最小のずれ
    
    keys = ['Subject', 'Sl', 'P', 'Length', 'Delta']
    for key in keys:
        data[key] = []
    
    for i, name in enumerate(names):
        namedir = os.path.join(OUTPUTDIR, name)
        with open(os.path.join(namedir, f'output_test.txt'), 'r') as file:
            for line in file:
                sl, wavlen, P, delta = line.split(' ')
                sl, wavlen, P, delta = int(sl), int(wavlen), float(P), float(delta)
                for key, value in zip(keys, [i, sl, P, wavlen, delta]):
                    data[key].append(value)
    data = pd.DataFrame(data)
    data = data[data['Delta'] != -1]
    return data
    

def one_anova(data):
    aov = pg.rm_anova(
        dv='Delta',  # 従属変数
        within=['Sl', 'Length'],# 要因
        subject='Subject',  # 被験者ID
        data=data,
        detailed=True
    )
    print(aov)


# 二要因分散分析（Two-Way ANOVA）
def two_anova(data):
    formula = 'Delta ~ C(P) * C(Length)'
    model = ols(formula, data=data).fit()
    anova_results = anova_lm(model, typ=2)
    print(anova_results)
    return anova_results
    # 線形混合モデル
    # lmm = smf.mixedlm('Delta ~ C(P) + C(Length)', data, groups=data['Subject'])
    # lmm_result = lmm.fit()
    # print(lmm_result.summary())


# 三要因分散分析（Three-Way ANOVA）
def three_anova(data):
    formula = 'Delta ~ C(Sl) * C(P) * C(Length)'
    model = ols(formula, data=data).fit()
    anova_results = anova_lm(model, typ=2)
    print(anova_results)
    return anova_results


# LSD分析
def lsd_analysis(data, anova_table, factor, value_col):
    means = data.groupby(factor)[value_col].mean()
    n = data.groupby(factor).size().mean()
    mse = anova_table['sum_sq']['Residual'] / anova_table['df']['Residual']
    se = (2 * mse / n) ** 0.5
    df_residual = anova_table['df']['Residual']
    t_threshold = t.ppf(1 - 0.05 / 2, df_residual)
    lsd = t_threshold * se
    results = []
    for g1 in means.index:
        for g2 in means.index:
            if g1 < g2:
                mean_diff = abs(means[g1] - means[g2])
                significant = mean_diff > lsd
                results.append((g1, g2, mean_diff, significant))
    results_df = pd.DataFrame(results, columns=["Group1", "Group2", "Mean_Difference", "Significant"])
    print(results_df)


if __name__ == "__main__":
    df = get_df(OUTPUTDIR)
    df = df.dropna()
    anova_table = two_anova(df)
    # anova_table = three_anova(df)
    # lsd_analysis(df, anova_table, 'Sl', 'Delta')
    # lsd_analysis(df, anova_table, 'P', 'Delta')
    # lsd_analysis(df, anova_table, 'Length', 'Delta')