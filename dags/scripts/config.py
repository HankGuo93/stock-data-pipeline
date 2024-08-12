import configparser
import os

def load_config(config_file=None):
    if config_file is None:
            # 使用相對於腳本文件的路徑
        config_file = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'settings.cfg')
    
    # 確保路徑是絕對路徑
    config_file = os.path.abspath(config_file)
    
    #C:\Users\Hank\Documents\GitHub\stock-data-pipeline\config\settings _local.cfg
    # 檢查文件是否存在
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"配置文件不存在：{config_file}")
    
    with open(config_file, 'r', encoding='utf-8') as f:
           content = f.read()
           print(f"文件原始內容：\n{content}")

    # 檢查不可見字符
    print("檢查不可見字符：")
    for i, char in enumerate(content):
        if ord(char) < 32 and char != '\n':
            print(f"位置 {i}: ASCII {ord(char)}")

    # 手動解析文件
    manual_config = {}
    current_section = None
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            current_section = line[1:-1]
            manual_config[current_section] = {}
        elif '=' in line and current_section is not None:
            key, value = line.split('=', 1)
            manual_config[current_section][key.strip()] = value.strip()

    print(f"手動解析結果：{manual_config}")

    # 嘗試使用 RawConfigParser
    config = configparser.RawConfigParser()
    config.read_string(content)
    
    print(f"RawConfigParser 解析結果 - 所有部分：{config.sections()}")
    print(f"RawConfigParser 解析結果 - DEFAULT 部分：{dict(config['DEFAULT']) if 'DEFAULT' in config else 'Not found'}")

    return manual_config.get('DEFAULT', {})
