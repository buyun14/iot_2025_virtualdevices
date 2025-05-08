import type { Device, DeviceCommand } from '@/types/device';

const API_BASE_URL = 'http://localhost:5000/api';

export const api = {
  async getDevices(): Promise<Record<string, Device>> {
    const response = await fetch(`${API_BASE_URL}/devices`);
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
    return response.json();
  },

  async removeDevice(id: string): Promise<{ message: string } | { error: string }> {
    const response = await fetch(`${API_BASE_URL}/devices/${id}`, {
      method: 'DELETE',
    });
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
    return response.json();
  },
}; 