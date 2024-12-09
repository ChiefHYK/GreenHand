# Python Tetris Game

一个使用 Python 和 Pygame 开发的俄罗斯方块游戏。

## 功能特点

- 经典的俄罗斯方块玩法
- 支持键盘控制
- 粒子效果系统
- 连击计分系统
- 游戏统计功能
- 最高分保存
- 背景音效

## 安装要求

- Python 3.x
- Pygame 库

## 安装步骤

1. 克隆仓库：
   ```bash
   git clone [repository-url]
   ```

2. 安装依赖：
   ```bash
   pip install pygame
   ```

3. 运行游戏：
   ```bash
   python tetris.py
   ```

## 游戏控制

- ←/→: 左右移动
- ↑: 旋转方块
- ↓: 加速下落
- 空格: 直接落下
- ESC: 退出游戏

## 项目结构

/tetris
/assets
/fonts  
 • simhei.ttf # 游戏字体    
/sounds 
 • move.wav # 移动音效  
 • rotate.wav # 旋转音效  
 • drop.wav # 落下音效  
 • clear.wav # 消行音效    
 • gameover.wav # 游戏结束音效  
/ tetris.py # 主游戏代码  
/ README.md # 项目文档   
/ highscore.txt # 最高分记录

## 主要类说明

1. `Config`
   - 游戏配置和常量管理
   - 包括屏幕尺寸、方块大小、颜色等配置

2. `FontManager`
   - 字体资源管理
   - 处理游戏中的文字显示

3. `Tetromino`
   - 俄罗斯方块类
   - 实现方块的移动、旋转等功能

4. `Particle`
   - 粒子效果系统
   - 实现消行时的视觉效果

5. `ComboSystem`
   - 连击系统
   - 处理连续消行的加分机制

6. `GameStats`
   - 游戏统计
   - 记录游戏数据和最高分

7. `GameUI`
   - 用户界面管理
   - 处理游戏界面的显示

8. `GameLogic`
   - 游戏核心逻辑
   - 处理碰撞检测、消行等机制

9. `TetrisGame`
   - 主游戏类
   - 整合所有组件并运行游戏

## 开发说明

### 代码风格
- 遵循 PEP 8 规范
- 使用类型提示
- 包含详细的注释和文档字符串

### 维护指南
1. 配置修改
   - 所有游戏配置集中在 `Config` 类中
   - 修改配置时注意保持一致性

2. 添加新功能
   - 遵循现有的类结构
   - 确保新代码有适当的注释
   - 更新相关文档

3. 错误处理
   - 使用 try-except 处理可能的异常
   - 添加适当的错误日志

4. 测试
   - 测试新添加的功能
   - 确保不影响现有功能

## 版本历史

- 1.0.0 (2024-12-07)
  - 初始版本发布
  - 实现基本游戏功能
  - 添加音效和粒子系统
  - 实现统计和计分系统

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

开源许可

## 联系方式

ChiefHYK@163.com