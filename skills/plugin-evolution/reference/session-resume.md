# セッション再開時の記憶連続性

詳細は `/doc/10_session_resume_continuity.md` を参照してください。

## 概要

現在のセッションメモ設計は「セッション内で揮発」を前提としているが、作業中断・再開のユースケースが存在する。

## 推奨案

Option B: 作業記憶の追加（v0.2.0で検討）

### 4種類の記憶

1. **ワークフロー** (`commands/`) - ワークフロー
2. **セッションメモ** (`.claude/short-term-memory.local.md`) - セッション内メモ
3. **作業記憶** (`.claude/work-in-progress.local.md`) - 作業中断・再開用（新規）
4. **ナレッジベース** (`skills/`, `agents/`) - パターンから生成

### 実装内容

```bash
# 作業記憶コマンド
/as-you:wip-set "Phase 5実装中: Scripts完了、次はHooks"
/as-you:wip-show
/as-you:wip-clear
/as-you:wip-done  # 完了時にアーカイブして削除
```

## 優先度

- v0.1.0: 実装しない（基本機能に集中）
- v0.2.0: 実装検討（実運用フィードバック後）
