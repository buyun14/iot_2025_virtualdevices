"""
设备API路由
"""
from flask import Blueprint, jsonify, request, current_app
from ..services.device_manager import DeviceManager

# 创建设备路由蓝图
device_bp = Blueprint('devices', __name__)

@device_bp.route('/devices', methods=['GET'])
def get_devices():
    """获取所有设备状态"""
    try:
        device_manager = current_app.device_manager
        devices = device_manager.get_all_devices()
        return jsonify(devices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@device_bp.route('/devices', methods=['POST'])
def add_device():
    """添加新设备"""
    try:
        data = request.get_json()
        device_id = data.get('id')
        device_type = data.get('type')
        
        if not device_id or not device_type:
            return jsonify({"error": "设备ID和类型不能为空"}), 400
        
        device_manager = current_app.device_manager
        if device_manager.add_device(device_id, device_type):
            return jsonify({"message": "设备添加成功"}), 201
        else:
            return jsonify({"error": "设备添加失败"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@device_bp.route('/devices/<device_id>', methods=['DELETE'])
def remove_device(device_id):
    """移除设备"""
    try:
        device_manager = current_app.device_manager
        if device_manager.remove_device(device_id):
            return jsonify({"message": "设备移除成功"}), 200
        else:
            return jsonify({"error": "设备不存在"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@device_bp.route('/devices/<device_id>/command', methods=['POST'])
def send_command(device_id):
    """发送设备命令"""
    try:
        command = request.get_json()
        if not command:
            return jsonify({"error": "命令数据不能为空"}), 400
        
        device_manager = current_app.device_manager
        if device_manager.handle_command(device_id, command):
            return jsonify({"message": "命令发送成功"}), 200
        else:
            return jsonify({"error": "设备不存在"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500 