clc;
clear all;
% close all;
% =========================================================================
% Written by:
%     - Byunghee CHOI, 2020--2021
%     - if you have any inquaries regarding the script, contact:
%         - bghechoi@gmail.com
%         - github.com/holmesjr42
% =========================================================================
%% start
%% path
route = 'D:\DATA\ELECTRO\'; % file location
Animal = 'CL127_20210719'; % animal number & date

%% load file
% chooose offset file you want to analyze
[filename_Tsp, pathname] = uigetfile('*zt_*.mat', 'Pick a mat-file',...
    [route, Animal, '/tsp/'],'MultiSelect', 'on');

% lfp file location and name
pathnamel = char(strcat(pathname(1:end-4),'lfp/'));
filename_LFP = char(strcat('LFP', filename_Tsp(4:end)));

% file loading
load([pathname filename_Tsp]);
load([pathnamel filename_LFP]); % LFP are in samples length=194832 / sr_lfp = 183.544

nt_snip = Tsp; % tsp data of the file
nt_lfp = LFP; % lfp data of the file

for i=1:49
    list_freq(i)=round(500*2^((i-1)*1/8));
end

%% SPL dB and noise condition
db = filename_Tsp(23:24); % SPL dB of the noise

% trying to get the parameter for noise and silence duration from the file
% name
if strcmp(filename_Tsp(25), '_') == false
    cond = filename_Tsp(25:27);
elseif strcmp(filename_Tsp(26), '_') == false
    cond = filename_Tsp(26:28);
end

cond3 = filename_Tsp(30:33); % center freauency of the notch (4000 == white noise)
sr_lfp = 1061.5; % sampling rate of lfp

% for i=1:16
%     lfp{i} = linenoise_removal(LFP{i},sr_lfp);
% end
 
%% Divide time window into onset and offset
% probable density function as a convolution filter to smooth the histogram
filter=pdf('normal',-2:2,0,1);
dt1 = 1;
dt2 = 100;
time = 180000; % total session duration, 3 min
% depending on the stimulus condition, this changes these parameters

% There is no way to optimize this script since MATLAB 2015 does not have
% function "split" to split a string with delimiters instead of selecting
% the eff element index from a string array. The reason why I use 

tran = [str2num(cond(1)) + str2num(cond(3))] * 1000; % time window range = noise + silence e.g. noise 3 ms + silence 1 s = tran 4000 ms
ef = tran; % this is to draw 4 s borderline in the plots
eb = str2num(cond(1)) * 1000; % this is to draw offset borderline in the plot
ei = 0; % this is to draw 0 s borderline in the plot
session = time / tran; % how many sweeps inside 3 minute
ral = (0:tran:time - tran) + dt1; % low lim of each time window
rah = (tran:tran:time); % high lim of each time window

% channel you want to select
% cha_int = [2 4 6 8 10 12 14 15];

% Nexus Rearrangment
Nexus_arrn=[1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16];

%% calculating things- notch noise?

mua = cell(1, 16);

% spike

for i=1:16
    mua{i}=zeros(round(180*1000),1);
    if round(nt_snip{i}*1000)>0
        mua{i}(round(nt_snip{i}*1000),1)=1;
    else
        kk=round(nt_snip{i}*1000);
        ikk=find(kk>0);
        mua{i}(kk(ikk),1)=1;
    end
end

% calculation

nrasters = cell(1, 16); % 16 channel
s_psth = zeros(16, tran); % average
ncs_psth = zeros(16, tran);

for j = 1:16
    for i = 1:session
        nrasters{j}(i, :) = mua{j}(ral(1,i):rah(1,i)); % dividing tsp into the sessions
    end
end

for i = 1:16
    s_psth(i, :) = sum(nrasters{i}); % sum all the sessions
    miid = conv(s_psth(i, :), filter)/(session*0.001); % averaging & smoothing psth
    ncs_psth(i, :) = miid(1:end - (length(filter) - 1)); % smoothed psth
    
end

%% calculating LFP

lfp = cell(1, 16);

% calculation 

lfps = cell(1, 16);
array = round(tran * sr_lfp / 1000);

lfp_a = zeros(16, array);
lfp_s = zeros(1, 16);
lfp_mm = zeros(1, 16);
for j = 1:16
    for i = 1:session
        l_ral = round(ral(1,i) * sr_lfp / 1000);
%         disp(l_rah - l_ral)
%         disp(length(nt_lfp{j}(l_ral:l_rah)))
        lfps{j}(i, :) = nt_lfp{j}(l_ral:l_ral + array - 1);
        
    end
end

for i = 1:16

    lfp_a(i, :) = mean(lfps{i});
    ti = round(100 * sr_lfp / 1000);
    tf = round(500 * sr_lfp / 1000);
end



%% plot

figure;
set(gcf, 'units','normalized','outerposition',[0 0 1 1]);
depth = 0:100:1500;

ff1 = linspace(0.88, 0.075, length(16));
xl = tran + 100;

nn_c = [36 146 255]/255;
wn_c = [200 70 70]/255;

%% ylim
% psth
eb2 = eb - 100;
pfi = eb2; % offset initial point for spikes
pff = eb2 + 500; % offset final point for spikes
pmx = round(max(max(ncs_psth(:, eb2:eb2 + 500))) * 1.3);
pmn = 0;
% lfp
lfi = round(pfi * sr_lfp / 1000); % offset initial point for lfp
lff = round(pff * sr_lfp / 1000); % offset final point for lfp

lmx = round(max(max(lfp_a(:, lfi:lff))) * 1.3);
lmn = round(min(min(lfp_a(:, lfi:lff))) * 1.3);

% which noise I'm using right now?
if filename_Tsp(end-4) == '1'
    noise = 'NN';
else
    noise = 'WN';
end

%% loop

for i=1:16
    j=[1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4];
    k=[1 1 1 1 2 2 2 2 3 3 3 3 4 4 4 4];
    
    axes('position',[0.06+0.117*2*(j(i)-1) 0.75-0.24*(k(i)-1) 0.115 0.21]);
    bar(ncs_psth(i,:),'FaceColor', nn_c, 'EdgeColor', nn_c);
    hold on;
    px = [eb, eb];
    py = [-1000, 1000];
    qx = [-5000000, 5000000];
    qy = [0, 0];
    plot(px, py, '--k');
%     plot(qx, qy, '-k');
    % x limit and y limit for offset
    set (gca, 'XLim', [pfi pff])
    set (gca, 'YLim', [pmn pmx])
    set(gca,'xticklabel',{' ',' ',' ',' ',' ',' '})
    set(gca,'yticklabel',{' ',' ',' ',' ',' ',' ',' '})
    % ticks & titles
    
    if i==1
        ylabel([noise, ' on/off: ',...
            char(strcat(cond(1), 's/', cond(3), 's')), ' ', db, 'dB']);
    end
    
    
    if i==13
        xticks = [pfi:100:pff];
        xlabel('Time (s)');
        set(gca, 'xtick', xticks);
        set(gca, 'XTickLabel', xticks  * 1e-3, 'FontSize', 8, 'FontWeight', 'bold');
    end
    
    if i==5 || i==9 || i==13
        
        ylabel(['Firing rate (spk / s)', ' ', char(strcat(cond3, 'Hz'))])
        
        set(gca, 'ytick', [0, round(pmx/2), pmx]);
        set(gca, 'yticklabel',... 
            [0, round(pmx/2), pmx], 'FontSize', 8, 'FontWeight', 'bold');
    end

    axes('position',[0.175+0.117*2*(j(i)-1) 0.75-0.24*(k(i)-1) 0.115 0.21])
    plot(lfp_a(i, :), 'Color', wn_c);
    hold on;
    lx = [round(eb * sr_lfp / 1000), round(eb * sr_lfp / 1000)];
    ly = [-2000, 2000];
    plot(lx, ly, '--k');
    hold on;  
    lx2 = [-5000000, 50000000];
    ly2 = [0, 0];
    ly3 = [-20, -20];
    plot(lx2, ly2, '-k');
    plot(lx2, ly3, '-k');
    
    % x limit and y limit for offset
    set (gca, 'XLim', [lfi lff])
    set (gca, 'YLim', [lmn lmx])
    set(gca,'xticklabel',{' ',' ',' ',' ',' ',' '})
    set(gca,'yticklabel',{' ',' ',' ',' ',' ',' ',' '})
   

end



