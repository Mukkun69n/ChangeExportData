import sys

import pandas as pd

#pathの設定
export_file_path = sys.argv[1]
change_export_file_path = sys.argv[2]

print(sys.argv[0])
print(sys.argv[1])

#エクスポートされたファイルを読み込む
df_export_data = pd.read_csv(export_file_path, encoding='shift-jis')

#変換後のエクスポートデータ
df_result_data = df_export_data

#同じ値を格納する列の列名と値の辞書
col_v_dic = {'収支区分': '収入', '勘定科目': '雑収入', '税区分': '課税売上10%', '取引先': 'ココナラ', '部門': '請負'}

#同じ値を格納する列を追加
for col_name, v in col_v_dic.items():
    df_result_data[col_name] = v

#result_data内をインポートできる形に変換していく
#1.列名の変更
df_result_data.rename(columns = {'売上確定日': '発生日', '売上金額': '金額'}, inplace = True)

#2.備考列を追加
df_result_data['トークルームNo'] = df_result_data.トークルームNo.astype(str)
df_result_data['購入者ID'] = df_result_data.購入者ID.astype(str)
df_result_data['備考'] = df_result_data['種別'].str.cat(
    [df_result_data['トークルームNo'], df_result_data['サービス名'],
    df_result_data['購入者ID'], df_result_data['購入者名'], df_result_data['内訳']],
    sep=',')

#3.必要のない列を削除
df_result_data.drop(columns = ['種別', 'トークルームNo', 'サービス名', '購入者ID', '購入者名', '内訳', '振込状況'], inplace = True)

#4.整列
df_result_data = df_result_data.loc[:, ['発生日', '収支区分', '勘定科目', '金額', '税区分', '取引先', '部門', '備考']]

#ファイルの書き込み
df_result_data.to_excel(change_export_file_path, index = False)

print('【終了】ファイルの書き込みが完了しました。')
