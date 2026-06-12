#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Python 虚拟环境创建和启动脚本${NC}"
echo -e "${GREEN}========================================${NC}"

# 定义虚拟环境目录名
VENV_DIR="venv"

# 检查是否已经存在虚拟环境
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}警告: 虚拟环境 '$VENV_DIR' 已存在${NC}"
    read -p "是否删除并重新创建? (y/n): " choice
    if [[ $choice == "y" || $choice == "Y" ]]; then
        echo -e "${YELLOW}正在删除旧的虚拟环境...${NC}"
        rm -rf "$VENV_DIR"
    else
        echo -e "${GREEN}使用现有的虚拟环境...${NC}"
    fi
fi

# 创建虚拟环境（如果不存在）
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${GREEN}正在创建虚拟环境...${NC}"
    python3 -m venv "$VENV_DIR"
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}错误: 创建虚拟环境失败${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ 虚拟环境创建成功${NC}"
fi

# 激活虚拟环境
echo -e "${GREEN}正在激活虚拟环境...${NC}"
source "$VENV_DIR/bin/activate"

if [ $? -ne 0 ]; then
    echo -e "${RED}错误: 激活虚拟环境失败${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 虚拟环境已激活${NC}"
echo ""

# 升级 pip
echo -e "${GREEN}正在升级 pip...${NC}"
pip install --upgrade pip

# 安装项目依赖
echo -e "${GREEN}正在安装项目依赖...${NC}"
pip install -e .

if [ $? -ne 0 ]; then
    echo -e "${RED}错误: 安装依赖失败${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 依赖安装完成${NC}"
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  虚拟环境已就绪!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "当前 Python 版本: $(python --version)"
echo -e "虚拟环境路径: $(pwd)/$VENV_DIR"
echo ""
echo -e "${YELLOW}提示:${NC}"
echo -e "  - 要退出虚拟环境，请输入: ${GREEN}deactivate${NC}"
echo -e "  - 要重新激活虚拟环境，请输入: ${GREEN}source $VENV_DIR/bin/activate${NC}"
echo ""

# 保持虚拟环境激活状态
exec bash
