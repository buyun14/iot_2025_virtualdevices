export type DeviceType = 
  | 'light'
  | 'thermostat'
  | 'doorlock'
  | 'blind'
  | 'ac'
  | 'smoke_detector'
  | 'fan'
  | 'plug';

export interface Device {
  type: DeviceType;
  online: boolean;
  last_update: string;
  error_state?: string;
  [key: string]: any;
}

export interface DeviceCommand {
  command: string;
  [key: string]: any;
}

export interface DeviceControl {
  command: string;
  label: string;
  type?: 'range' | 'number' | 'select';
  class?: string;
  min?: number;
  max?: number;
  step?: number;
  param?: string;
  options?: string[];
} 