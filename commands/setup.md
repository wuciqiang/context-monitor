---
description: 配置 statusLine 显示上下文使用率
---

# 配置 statusLine

自动配置 Claude Code 状态栏显示上下文使用率。

## 执行步骤

1. **检测插件路径**
   - 查找已安装的 cm 插件路径
   - 定位 statusline.py 脚本

2. **读取现有配置**
   - 读取 `.claude/settings.json`
   - 如果不存在则创建

3. **添加 statusLine 配置**
   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "python <插件路径>/statusline.py",
       "padding": 0
     }
   }
   ```

4. **保存配置**
   - 写入 `.claude/settings.json`
   - 提示用户重启 Claude Code

5. **验证配置**
   - 测试 statusline 脚本是否正常运行
   - 显示预期输出示例

**输出**: 配置完成提示 + 重启说明
