import type { Device, DeviceCommand } from '@/types/device';

const API_BASE_URL = 'http://localhost:5000/api';

export const api = {
  async getDevices(): Promise<Device[]> {
    const response = await fetch(`${API_BASE_URL}/devices`);
    if (!response.ok) {
      throw new Error('获取设备列表失败');
    }
    return response.json();
  },

  async addDevice(type: string, id: string): Promise<{ message: string } | { error: string }> {
    const response = await fetch(`${API_BASE_URL}/devices`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ type, id }),
    });
    if (!response.ok) {
      throw new Error('添加设备失败');
    }
    return response.json();
  },

  async removeDevice(id: string): Promise<{ message: string } | { error: string }> {
    const response = await fetch(`${API_BASE_URL}/devices/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('删除设备失败');
    }
    return response.json();
  },

  async sendCommand(id: string, command: DeviceCommand): Promise<{ message: string } | { error: string }> {
    const response = await fetch(`${API_BASE_URL}/devices/${id}/command`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(command),
    });
    if (!response.ok) {
      throw new Error('发送命令失败');
    }
    return response.json();
  },
}; 