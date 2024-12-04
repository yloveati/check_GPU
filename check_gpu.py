import subprocess
import platform
import sys
import ssl
import traceback
import ctypes
import wmi

class GPUChecker:
    def __init__(self):
        # 初始化 WMI
        try:
            self.wmi_obj = wmi.WMI()
        except Exception as e:
            print(f"初始化WMI失败: {str(e)}")
            self.wmi_obj = None

    def get_gpu_info(self):
        """获取显卡基本信息"""
        try:
            if platform.system() == "Windows":
                if self.wmi_obj:
                    gpu_info = self.wmi_obj.Win32_VideoController()
                    
                    print("\n=== 显卡基本信息 ===")
                    for gpu in gpu_info:
                        print(f"显卡名称: {gpu.Name}")
                        if gpu.AdapterRAM:
                            ram_gb = gpu.AdapterRAM / (1024**3)
                            print(f"显存大小: {ram_gb:.2f} GB")
                        print(f"驱动版本: {gpu.DriverVersion}")
                        print()
                else:
                    print("无法获取显卡信息：WMI初始化失败")
            else:
                print(f"当前系统 ({platform.system()}) 暂不支持")
                
        except Exception as e:
            print(f"获取显卡信息时出错: {str(e)}")
            traceback.print_exc()

    def get_detailed_info(self):
        """获取详细的显卡信息"""
        if platform.system() != "Windows":
            print("详细信息查询仅支持Windows系统")
            return

        try:
            if self.wmi_obj:
                gpu_info = self.wmi_obj.Win32_VideoController()[0]
                
                print("\n=== 详细显卡信息 ===")
                details = {
                    "显卡名称": gpu_info.Name,
                    "显存大小": f"{gpu_info.AdapterRAM / (1024**3):.2f} GB" if gpu_info.AdapterRAM else "未知",
                    "驱动版本": gpu_info.DriverVersion,
                    "显示模式": gpu_info.VideoModeDescription,
                    "刷新率": f"{gpu_info.CurrentRefreshRate} Hz" if gpu_info.CurrentRefreshRate else "未知",
                    "显卡状态": gpu_info.Status,
                    "显卡制造商": gpu_info.VideoProcessor,
                    "显示器接口": gpu_info.VideoMemoryType,
                    "驱动日期": gpu_info.DriverDate,
                    "最大刷新率": f"{gpu_info.MaxRefreshRate} Hz" if gpu_info.MaxRefreshRate else "未知",
                    "最小刷新率": f"{gpu_info.MinRefreshRate} Hz" if gpu_info.MinRefreshRate else "未知",
                    "显卡芯片": gpu_info.VideoArchitecture
                }
                
                for key, value in details.items():
                    if value:
                        print(f"{key}: {value}")

        except Exception as e:
            print(f"获取详细信息时出错: {str(e)}")
            traceback.print_exc()

    def check_nvidia_gpu(self):
        """检查是否有NVIDIA显卡并获取信息"""
        try:
            # 尝试运行nvidia-smi命令
            output = subprocess.check_output(
                ["nvidia-smi"], 
                shell=True, 
                stderr=subprocess.PIPE
            ).decode('utf-8')
            
            print("\n=== NVIDIA GPU信息 ===")
            print(output)
            
        except subprocess.CalledProcessError:
            print("\nNVIDIA显卡未找到或驱动未安装")
        except Exception as e:
            print(f"检查NVIDIA显卡时出错: {str(e)}")

    def get_system_info(self):
        """获取系统信息"""
        print("\n=== 系统信息 ===")
        print(f"操作系统: {platform.system()} {platform.release()}")
        print(f"系统版本: {platform.version()}")
        print(f"机器类型: {platform.machine()}")
        print(f"处理器: {platform.processor()}")
        print(f"Python版本: {sys.version.split()[0]}")

def main():
    try:
        checker = GPUChecker()
        
        # 获取系统信息
        checker.get_system_info()
        
        # 获取基本显卡信息
        checker.get_gpu_info()
        
        # 获取详细信息
        checker.get_detailed_info()
        
        # 检查NVIDIA显卡
        checker.check_nvidia_gpu()
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 