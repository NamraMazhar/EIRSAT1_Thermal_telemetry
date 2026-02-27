%% EIRSAT-1 Synthetic Thermal Telemetry Generator
% Week 01 Dataset Generation

clear; clc;

%% 1. Reproducibility
rng(1337);

%% 2. Time Settings
start_time = datetime(2023,1,1,0,0,0);
days_total = 30;          % 30 days of data
dt_seconds = 60;          % 1-minute sampling

timestamps = (start_time : seconds(dt_seconds) : ...
              start_time + days(days_total))';

n_samples = length(timestamps);

%% 3. Channel Definitions
channels = {
    'TEMP_BAT'
    'TEMP_CPU'
    'TEMP_PANEL_X'
    'TEMP_PANEL_Y'
    'TEMP_PAYLOAD'
    'TEMP_STRUCTURE'
};

n_channels = length(channels);

%% 4. Generate Thermal Data
all_timestamp = [];
all_channel   = [];
all_value     = [];

orbital_period_minutes = 90;           % Simulated orbital thermal cycle
orbital_freq = 2*pi / (orbital_period_minutes*60);

for c = 1:n_channels
    
    base_temp = 15 + 10*rand();        % Random baseline temperature
    
    t_seconds = (0:n_samples-1)' * dt_seconds;
    
    % Orbital sinusoidal variation
    variation = 5 * sin(orbital_freq * t_seconds);
    
    % Gaussian noise
    noise = 0.5 * randn(n_samples,1);
    
    values = base_temp + variation + noise;
    
    % Introduce 1% random missing samples
    missing_idx = randperm(n_samples, round(0.01*n_samples));
    values(missing_idx) = NaN;
    
    % Append to master arrays
    all_timestamp = [all_timestamp; timestamps];
    all_channel   = [all_channel; repmat(channels(c), n_samples,1)];
    all_value     = [all_value; values];
end

%% 5. Create Table
T = table(all_timestamp, all_channel, all_value, ...
    'VariableNames', {'timestamp','channel','value'});

%% 6. Save to Project Raw Folder

project_root = 'D:\EIRSAT1_Thermal_telemetry\eirsat_week01_project';

output_folder = fullfile(project_root, ...
    'data', 'raw', 'eirsat1_original');

% Create folder if it doesn't exist
if ~exist(output_folder, 'dir')
    mkdir(output_folder);
end

output_path = fullfile(output_folder, 'synthetic_telemetry.csv');

% Write CSV
writetable(T, output_path);

%% 7. Confirmation Output
disp("---------------------------------------------------");
disp("Dataset generated successfully.");
disp("Saved to:");
disp(output_path);
disp("Total rows generated:");
disp(height(T));
disp("---------------------------------------------------");