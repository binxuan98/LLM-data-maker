import tkinter as tk
from MENU.menu import GUIWithMenu
import sys
import platform
import time
# youhua1
def optimize_gui_performance():
    # 根据不同操作系统进行优化
    if platform.system() == 'Windows':
        try:
            from ctypes import windll
            # 启用 Windows DPI 感知
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

def main():
    # 在创建窗口前进行优化设置
    optimize_gui_performance()
    
    root = tk.Tk()
    
    # 优化窗口性能
    root.update_idletasks()  # 预先处理待处理的界面更新
    root.withdraw()  # 临时隐藏窗口，避免闪烁
    
    # 设置应用程序优先级
    try:
        root.attributes('-priority', 'normal')  # 设置正常优先级
    except:
        pass
    
    app = GUIWithMenu(root)
    
    # 显示优化后的窗口
    root.deiconify()
    root.mainloop()

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"启动用时: {time.time() - start_time:.2f} 秒")
