#!/usr/bin/env bash
# ============================================================
# md2pdf 一键安装脚本 (macOS / Linux)
# ============================================================
set -e

echo "========================================"
echo "  md2pdf — Markdown → PDF 转换工具"
echo "  一键安装脚本"
echo "========================================"
echo ""

# 检测 Python
PYTHON=""
for cmd in python3 python; do
    if command -v $cmd &>/dev/null; then
        VER=$($cmd --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
        MAJOR=${VER%%.*}
        if [ "$MAJOR" -ge 3 ]; then
            PYTHON=$cmd
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "❌ 未找到 Python 3。请先安装: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ 检测到: $($PYTHON --version)"

# 安装依赖
echo ""
echo "📦 安装 Python 依赖..."
$PYTHON -m pip install --upgrade pip -q
$PYTHON -m pip install markdown-it-py mdit-py-plugins pygments -q
echo "✅ 依赖安装完成"

# 安装 WeasyPrint
echo ""
echo "🔧 安装 PDF 渲染引擎 (WeasyPrint)..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "   macOS: 尝试安装 weasyprint..."
    $PYTHON -m pip install weasyprint -q 2>/dev/null && echo "✅ weasyprint 已安装" || echo "⚠️  pip 安装失败，可能需要系统库: brew install glib pango gdk-pixbuf"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "   Linux: 安装系统依赖..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get update -qq && sudo apt-get install -y -qq libglib2.0-0 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev 2>/dev/null
    fi
    $PYTHON -m pip install weasyprint -q
fi

# 安装 md2pdf
echo ""
echo "📦 安装 md2pdf..."
$PYTHON -m pip install . -q 2>/dev/null || {
    # fallback: 直接复制脚本
    SCRIPT_SRC="md2pdf/__init__.py"
    if [ -f "$SCRIPT_SRC" ]; then
        echo "   尝试直接安装..."
        $PYTHON -m pip install -e . -q
    fi
}

# 验证
echo ""
echo "🔍 验证安装..."
if command -v md2pdf &>/dev/null; then
    echo "✅ md2pdf 安装成功!"
    md2pdf --version
else
    # 尝试用 pip show 找到位置
    LOC=$($PYTHON -m pip show md2pdf-tool 2>/dev/null | grep Location | awk '{print $2}')
    if [ -n "$LOC" ]; then
        echo "  添加到 PATH: export PATH=\"\$PATH:$LOC/bin\""
    fi
    echo ""
    echo "⚠️  请确保 ~/.local/bin 在 PATH 中"
fi

echo ""
echo "========================================"
echo "  🎉 安装完成!"
echo "  使用: md2pdf input.md -o output.pdf"
echo "========================================"
