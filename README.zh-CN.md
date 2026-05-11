# Zotero Attachment Lookup Skill

可移植的 Zotero PDF local-first lookup skill，支持 quick-reference hint 和 deterministic storage scanning。

## 适合谁

| 适合使用 | 不适合使用 |
| --- | --- |
| 需要在本地 Zotero storage 中定位一篇 paper PDF | 需要重组整个 Zotero library |
| 有 DOI、title、item key、attachment key、filename 或 author hint | 需要 debug Zotero MCP startup |
| 希望先查本地文件，再用 metadata tooling | 已经知道 PDF path，只想解释论文 |

## 为什么需要它

- 本地文件是实际 PDF access 的最高置信来源。
- lookup 与 library organization、paper reading 分开。
- 结构化 match output 让 confidence 和 source tier 可见。

## 包含内容

| Component | 作用 |
| --- | --- |
| [`zotero-attachment-lookup`](./zotero-attachment-lookup) | 可安装的 Codex App skill package |
| [`zotero-attachment-lookup/references`](./zotero-attachment-lookup/references) | 随包发布的公开 reference material |
| [`zotero-attachment-lookup/scripts`](./zotero-attachment-lookup/scripts) | 随包发布的 helper scripts |
| [`zotero-attachment-lookup/test-prompts.json`](./zotero-attachment-lookup/test-prompts.json) | trigger / non-trigger 示例 |
| [`CHANGELOG.md`](./CHANGELOG.md) | release history |
| [`LICENSE`](./LICENSE) | license |

## 安装 / 使用

### Codex App

- 从本 repo 的这个路径安装 skill：`zotero-attachment-lookup`
- GitHub install target:
  - repo: `Mingdao007/zotero-attachment-lookup-skill`
  - path: `zotero-attachment-lookup`
- 安装后重启 `Codex App`，让新 skill 被重新发现。

## 工作流

```mermaid
flowchart LR
    A["Paper hint"] --> B["本地 Zotero 扫描"]
    B --> C["候选评分"]
    C --> D["最佳 PDF path"]
    D --> E["结构化结果"]
```

## 覆盖范围

- 支持 attachment-key、item-key、DOI、title、filename 和 author lookup input
- local-storage-first search，并可用 quick-reference hint
- 结构化 JSON 输出 match type、confidence 和 source tier

## 预期结果 / 验证

| 检查项 | 预期结果 |
| --- | --- |
| 安装路径 | `zotero-attachment-lookup` |
| GitHub target | `Mingdao007/zotero-attachment-lookup-skill`，path 为 `zotero-attachment-lookup` |
| Skill 入口 | 存在 `zotero-attachment-lookup/SKILL.md` |
| 触发样例 | `zotero-attachment-lookup/test-prompts.json` |
| 隐私检查 | 公开包不包含私人本机路径或 live user state |

## 触发示例

- `Find the local PDF for this Zotero item.`
- `Resolve this DOI to the best local Zotero attachment.`
- `Locate the attachment path before using metadata tooling.`

## 不应触发

- `Reorganize the whole Zotero library.`
- `Debug a Zotero transport startup failure.`
- `Explain the paper after the PDF is already known.`

## 隐私边界

这个公开仓库只保留通用、可复用的 workflow。

- local paths 改写为 host-relative defaults 或 environment overrides。
- 公开包保留 lookup logic，但移除 private companion-path assumptions。

## 仓库结构

| 路径 | 作用 |
| --- | --- |
| [`zotero-attachment-lookup`](./zotero-attachment-lookup) | 可安装的 Codex App skill package |
| [`zotero-attachment-lookup/references`](./zotero-attachment-lookup/references) | 随包发布的公开 reference material |
| [`zotero-attachment-lookup/scripts`](./zotero-attachment-lookup/scripts) | 随包发布的 helper scripts |
| [`zotero-attachment-lookup/test-prompts.json`](./zotero-attachment-lookup/test-prompts.json) | trigger / non-trigger 示例 |
| [`CHANGELOG.md`](./CHANGELOG.md) | release history |
| [`LICENSE`](./LICENSE) | license |

English:

- [README.md](./README.md)
