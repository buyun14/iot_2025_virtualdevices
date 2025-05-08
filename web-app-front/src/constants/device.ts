import type { DeviceControl } from '@/types/device';

export const DEVICE_TYPES = [
  'light',
  'thermostat',
  'doorlock',
  'blind',
  'ac',
  'smoke_detector',
  'fan',
  'plug',
] as const;

export const DEVICE_ICONS: Record<string, string> = {
  light: 'bi-lightbulb',
  thermostat: 'bi-thermometer-half',
  doorlock: 'bi-door-closed',
  blind: 'bi-window',
  ac: 'bi-snow',
  smoke_detector: 'bi-shield-exclamation',
  fan: 'bi-fan',
  plug: 'bi-power',
};

export const DEVICE_COMMANDS: Record<string, DeviceControl[]> = {
  light: [
    { command: 'turn_on', label: '开启', class: 'btn-success' },
    { command: 'turn_off', label: '关闭', class: 'btn-danger' },
    { command: 'set_brightness', label: '设置亮度', type: 'range', min: 0, max: 100 },
    { command: 'set_color_temp', label: '设置色温', type: 'range', min: 2700, max: 6500 },
  ],
  thermostat: [
    { command: 'set_target_temp', label: '设置目标温度', type: 'number', min: 16, max: 30 },
    { command: 'set_mode', label: '设置模式', type: 'select', options: ['auto', 'heat', 'cool'] },
    { command: 'set_fan_speed', label: '设置风速', type: 'select', options: ['auto', 'low', 'medium', 'high'] },
  ],
  doorlock: [
    { command: 'lock', label: '上锁', class: 'btn-warning' },
    { command: 'unlock', label: '解锁', class: 'btn-success' },
  ],
  blind: [
    { command: 'open', label: '打开', class: 'btn-success' },
    { command: 'close', label: '关闭', class: 'btn-danger' },
    { command: 'set_position', label: '设置位置', type: 'range', min: 0, max: 100 },
    { command: 'set_tilt', label: '设置倾斜角度', type: 'range', min: 0, max: 180 },
  ],
  ac: [
    { command: 'turn_on', label: '开启', class: 'btn-success' },
    { command: 'turn_off', label: '关闭', class: 'btn-danger' },
    { command: 'set_temp', label: '设置温度', type: 'number', min: 16, max: 30, step: 0.5, param: 'temperature' },
    { command: 'set_mode', label: '设置模式', type: 'select', options: ['cool', 'heat', 'dry', 'fan'], param: 'mode' },
    { command: 'set_fan_speed', label: '设置风速', type: 'select', options: ['auto', 'low', 'medium', 'high'], param: 'speed' },
    { command: 'toggle_swing', label: '切换摆风', class: 'btn-info' },
  ],
  smoke_detector: [
    { command: 'reset', label: '重置报警', class: 'btn-warning' },
    { command: 'test', label: '测试', class: 'btn-info' },
  ],
  fan: [
    { command: 'turn_on', label: '开启', class: 'btn-success' },
    { command: 'turn_off', label: '关闭', class: 'btn-danger' },
    { command: 'set_speed', label: '设置风速', type: 'range', min: 1, max: 3 },
    { command: 'toggle_oscillate', label: '切换摆头', class: 'btn-info' },
    { command: 'set_timer', label: '设置定时', type: 'number', min: 0, max: 120 },
  ],
  plug: [
    { command: 'turn_on', label: '开启', class: 'btn-success' },
    { command: 'turn_off', label: '关闭', class: 'btn-danger' },
    { command: 'set_timer', label: '设置定时', type: 'number', min: 0, max: 120 },
  ],
};

export const STATUS_TRANSLATIONS: Record<string, string> = {
  state: '状态',
  brightness: '亮度',
  color_temp: '色温',
  power_consumption: '功率',
  current_temp: '当前温度',
  target_temp: '目标温度',
  humidity: '湿度',
  mode: '模式',
  fan_speed: '风速',
  locked: '锁定状态',
  battery_level: '电池电量',
  position: '位置',
  tilt: '倾斜角度',
  moving: '移动中',
  swing: '摆风',
  alarm: '报警状态',
  smoke_level: '烟雾等级',
  oscillate: '摆头',
  timer: '定时',
  voltage: '电压',
  current: '电流',
  power_factor: '功率因数',
}; 