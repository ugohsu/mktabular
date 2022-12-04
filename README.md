# mktabular

## SYNOPSIS

```
mktabular [-n MIDNUM] [-d] [--align ALIGN]
```

## DESCRIPTION

標準入力から読み込んだ文字列データ (区切り文字は原則として "\t") を LaTeX tabular 形式に変換し、標準出力に書き込む。

下線等は booktabs.sty の toprule, midrule, cmidrule, bottomrule を採用するため、LaTeX プリアンブルで同パッケージをインポートしておく必要がある。

各列の揃え方は、基本的に lccc... であるが、-d (--dcolumn) を指定する場合 lD{.}{.}{-1}D{.}{.}{-1}... となる。また、--align で具体的な規則を指定することができる。

任意の下線を引く、もしくは、セルを横に結合という処理の命令は csv ファイルに記述する。たとえば下線については、下線を引きたい行のいずれかのセルに `_hline_` もしくは `_midrule_` を挿入する (e.g., `AGE_hline_,12,23,11,34`)。ある特定のセルのみに下線を引く場合は、そのセルに `_cline_` もしくは `_cmidrule_` を挿入する。

セルを横に結合する場合は、結合セルの 2 列目以降のセルを `_union_` とする (e.g., `HEIGHT_cline_,_union_,_union_` とすれば、この 3 列がひとつのセルに結合され、HEIGHT という文字列が中央揃えで表示され、局所的な下線が引かれる)。

- -s SEP, --sep SEP
    - 区切り文字を指定。デフォルトは '\t' (タブ区切りテキスト)。csv などコンマ区切り文字列を指定したい場合は、-s, と指定する。
- -n MIDNUM, --nhead MIDNUM
    - ヘッダーの行数を指定。デフォルトは 1。0 以下を指定すると、ヘッダー無しと解釈する。 
- -d, --dcolumn
    - 小数点揃えにする場合に使用 (要 dcolumn.sty)。
- --align ALIGN
    - 列の揃え方についての指定。

## EXAMPLE

### UNIX

```
$ < foo.csv mktabular > bar.tex
```

# version

- v0.0.1 (2017-02-08)
    - 第 1 号
- v0.0.2 (2017-02-09)
    - cmidrule について、union が適用されない場合でも n-n の形にするよう修正
    - デフォルトの配列基準を lccc から lrrr に変更
    - 各要素をストリップする
    - midnum というキーワードをすべて nhead に置換
    - align の修正
    - multi が指定された場合、lcccc にする
        - complexconv を変更
- v0.0.3 (2017-02-09)
    - --sep を -s と省略できることにする
    - sep について、\\t が指定された場合タブに変換する
    - sep について、デフォルトを '\t' とする


