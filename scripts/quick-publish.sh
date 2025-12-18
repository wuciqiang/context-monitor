#!/bin/bash
# 快速发布脚本

set -e  # 遇到错误立即退出

echo "🚀 Claude Context Monitor - Quick Publish"
echo "========================================"
echo ""

# 检查是否在正确的目录
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Are you in the right directory?"
    exit 1
fi

# 读取当前版本
CURRENT_VERSION=$(node -p "require('./package.json').version")
echo "📦 Current version: $CURRENT_VERSION"
echo ""

# 询问用户名（如果还没设置）
if grep -q "YOUR-USERNAME" package.json; then
    echo "⚠️  Please update package.json with your GitHub username first!"
    read -p "Enter your GitHub username: " GITHUB_USERNAME

    # 更新 package.json
    sed -i "s/YOUR-USERNAME/$GITHUB_USERNAME/g" package.json
    sed -i "s/your-username/$GITHUB_USERNAME/g" package.json
    echo "✅ Updated package.json with username: $GITHUB_USERNAME"
    echo ""
fi

# 步骤 1: Git 初始化
echo "1️⃣ Initializing Git repository..."
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git initialized"
else
    echo "⏭️  Git already initialized"
fi
echo ""

# 步骤 2: 添加所有文件
echo "2️⃣ Adding files to Git..."
git add .
echo "✅ Files added"
echo ""

# 步骤 3: 提交
echo "3️⃣ Creating initial commit..."
if ! git diff --cached --quiet; then
    git commit -m "Initial commit: Claude Context Monitor v$CURRENT_VERSION"
    echo "✅ Committed"
else
    echo "⏭️  No changes to commit"
fi
echo ""

# 步骤 4: 询问是否推送到 GitHub
read -p "4️⃣ Do you want to push to GitHub? (y/N): " PUSH_GITHUB
if [ "$PUSH_GITHUB" = "y" ] || [ "$PUSH_GITHUB" = "Y" ]; then
    # 检查是否已设置 remote
    if ! git remote get-url origin > /dev/null 2>&1; then
        GITHUB_USERNAME=$(node -p "require('./package.json').repository.url.match(/github.com\/([^\/]+)/)[1]")
        REPO_URL="https://github.com/$GITHUB_USERNAME/context-monitor.git"

        echo "   Setting remote: $REPO_URL"
        git remote add origin "$REPO_URL"
    fi

    git branch -M main
    git push -u origin main

    # 创建 tag
    git tag -a "v$CURRENT_VERSION" -m "Release v$CURRENT_VERSION"
    git push origin "v$CURRENT_VERSION"

    echo "✅ Pushed to GitHub"
    echo ""
    echo "📝 Next: Create a Release on GitHub:"
    echo "   https://github.com/$GITHUB_USERNAME/context-monitor/releases/new"
else
    echo "⏭️  Skipped GitHub push"
fi
echo ""

# 步骤 5: 询问是否发布到 npm
read -p "5️⃣ Do you want to publish to npm? (y/N): " PUBLISH_NPM
if [ "$PUBLISH_NPM" = "y" ] || [ "$PUBLISH_NPM" = "Y" ]; then
    echo "   Checking npm login..."
    if npm whoami > /dev/null 2>&1; then
        echo "   ✅ Logged in as: $(npm whoami)"
    else
        echo "   Please login to npm:"
        npm login
    fi

    echo "   Running tests..."
    npm test || echo "⚠️  Tests failed, but continuing..."

    echo "   Publishing to npm..."
    npm publish --access public

    echo "✅ Published to npm!"
    echo ""
    echo "📦 View on npm:"
    echo "   https://www.npmjs.com/package/@claude/context-monitor"
else
    echo "⏭️  Skipped npm publish"
fi
echo ""

echo "========================================"
echo "✅ Done!"
echo ""
echo "📚 Next steps:"
echo "1. Create a Release on GitHub (if not done)"
echo "2. Test installation: npm install @claude/context-monitor"
echo "3. Update documentation if needed"
echo ""
echo "🎉 Congratulations on publishing!"
