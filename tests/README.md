# As You Plugin Tests

このディレクトリには、As Youプラグインのテストスイートが含まれています。

## テスト構成

```
tests/
├── unit/                # 単体テスト
│   ├── scripts.bats    # スクリプトのユニットテスト (scripts/*.sh)
│   └── hooks.bats      # フックのユニットテスト (hooks/*.sh)
├── integration/         # 統合テスト
│   └── workflow.bats   # エンドツーエンドワークフローテスト
├── validation/          # 検証テスト
│   ├── frontmatter.bats # YAML frontmatter検証 (commands/, agents/, skills/)
│   └── json-schema.bats # JSON構造検証 (plugin.json, hooks.json)
└── fixtures/            # テストフィクスチャ
    ├── sample-memo.md
    ├── sample-archive.md
    ├── sample-command.md
    └── invalid-frontmatter.md
```

## テストの実行

### 前提条件

- **mise**: タスクランナー（必須）
- **bats-core**: Bashテストフレームワーク
- **jq**: JSON処理ツール

```bash
# miseのインストール
curl https://mise.run | sh

# bats-coreのインストール
mise use -g bats@latest

# jqのインストール (Ubuntu/Debian)
sudo apt-get install jq

# または (macOS)
brew install jq
```

### miseタスクで実行

```bash
# プロジェクトルートから実行
mise run test              # すべてのテスト
mise run test:unit         # 単体テストのみ
mise run test:integration  # 統合テストのみ
mise run test:validation   # 検証テストのみ
mise run test:watch        # watchモード

# その他の開発タスク
mise tasks                 # タスク一覧
mise run lint              # shellcheck
mise run format            # shfmt
mise run validate          # プラグイン設定検証
```

### 個別のテストファイルを直接実行

```bash
bats tests/unit/scripts.bats
bats tests/integration/workflow.bats
```

## テストカバレッジ

### Unit Tests (単体テスト)

- **scripts.bats**: 8個のスクリプトの動作検証
  - `detect-patterns.sh`: パターン検出
  - `archive-memo.sh`: メモアーカイブ
  - `cleanup-archive.sh`: 古いアーカイブの削除
  - `track-frequency.sh`: パターン頻度追跡
  - `suggest-promotions.sh`: 昇格候補の提案
  - その他のスクリプト

- **hooks.bats**: 3個のフックの動作検証
  - `session-start.sh`: セッション開始処理
  - `session-end.sh`: セッション終了処理
  - `post-edit-format.sh`: 編集後処理

### Integration Tests (統合テスト)

- **workflow.bats**: エンドツーエンドワークフロー
  - セッションライフサイクル
  - パターン検出→昇格提案フロー
  - アーカイブクリーンアップ
  - 共起パターン検出
  - パターンの蓄積

### Validation Tests (検証テスト)

- **frontmatter.bats**: YAML frontmatter検証
  - Commands の frontmatter
  - Agents の frontmatter
  - Skills の frontmatter
  - 名前の一意性チェック

- **json-schema.bats**: JSON構造検証
  - `plugin.json` 構造
  - `hooks.json` 構造
  - パス参照の正当性

## CI/CD

GitHub Actionsで自動テストを実行：

- Push時 (main, develop)
- Pull Request時

テスト結果は各PRのChecks タブで確認できます。

## テストの追加

新しいテストを追加する場合：

1. 適切なカテゴリ (unit/integration/validation) に `.bats` ファイルを作成
2. 必要に応じて `fixtures/` にテストデータを追加
3. `test-runner.sh` は自動的に新しいテストを検出

### テストの書き方

```bash
#!/usr/bin/env bats

setup() {
    # テスト前の準備
    export TEST_DIR="$(mktemp -d)"
}

teardown() {
    # テスト後のクリーンアップ
    rm -rf "$TEST_DIR"
}

@test "description of test" {
    run your_command

    [ "$status" -eq 0 ]
    [[ "$output" =~ "expected output" ]]
}
```

詳細は既存のテストファイルを参照してください。
