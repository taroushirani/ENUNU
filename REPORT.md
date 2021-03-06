# ENUNUの開発にあたって

## 要約

NNSVSを活用したUTAUプラグインを作った。UTAUをNNSVS用エディタとして使える。配布zip内のUTAU音源とUTAUプラグインをUTAUにインストールすることで使えるようになる。はず。

## 緒言

### 動機

最近、FLOSS である **[NNSVS](https://github.com/r9y9/nnsvs)** が話題となっている。NNSVS は山本りゅういち氏を中心に開発されており、ニューラルネットワークに基づく音声合成用 Python ライブラリである。機械学習を用いた音声合成ソフトウェアとして CeVIO、Sinsy、NEUTRINO などが挙げられるが、これらはソフトウェアの全部または一部がオープンソースではない。そのうち、NEUTRINO はフリーソフトであるが歌声モデルの生成手法が公開されていない。したがって、独自の歌声モデルを作成および配布したいという需要に応えることのできる機械学習系音声合成ソフトウェアとして、NNSVS は注目を浴びている。

NNSVS の利用に関して、既存の音声合成ソフトウェアである **[UTAU](http://utau2008.web.fc2.com/index.html#about)** のユーザーが独自のモデル生成に意欲的である。UTAU は波形合成型音声合成ソフトウェアであり、ユーザーによる音声ライブラリ作成が盛んに行われてきた歴史があり、その音声ライブラリは、2013年時点で5千種類以上が確認されており、2020年現在では1万種類以上と推測されている。しかしながら、情報技術開発者ではない UTAU ユーザーが NNSVS で遊ぶにあたり、NNSVS の実行環境構築とファイル変換のハードルは依然として高い。その原因として、フルコンテキストラベルを扱う **Sinsy** および **hts_engine API** をネイティブ Windows 上に構築するのが困難なことが挙げられる。

これを改善するのが本ソフトウェアの目的である。本ソフトウェアでは、次の5つの条件を満たす NNSVS の利用を目標とした。

- Windows で実行可能であること
- WSL や MSYS などの仮想環境および仮想ターミナルを必要としないこと
- UTAU エディタからプラグインとして起動できること
- UST ファイルからの手動ファイル変換を必要としないこと
- EXEファイルにすることで各種ライブラリのバージョンを固定すること

## 設計

### 開発環境

- Windows 10
- Python 3.8
  - utaupy 1.10.0
  - numpy 1.19.3（1.19.4 はWindowsのバグで動かない）
  - nnsvs 開発バージョン

### 全体の処理の流れ

1. USTをフルコンテキストラベルに変換する。
2. フルコンテキストラベルをNNSVSに渡す。

### 開発手順

1. hts_engine API および Sinsy に依存せずにHTSフルコンテキストラベルを入出力できるPythonモジュールを作成した。拙作のPythonライブラリである [utaupy](https://github.com/oatsu-gh/utaupy) に同梱し、utaupy.hts として公開している。
2. USTファイルをHTSフルコンテキストラベルに変換するPythonツールを作成した。本リポジトリ内に存在する。
3. NNSVSをWindows上で実行するためのPythonツールを作成した。（**ここはまだ計画**）
4. UTAUプラグインとして起動するためのPythonツールを作成した。（**ここもまだ計画**）

## 結果

### 従来のNNSVS利用方法

#### 実行環境

- Google Colaboratory
  - クラウド環境なため毎回環境構築が必要
- pnew
  - 環境構築のハードルが低い
  - msysを利用
  - スタンドアロンだがフルコンテキストラベルが必要
- WSL
  - 環境構築のハードルが高い
- Linux
  - ハードルが高い

#### 音声ファイル合成手順

1. **UTAU** でUSTからMIDIを作成
2. **MuseScore** でMIDIファイルからMusicXMLファイルを作成
3. **CeVIO** または **Sinsy** でMusicXMLファイルをHTSフルコンテキストラベルに変換
4. **NNSVS** にHTSフルコンテキストラベルを渡して音声ファイルを合成

### 本ソフトウェアを用いたNNSVS利用方法

#### 実行環境

- UTAUプラグイン
  - UTAUエディタから呼び出し
  - ネイティブWindows
  - Embeddable Python を同梱

### 音声ファイル合成手順

1. UTAUの音声ライブラリを本ソフトウェア同梱のものに設定する
2. UTAUエディタ上でノートを範囲選択
3. プラグインを起動して音声ファイルを合成

## 結論

~~いかがでしたか？~~