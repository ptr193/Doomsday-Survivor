# -*- coding: utf-8 -*-

import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

class SaveSystem:
    def __init__(self, game):
        self.game = game
        self.save_dir = "saves"
        self.backup_dir = "saves/backups"
        self.ensure_directories()

    def ensure_directories(self):
        """确保保存目录存在"""
        os.makedirs(self.save_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

    def save_game(self, save_slot: int, save_data: Dict[str, Any]) -> bool:
        """保存游戏"""
        try:
            save_file = self.get_save_file_path(save_slot)
            # 创建备份
            if os.path.exists(save_file):
                self.create_backup(save_slot)
            # 添加元数据
            save_data['metadata'] = {
                'version': self.game.version,
                'save_slot': save_slot,
                'save_time': datetime.now().isoformat(),
                'player_name': save_data.get('player', {}).get('name', '未知'),
                'day_count': save_data.get('day_count', 1)
            }
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            logging.info(f"游戏保存成功: 槽位 {save_slot}")
            return True
        except Exception as e:
            logging.error(f"保存游戏失败: {e}")
            return False

    def load_game(self, save_slot: int) -> Optional[Dict[str, Any]]:
        """加载游戏"""
        try:
            save_file = self.get_save_file_path(save_slot)
            if not os.path.exists(save_file):
                logging.error(f"存档文件不存在: {save_file}")
                return None
            with open(save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            if self.validate_save_data(save_data):
                logging.info(f"游戏加载成功: 槽位 {save_slot}")
                return save_data
            else:
                logging.error("存档数据验证失败")
                return self.restore_backup(save_slot)
        except Exception as e:
            logging.error(f"加载游戏失败: {e}")
            return self.restore_backup(save_slot)

    def validate_save_data(self, save_data: Dict[str, Any]) -> bool:
        """验证存档数据完整性"""
        try:
            required_sections = ['player', 'world', 'game_time']
            for section in required_sections:
                if section not in save_data:
                    logging.error(f"存档缺少必需数据段: {section}")
                    return False
            # 检查玩家数据
            player_data = save_data['player']
            required_player_fields = ['name', 'health', 'stamina', 'mental']
            for field in required_player_fields:
                if field not in player_data:
                    logging.error(f"玩家数据缺少字段: {field}")
                    return False
            # 验证游戏时间
            datetime.fromisoformat(save_data['game_time'])
            return True
        except Exception as e:
            logging.error(f"存档数据验证错误: {e}")
            return False

    def get_save_file_path(self, save_slot: int) -> str:
        """获取存档文件路径"""
        return os.path.join(self.save_dir, f"save_slot_{save_slot}.json")

    def get_backup_file_path(self, save_slot: int) -> str:
        """获取备份文件路径"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.backup_dir, f"save_slot_{save_slot}_backup_{timestamp}.json")

    def create_backup(self, save_slot: int) -> bool:
        """创建备份"""
        try:
            save_file = self.get_save_file_path(save_slot)
            backup_file = self.get_backup_file_path(save_slot)
            with open(save_file, 'r', encoding='utf-8') as source:
                with open(backup_file, 'w', encoding='utf-8') as target:
                    target.write(source.read())
            logging.info(f"备份创建成功: {backup_file}")
            return True
        except Exception as e:
            logging.error(f"创建备份失败: {e}")
            return False

    def restore_backup(self, save_slot: int) -> Optional[Dict[str, Any]]:
        """恢复备份"""
        try:
            backup_files = []
            for filename in os.listdir(self.backup_dir):
                if filename.startswith(f"save_slot_{save_slot}_backup"):
                    backup_files.append(filename)
            if not backup_files:
                logging.error("没有找到备份文件")
                return None
            backup_files.sort(reverse=True)
            latest_backup = backup_files[0]
            backup_path = os.path.join(self.backup_dir, latest_backup)
            with open(backup_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            logging.info(f"从备份恢复成功: {latest_backup}")
            return save_data
        except Exception as e:
            logging.error(f"恢复备份失败: {e}")
            return None

    def delete_save(self, save_slot: int) -> bool:
        """删除存档"""
        try:
            save_file = self.get_save_file_path(save_slot)
            if os.path.exists(save_file):
                os.remove(save_file)
                logging.info(f"存档删除成功: 槽位 {save_slot}")
                return True
            else:
                logging.warning(f"存档文件不存在: {save_file}")
                return False
        except Exception as e:
            logging.error(f"删除存档失败: {e}")
            return False

    def get_save_info(self, save_slot: int) -> Optional[Dict[str, Any]]:
        """获取存档信息"""
        try:
            save_data = self.load_game(save_slot)
            if not save_data:
                return None
            metadata = save_data.get('metadata', {})
            player_data = save_data.get('player', {})
            return {
                'slot': save_slot,
                'player_name': player_data.get('name', '未知'),
                'day_count': save_data.get('day_count', 1),
                'save_time': metadata.get('save_time', '未知'),
                'location': player_data.get('location', '未知'),
                'health': player_data.get('health', 0),
                'max_health': player_data.get('max_health', 0),
                'version': metadata.get('version', '未知')
            }
        except Exception as e:
            logging.error(f"获取存档信息失败: {e}")
            return None

    def list_all_saves(self) -> Dict[int, Dict[str, Any]]:
        """列出所有存档"""
        saves = {}
        for slot in range(1, 6):
            save_info = self.get_save_info(slot)
            if save_info:
                saves[slot] = save_info
        return saves

    def cleanup_old_backups(self, max_backups: int = 5) -> bool:
        """清理旧的备份文件"""
        try:
            backup_groups = {}
            for filename in os.listdir(self.backup_dir):
                if filename.startswith("save_slot_") and filename.endswith(".json"):
                    parts = filename.split('_')
                    if len(parts) >= 3:
                        slot = int(parts[2])
                        if slot not in backup_groups:
                            backup_groups[slot] = []
                        backup_groups[slot].append(filename)
            for slot, backups in backup_groups.items():
                if len(backups) > max_backups:
                    backups.sort(reverse=True)
                    for backup in backups[max_backups:]:
                        backup_path = os.path.join(self.backup_dir, backup)
                        os.remove(backup_path)
                        logging.info(f"删除旧备份: {backup}")
            return True
        except Exception as e:
            logging.error(f"清理备份失败: {e}")
            return False

    def export_save(self, save_slot: int, export_path: str) -> bool:
        """导出存档"""
        try:
            save_data = self.load_game(save_slot)
            if not save_data:
                return False
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            logging.info(f"存档导出成功: {export_path}")
            return True
        except Exception as e:
            logging.error(f"导出存档失败: {e}")
            return False

    def import_save(self, save_slot: int, import_path: str) -> bool:
        """导入存档"""
        try:
            if not os.path.exists(import_path):
                logging.error(f"导入文件不存在: {import_path}")
                return False
            with open(import_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            if not self.validate_save_data(save_data):
                logging.error("导入的存档数据验证失败")
                return False
            return self.save_game(save_slot, save_data)
        except Exception as e:
            logging.error(f"导入存档失败: {e}")
            return False

    def get_save_statistics(self, save_slot: int) -> Optional[Dict[str, Any]]:
        """获取存档统计信息"""
        try:
            save_data = self.load_game(save_slot)
            if not save_data:
                return None
            player_data = save_data.get('player', {})
            stats = player_data.get('stats', {})
            return {
                'days_survived': stats.get('days_survived', 0),
                'enemies_defeated': stats.get('enemies_defeated', 0),
                'locations_discovered': stats.get('locations_discovered', 0),
                'items_crafted': stats.get('items_crafted', 0),
                'crops_harvested': stats.get('crops_harvested', 0),
                'quests_completed': stats.get('quests_completed', 0),
                'npcs_met': stats.get('npcs_met', 0),
                'total_play_time': stats.get('total_play_time', 0)
            }
        except Exception as e:
            logging.error(f"获取存档统计失败: {e}")
            return None

    def repair_save_file(self, save_slot: int) -> bool:
        """修复损坏的存档文件"""
        try:
            save_data = self.load_game(save_slot)
            if not save_data:
                return False
            repaired = False
            player_data = save_data.get('player', {})
            if 'health' not in player_data:
                player_data['health'] = 100
                player_data['max_health'] = 100
                repaired = True
            if 'stamina' not in player_data:
                player_data['stamina'] = 100
                player_data['max_stamina'] = 100
                repaired = True
            if 'mental' not in player_data:
                player_data['mental'] = 100
                player_data['max_mental'] = 100
                repaired = True
            if 'inventory' not in player_data:
                player_data['inventory'] = {'food': 5, 'water': 5, 'materials': 10, 'medicine': 2}
                repaired = True
            if repaired:
                logging.info(f"修复存档数据: 槽位 {save_slot}")
                return self.save_game(save_slot, save_data)
            return True
        except Exception as e:
            logging.error(f"修复存档失败: {e}")
            return False

    def migrate_save_data(self, save_slot: int, target_version: str) -> bool:
        """迁移存档数据到新版本"""
        try:
            save_data = self.load_game(save_slot)
            if not save_data:
                return False
            current_version = save_data.get('metadata', {}).get('version', '1.0.0')
            if current_version == target_version:
                logging.info("存档版本已是最新，无需迁移")
                return True
            # 版本迁移逻辑可在此扩展
            logging.info(f"迁移存档从 {current_version} 到 {target_version}")
            if 'metadata' not in save_data:
                save_data['metadata'] = {}
            save_data['metadata']['version'] = target_version
            save_data['metadata']['migrated_at'] = datetime.now().isoformat()
            return self.save_game(save_slot, save_data)
        except Exception as e:
            logging.error(f"迁移存档失败: {e}")
            return False