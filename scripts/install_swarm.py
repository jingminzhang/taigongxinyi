#!/usr/bin/env python3
"""
安装OpenAI Swarm的脚本
"""

import subprocess
import sys

def install_swarm():
    """安装OpenAI Swarm"""
    print("🚀 正在安装OpenAI Swarm...")
    
    try:
        # 安装Swarm
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "git+https://github.com/openai/swarm.git"
        ], check=True, capture_output=True, text=True)
        
        print("✅ OpenAI Swarm安装成功！")
        print(result.stdout)
        
        # 验证安装
        try:
            import swarm
            print("✅ Swarm导入测试成功")
            print(f"📦 Swarm版本: {getattr(swarm, '__version__', '未知')}")
        except ImportError as e:
            print(f"❌ Swarm导入失败: {e}")
            return False
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def main():
    """主函数"""
    print("🏛️ 稷下学宫Swarm环境安装")
    print("=" * 40)
    
    # 检查是否已安装
    try:
        import swarm
        print("✅ OpenAI Swarm已安装")
        print(f"📦 版本: {getattr(swarm, '__version__', '未知')}")
        
        choice = input("是否重新安装？(y/N): ").strip().lower()
        if choice not in ['y', 'yes']:
            print("🎉 安装检查完成")
            return
    except ImportError:
        print("📦 OpenAI Swarm未安装，开始安装...")
    
    # 安装Swarm
    success = install_swarm()
    
    if success:
        print("\n🎉 安装完成！现在可以使用Swarm八仙论道了")
        print("💡 使用方法:")
        print("   python src/jixia/debates/swarm_debate.py")
        print("   或在Streamlit应用中选择'Swarm模式'")
    else:
        print("\n❌ 安装失败，请手动安装:")
        print("   pip install git+https://github.com/openai/swarm.git")

if __name__ == "__main__":
    main()