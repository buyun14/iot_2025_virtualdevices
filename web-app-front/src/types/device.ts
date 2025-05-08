import type { DeviceType } from '@/constants/device';

export interface DeviceState {
  on?: boolean;
  state?: string;
  brightness?: number;
  color_temp?: number;
  power_consumption?: number;
  temp?: number;
  mode?: string;
  fan_speed?: string;
  swing?: boolean;
  locked?: boolean;
  battery_level?: number;
  last_lock_time?: string;
  last_unlock_time?: string;
  tamper_alert?: boolean;
  position?: number;
  tilt?: number;
  moving?: boolean;
  last_move_time?: string;
  alarm?: boolean;
  smoke_level?: number;
  last_test_time?: string | null;
  speed?: number;
  oscillate?: boolean;
  timer?: number;
  voltage?: number;
  current?: number;
  schedule?: Array<{
    time: string;
    action: string;
  }>;
  error_state?: string;
  online?: boolean;
  last_update?: string;
}

export interface Device {
  id: string;
  type: DeviceType;
  state: DeviceState;
}

export interface DeviceCommand {
  command: string;
  [key: string]: any;
}

export interface DeviceControl {
  command: string;
  label: string;
  type?: 'number' | 'range' | 'select';
  param?: string;
  min?: number;
  max?: number;
  step?: number;
  options?: string[];
  class?: string;
} 