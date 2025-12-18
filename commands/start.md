---
description: 启动完整工作流（Phase 0-1）
---

# Context Monitor 工作流启动

执行 Phase 0-1：初始化与上下文检索

## Phase 0: 初始化与上下文检查

1. **检查上下文使用率**
   - 调用 `check_context_usage` 工具
   - 确认使用率 < 50%
   - 如果使用率过高，提示用户执行 `/clear`

2. **初始化代码索引**（首次使用）
   - 调用 `set_project_path` 设置项目路径
   - 调用 `build_deep_index` 构建索引
   - 调用 `configure_file_watcher(enabled=true)` 启用文件监控

## Phase 1: 上下文全量检索

3. **搜索相关代码**
   - 使用 `search_code_advanced` 进行自然语言搜索
   - 使用 `get_file_summary` 获取完整定义
   - 递归检索依赖文件

4. **总结上下文**
   - 汇总所有相关代码
   - 识别关键类、函数、变量
   - 准备进入下一阶段

**输出**：完整的代码上下文 + 上下文状态报告
