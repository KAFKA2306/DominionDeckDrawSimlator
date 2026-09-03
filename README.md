https://kafka2306.github.io/DominionDeckDrawSimlator/

# ドミニオン デッキ引き切り確率計算機

[![Exact probability tests](https://github.com/KAFKA2306/DominionDeckDrawSimlator/actions/workflows/test.yml/badge.svg)](https://github.com/KAFKA2306/DominionDeckDrawSimlator/actions/workflows/test.yml)

## 対象モデル

これはドミニオン全体のシミュレーターではありません。次の単純化モデルについて、乱数推定ではなく状態遷移の動的計画法で厳密確率を計算します。

- 初期手札は5枚
- 山札の順序は一様ランダム
- `+dドロー`カードを処理すると、利用可能カードを1枚消費し、d枚を追加
- アクション回数制限は無視し、引いたドローカードをすべて使用可能
- 捨て札、再シャッフル、獲得、持続、村、手札交換などは対象外

したがって、表示値を実ゲーム全体の「引き切り確率」と解釈してはいけません。

## 再現性

`probability.js` の `exactDrawProbability` は同じ入力に常に同じ値を返します。教育・検算用のMonte Carlo実装も残していますが、seed、試行回数、標準誤差、95%信頼区間を返し、公開UIの正準値には使いません。

```bash
npm test
```

テストは小規模デッキの全ユニーク順列列挙との一致、不正入力拒否、seed固定Monte Carloの統計的整合を検査します。

## 入力制限

単一計算は0〜200枚、表はデッキ10〜80枚・研究所0〜40枚・最大1,000セルです。負数、非整数、ドローカード総数がデッキ枚数を超える入力は拒否します。
