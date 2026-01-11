# Default 统一管理与同步机制（计划）

## 背景
当前 `agents/templates/` 下存在多个 Agent 模板（如 `avery/`、`dexter/`、`nova/`），它们在**文件结构**与**工作规则**上高度相似，但已经出现漂移与不一致（例如目录命名差异、README/Onboarding 文案错位、`CLAUDE.md` 规则增量无法集中管理等）。同时 `default/` 目前过于精简，尚未承担“统一管理”的角色。

目标是在 `default/` 中集中维护：
- 标准文件结构（目录骨架 + 公共模板文件）
- `CLAUDE.md` 中通用的工作规则（Common rules）
- 可选的公共 skills（同名 skill 才同步更新）

并提供一个可幂等执行的同步 CLI（基于 Typer）对其它模板进行同步更新。

---

## 调研结论（当前仓库现状）
以当前目录为例（`agents/templates/`）：
- `default/` 仅包含一个非常简化的 `CLAUDE.md`。
- `avery/`、`dexter/`、`nova/` 都具备较完整的模板骨架：`areas/`、`memory/`、`resources/`、`.claude/skills/`、`archive/`、`artifacts/` 等。
- 结构与内容差异点（影响“统一管理”的关键）：
  - `daily/` vs `logs/daily/`：`avery/` 使用 `logs/daily/`，而 `dexter/`、`nova/` 使用 `daily/`。
  - 文案漂移：`dexter/README.md` 标题/路径出现 “Nova” 字样；`dexter/ONBOARDING_GUIDE.md` 仍写 “Reader: Avery”。
  - `CLAUDE.md`：`avery/` 与 `dexter/` 内容一致；`nova/` 在 “Core Principles” 处新增了 3 条额外约束。
  - skills：三者共有 `hook-development`、`skill-creator`；`dexter/` 额外拥有 `developer-growth-analysis`。
  - `nova/` 额外包含 `IDENTITY.md`（示例：应被保护，永远不自动覆盖）与 `resources/credentials/`（潜在敏感/可选结构）。
  - `.DS_Store` 等平台文件存在（应在同步中忽略）。

---

## 设计原则
- **Single Source of Truth**：`default/` 是公共内容的唯一权威来源。
- **幂等（Idempotent）**：多次执行 `sync` 的结果一致；无变化时不写入文件。
- **安全优先**：默认不做删除（prune），不覆盖“受保护文件”；对可能破坏性操作提供显式开关与备份策略。
- **可解释/可审计**：所有写入都能在 `--dry-run` 下预览；输出清晰列出 create/update/skip。
- **可扩展**：未来新增模板、规则或迁移路径时，只需修改配置文件与 default 内容。

---

## 同步模型（default → targets）
### 1) 角色定义
- **Source（源模板）**：`default/`
- **Targets（目标模板集合）**：仓库根目录下的模板目录（例如 `avery/`、`dexter/`、`nova/`），可通过配置显式列出或自动发现（排除 `default/` 与点目录）。

### 2) 路径策略（按文件/目录分类）
建议在配置中把路径分成三类（按 glob 匹配）：
1. **keep_updated（保持更新）**：由 `default/` 管理，目标模板应始终与 default 对齐（必要时支持托管区块替换等机制）。
2. **never_update（永不更新）**：无论 default 是否变化，都不对目标模板写入（例如 `IDENTITY.md`）。
3. **update_if_exists（存在才更新）**：用于 skills：目标模板存在同名 skill 才同步更新；不存在则跳过（保持各自独特技能集合）。

> 同步时只对 “配置声明的路径集合” 写入；默认不删除 target 中多出来的文件/目录（避免误删个性化资产）。

---

## `CLAUDE.md` 的通用部分管理（推荐方案）
需求是“统一管理 `CLAUDE.md` 中通用部分，同时允许每个模板保留独特补充规则”。

### 推荐：managed block markers（仅替换特定区块）
目标：同步工具只负责 `CLAUDE.md` 的“通用规则区块”；每个模板的个性化内容仍然由各自目录下的 `CLAUDE.md` 直接维护（不会被覆盖）。

#### 标记格式（示例）
在目标模板 `CLAUDE.md` 中，用成对标签包住“托管区块”，例如：
```md
<general_rules>[[managed content]]</general_rules>
```

建议实际落盘用多行，便于阅读与 diff（同步工具应同时支持单行/多行）：
```md
<general_rules>
[[managed content]]
</general_rules>
```

#### 替换逻辑（v1）
- 扫描目标文件中的 `<general_rules>` 与 `</general_rules>`，提取区块内部内容（exclusive）。
- 用 `default/` 中维护的 canonical 内容替换该区块的内部内容（保留 tag 本身）。
- 用 `sha256` 对比 “canonical 内容” 与 “目标区块内容”；一致则跳过，不一致则更新（幂等）。

#### canonical 内容存放（建议）
- `default/managed_blocks/claude/general_rules.md`（仅存放区块内容，不含外层 tag）。
- 后续扩展时：`default/managed_blocks/claude/<block_name>.md`。

#### 异常/冲突处理（v1）
- 缺失 required block：默认 skip + warning（`--strict` 下视为 error）。
- 同名 block 出现多次：视为结构异常，默认 error（避免不确定替换）。
- 只修改托管区块范围，尽量保持文件其它部分原样（减少噪音 diff）。

---

## skills 同步策略（“同名才更新”）
定义 `skills_root = .claude/skills`。

同步规则：
- `default/.claude/skills/<skill_name>/` 视为公共技能源。
- 对每个 target：
  - 若存在 `target/.claude/skills/<skill_name>/`：同步更新该 skill 下 default 已包含的文件（create/update），并 **不删除** target 额外文件（保留本地扩展）。
  - 若不存在：默认跳过（保持各自独特 skills 集合）；可选提供 `--install-missing-skills` 开关用于显式安装。

---

## 哈希比对与幂等更新
### 哈希算法
建议使用 `sha256`（Python 标准库 `hashlib`），对文件内容字节流计算 hash。

### 幂等定义（可测试）
对任意 target：
- 第一次 `sync` 后，所有 `keep_updated` 路径的“期望内容”与实际内容一致。
- 再次执行 `sync`，hash 全部一致，因此不再写入任何文件（输出 0 changes）。

### 忽略项
至少忽略：
- `.DS_Store`
- `.git/`（如果未来把 sync 工具放在同 repo，需要显式排除）
- 其它可在配置里扩展的 ignore patterns

---

## 配置文件（建议落在 default 内统一管理）
建议默认配置路径：`default/template-sync.yaml`（也允许 CLI 通过 `--config` 指定别处）。

### 配置内容建议（v1）
1. **targets**
   - `mode: explicit|discover`
   - `include/exclude`（discover 模式下的目录过滤）
2. **sync**
   - `keep_updated`: glob 列表（相对 target 根目录的路径）
   - `never_update`: glob 列表
3. **managed_blocks**
   - `files`: 哪些文件需要做托管区块替换（例如 `CLAUDE.md`）
   - `blocks`: block 名称 → canonical 内容来源（file path）
4. **skills**
   - `root: .claude/skills`
   - `mode: update_if_exists`
5. **migrations（可选）**
   - 用于处理目录结构统一（如 `logs/daily → daily`）的显式迁移规则，只在 `--migrate` 开关下执行

### 示例（示意，字段可调整）
```yaml
version: 1

source:
  dir: default

targets:
  mode: explicit
  list: [avery, dexter, nova]

sync:
  keep_updated:
    - .gitignore
    - areas/**
    - resources/templates/**
    - daily_logs/YYYY-MM-DD.md
    - README.md
  never_update:
    - IDENTITY.md
    - ONBOARDING_GUIDE.md

managed_blocks:
  files:
    - CLAUDE.md
  blocks:
    general_rules:
      source: default/managed_blocks/claude/general_rules.md

skills:
  root: .claude/skills
  mode: update_if_exists
```

---

## CLI 设计（Typer）
建议 CLI 目标：在本仓库内执行模板同步（不依赖网络运行；依赖安装除外）。

### 命令与行为
- `templates status`：只计算并展示差异（默认等价 `sync --dry-run`），不写文件。
- `templates sync`：执行同步更新。
  - `--dry-run`：不写入，只打印变更清单
  - `--target <name>`：只同步某一个模板（可多次传入或逗号分隔）
  - `--with-skills/--no-skills`
  - `--strict`：托管区块缺失/重复等结构问题直接报错（默认仅 warning/skip）
  - `--migrate`：执行显式迁移规则（例如日志目录改名）
  - `--check`：有差异时返回非 0（用于 CI）

输出建议（人类友好）：
- 每个 target 一段汇总：`created/updated/skipped/protected/conflicts`
- 变更清单包含：相对路径、操作类型、hash before/after（可选在 verbose 下展示）

---

## 实施里程碑（分阶段落地）
### Phase 0：整理 default 为“真正的基座模板”
- 从现有模板中抽取 90% 公共骨架补齐到 `default/`（目录与公共文件）。
- 在 `default/` 中补齐 `CLAUDE.md` 的通用规则托管区块 canonical 内容（例如 `default/managed_blocks/claude/general_rules.md`），并约定目标模板用 `<general_rules>...</general_rules>` 承载通用规则。
- 增加 `default/template-sync.yaml` 作为唯一配置入口。

### Phase 1：实现同步内核（无 CLI）
- 实现：glob 展开、忽略规则、sha256、copy/update、managed blocks 替换、skills update_if_exists。
- 提供纯 Python API：`plan_changes()` + `apply_changes()`，便于测试与 CLI 复用。

### Phase 2：实现 Typer CLI
- 按上文命令设计落地 `status/sync`，支持 `--dry-run/--check/--target`。
- 增加清晰错误提示：配置缺失/字段错误/目标目录不存在等。

### Phase 3：测试与回归
- 针对 sync 规则做最小测试集：
  - `CLAUDE.md` 托管区块替换（`<general_rules>...</general_rules>`）
  - `never_update` 跳过验证（`IDENTITY.md` 不被覆盖）
  - skills 同名更新、不同名保留验证
  - 幂等验证（连续两次 sync 无变更）

---

## 验收标准
- `templates sync` 能把 `keep_updated` 路径同步到一致，并在第二次运行时输出 0 changes（幂等）。
- `never_update` 路径（如 `IDENTITY.md`）始终不被覆盖。
- skills：同名 skill 会同步更新，不同名 skill 保留不动。
- `--dry-run` 与实际写入结果一致可预期。

---

## 待确认问题（建议在实现前确认）
1. `daily/` vs `logs/daily/`：最终希望统一到哪一种？是否需要自动迁移并删除旧路径？
2. `memory/memory.jsonl`、`daily/*.md` 这类“可能变成状态数据”的文件，在目标模板里是否也应该加入 `never_update`？
3. `CLAUDE.md` 的托管区块是否只需要 `general_rules`，还是还要拆更多 block（如 `tooling_rules`、`communication_rules`）？
