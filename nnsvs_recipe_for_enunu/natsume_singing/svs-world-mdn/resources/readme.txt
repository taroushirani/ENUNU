【夏目悠李 (ENUNU) (RMDN) v0.0.1 】

夏目悠李/ 男声歌声データベース (2020 年 9 月 2 日版) を NNSVS で学習させて,
UTAU プラグイン「 ENUNU 」から呼び出せるようにした歌声モデルです.

UTAU エディタ上での採譜および歌詞チェック用に,
「波音リツ音声ライブラリ単独音 Ver1.5.1Lite for UTAU 」を同梱しています.


【ソフトウェアの対応バージョン】

Windows 10 / UTAU 0.4.18 / ENUNU 0.1.0


----------------------------

【使い方】

1. 単独音歌詞で UST を作成
2. UST を保存
3. 音源に「夏目悠李 (ENUNU) v0.0.1 」を選択
4. ノートを範囲選択し, プラグイン「 ENUNU 」を起動
5. 待機
6. UST の保存場所の隣に WAV ファイルが生成される


【利用規約】

夏目悠李/ 男性歌声データベースの利用規約に従ってください. (https://amanokei.hatenablog.com/entry/2020/04/30/225933)

再配布可としますが, 前項の規約に相当する内容を必ず含んでください.

夏目悠李 (ENUNU) の不具合修正は, その時点での最新バージョンのみ対応します.

不具合報告はこちらの「 New issue 」にお願いします. (https://github.com/taroushirani/ENUNU/issues)

アイコン画像はデザイナーの UNF/UserNotFound 氏の公式イラストから作成しています. キャラクター「夏目悠李」を使用する際のガイドライン (https://amanokei.hatenablog.com/entry/2020/10/10/134126) に従ってください.


【歌声モデル仕様】

- 夏目悠李/ 男性歌声データベース (2020 年 9 月 2 日版) から学習
- 使用レシピ: svs-world-mdn
  - timelag model: FeedForwardNet num_layers 2, hidden_dim 128
  - duration model: RMDN, num_gaussians 4, num_layers 2, hidden_dim 256
  - acoustic model: RMDN with mlpg(dim-wise), num_gaussians ,4 num_layers 2, hidden_dim 256
- 音声ファイル出力:24bit 整数 / 48kHz
- ブレスのノイズを軽減するため, pau/sil を無音化

----------------------------

【連絡先】

Tarou Shirani

Twitter: https://twitter.com/taroushirani
E-mail : taroushirani@gmail.com
