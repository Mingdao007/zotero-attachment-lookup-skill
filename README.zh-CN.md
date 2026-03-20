# Zotero Attachment Lookup Skill

面向 Zotero 附件定位的可移植 local-first skill，支持可选 quick-reference 与确定性 storage 扫描。

## 提供内容

- 可安装 skill: [`zotero-attachment-lookup`](./zotero-attachment-lookup)
- 公开 references: [`zotero-attachment-lookup/references/`](./zotero-attachment-lookup/references)
- 辅助脚本: [`zotero-attachment-lookup/scripts/`](./zotero-attachment-lookup/scripts)

## 安装 / 使用

- `Codex App`：从本仓库路径 `zotero-attachment-lookup` 安装
- GitHub 安装目标：
  - repo：`<owner>/zotero-attachment-lookup-skill`
  - path：`zotero-attachment-lookup`
- 安装后重启 `Codex App`，让新 skill 被发现。

## 覆盖范围

- 支持 attachment key、item key、DOI、title、filename、author 等输入
- 以本地存储优先，必要时结合 quick-reference 提示
- 输出结构化 JSON，包含 match type、confidence 与 source tier

## 触发示例

- `Find the local PDF for this Zotero item.`
- `Resolve this DOI to the best local Zotero attachment.`
- `Locate the attachment path before using metadata tooling.`

## 不触发示例

- `Reorganize the whole Zotero library.`
- `Debug a Zotero transport startup failure.`
- `Explain the paper after the PDF is already known.`

## 隐私边界

这个公开仓库只保留可复用、可公开的工作流部分。

- Local paths are rewritten to use host-relative defaults or environment overrides.
- The public package keeps the lookup logic but removes private companion-path assumptions.

## 仓库结构

- `zotero-attachment-lookup/`: installable `Codex App` skill
- `zotero-attachment-lookup/references/`: bundled public references
- `zotero-attachment-lookup/scripts/`: bundled public scripts
- `CHANGELOG.md`: release history
- `LICENSE`: `MIT`

English:

- [README.md](./README.md)
